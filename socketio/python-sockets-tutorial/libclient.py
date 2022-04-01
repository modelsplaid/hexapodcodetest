import sys
import selectors
import json
import io
import struct
import logging
import queue
class Message:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self.request = None
        self._recv_raw_buffer = b""
        self._send_buffer = b""
        self._request_queued = False
        self._jsonheader_len = None
        self.jsonheader = None
        self.response = None
        self.recv_queue = queue.Queue()


    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {mode!r}.")
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
            #print("received data in _read(): "+str(data) )
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            print("client is not connected")
            #pass
            return False
    
        except ConnectionRefusedError:
            print("connection refused")
            return False
        else:
            if data:
                self._recv_raw_buffer += data
            else:
                print("---peer closed")
                return False
        return True



    def write(self):
        if len(self._send_buffer)>=0:
            
            print(f"Sending {self._send_buffer!r} to {self.addr}")
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                print("Resource temporarily unavailable (errno EWOULDBLOCK)")
                pass

            else:
                self._send_buffer = self._send_buffer[sent:]

    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        #print("json_bytes: "+str(json_bytes))
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def _create_message(
        self, *, content_bytes, content_type, content_encoding
    ):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            if(self.read()==False):
                return False
            
        if mask & selectors.EVENT_WRITE:
            self.write()
        
        return True

    def server_send_json(self,json_data):
        self.queue_request(json_data) 
        self._set_selector_events_mask("rw") 

    def read(self):
        if(self._read()==False):
            return False
        
        if self._jsonheader_len is None:
            self.process_protoheader()        

        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()
        
        if self.jsonheader:
            if self.response is None:
                self.process_response()

        return True

    def send_json(self,json_data):
        a=0



    
    def close(self):
        print(f"Closing connection to {self.addr}")
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(
                f"Error: selector.unregister() exception for "
                f"{self.addr}: {e!r}"
            )

        try:
            self.sock.close()
        except OSError as e:
            print(f"Error: socket.close() exception for {self.addr}: {e!r}")
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def queue_request(self,sentdata):
        content = sentdata
        content_type = self.request["type"]
        content_encoding = self.request["encoding"]
       
        req = {
            "content_bytes": self._json_encode(content, content_encoding),
            "content_type": content_type,
            "content_encoding": content_encoding,
        }
 
        message = self._create_message(**req)
        self._send_buffer += message

    def process_protoheader(self):
        hdrlen = 2 # first two bytes is header, contains message length info
        if len(self._recv_raw_buffer) >= hdrlen:
            self._jsonheader_len = struct.unpack(
                ">H", self._recv_raw_buffer[:hdrlen]
            )[0]
            self._recv_raw_buffer = self._recv_raw_buffer[hdrlen:]
            logging.debug("self._jsonheader_len:"+str(self._jsonheader_len))

    def process_jsonheader(self):
        hdrlen = self._jsonheader_len
        if len(self._recv_raw_buffer) >= hdrlen:
            self.jsonheader = self._json_decode(
                self._recv_raw_buffer[:hdrlen], "utf-8"
            )
            logging.debug("len(self._recv_raw_buffer):"+str(len(self._recv_raw_buffer)))
            logging.debug("self._jsonheader_len:"+str(self._jsonheader_len))
            logging.debug("self.jsonheader:"+str(self.jsonheader))
            self._recv_raw_buffer = self._recv_raw_buffer[hdrlen:]
            for reqhdr in (
                "byteorder",
                "content-length",
                "content-type",
                "content-encoding",
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f"Missing required header '{reqhdr}'.")

    def process_response(self):
        content_len = self.jsonheader["content-length"]

        #logging.debug("len(self._recv_raw_buffer):"+str(len(self._recv_raw_buffer))+" content_len:"+str(content_len))
        
        # if not received full data pack 
        if not len(self._recv_raw_buffer) >= content_len:
            logging.error("not received full data pack. if not len(self._recv_raw_buffer) >= content_len")
            print("not received full data pack. return process_response")
            return

        # if  received full data pack, start to process it 
        data = self._recv_raw_buffer[:content_len]
        self._recv_raw_buffer = self._recv_raw_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.response = self._json_decode(data, encoding)
            logging.debug("self.response:"+str(self.response))
            #print(f"Received response {self.response!r} from {self.addr}")
            
            self.recv_queue.put(self.response) # pop out the queu
            ## init for next return
            self._jsonheader_len = None
            self.response = None
            self.jsonheader = None
            self._recv_raw_buffer = b""
            #self._process_response_json_content()
   
    def get_recv_queu(self):
        if(self.recv_queue.empty()==False):
            return self.recv_queue.get()
        else: 
            return False
