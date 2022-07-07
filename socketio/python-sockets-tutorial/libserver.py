import sys
import selectors
import json
import io
import struct
import logging
import queue
import threading
import traceback
import socket
import time

class MessageServer:
    def __init__(self, selector, sock, addr,socket_buffer_sz=4096):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_raw_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.response = None
        self.request = self.create_request('')
        self.recv_queue = queue.Queue()
        self.hdrlen = 2
        self.socket_recv_buffer_sz = socket_buffer_sz
    def create_request(self,value):
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(value=value),
            )


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
            #data = self.sock.recv(40)
            data = self.sock.recv(self.socket_recv_buffer_sz)
            #print("recv data: "+str(data))
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            print("# Resource temporarily unavailable (errno EWOULDBLOCK)")
            #pass
            return False
        else:
            if data:
                self._recv_raw_buffer += data
                return True
            else:
                #raise RuntimeError("Peer closed.")
                print("Client closed.")
        return False

    def write(self):
        if len(self._send_buffer)>0:

            #print(f"Sending {self._send_buffer!r} to {self.addr}")
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                print("Resource temporarily unavailable (errno EWOULDBLOCK)")
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]            
      
            
    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
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

        #print("message: "+str(message) )
        return message

    def process_events(self, mask):
        #print("In process_events, mask: "+str(mask))
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()
                
    def server_send_json(self,json_data):
        self.queue_request(json_data) 
        self._set_selector_events_mask("rw")    

    def read(self):
        self._read()

        while len(self._recv_raw_buffer) >= self.hdrlen:
            if self._jsonheader_len is None:
                self.process_protoheader()

            else:
                if self.jsonheader is None:
                    if(self.process_jsonheader() == False):
                        # does not receive all jsonheader yet, quit it to receive more data
                        # stop next function
                        return

            if self.jsonheader:
                if self.process_response() == False:
                    return    # does not receive all jsonheader yet, quit it to receive more data


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

    def process_protoheader(self):
        self.hdrlen = 2  # first two bytes is header, contains message length info
        if len(self._recv_raw_buffer) >= self.hdrlen:
            self._jsonheader_len = struct.unpack(">H", self._recv_raw_buffer[:self.hdrlen])[0]
            self._recv_raw_buffer = self._recv_raw_buffer[self.hdrlen:]

    def process_jsonheader(self):
        if len(self._recv_raw_buffer) >= self._jsonheader_len:
            self.jsonheader = self._json_decode(
                self._recv_raw_buffer[:self._jsonheader_len], "utf-8"
            )
            self._recv_raw_buffer = self._recv_raw_buffer[self._jsonheader_len:]
            for reqhdr in ("byteorder","content-length",
                "content-type","content-encoding",):

                if reqhdr not in self.jsonheader:
                    raise ValueError(f"Missing required header '{reqhdr}'.")
            
            return True  # means the raw buffer contains all json header content, and processed it 
        else: 
            print("!!!!!!THIIS WARNING MEANS: means the raw buffer not contains all json header content, should skip it and wait next recev!!!!!")
            return False# means the raw buffer not contains all json header content, should skip it and wait next recev

    def process_response(self):
        content_len = self.jsonheader["content-length"]

        #logging.debug("len(self._recv_raw_buffer):"+str(len(self._recv_raw_buffer))+" content_len:"+str(content_len))

        # if not received full data pack 
        if  content_len > len(self._recv_raw_buffer):
            logging.error("not received full data pack. if not len(self._recv_raw_buffer) >= content_len")
            print("!!!!!!not received full data pack. return process_response!!!!!!")
            return False
        else:
            # if  received full data pack, start to process it 
            data = self._recv_raw_buffer[:content_len]
            self._recv_raw_buffer = self._recv_raw_buffer[content_len:]

            # decoded one frame of data 
            if self.jsonheader["content-type"] == "text/json": 
                encoding = self.jsonheader["content-encoding"]
                self.response = self._json_decode(data, encoding) 
                logging.debug("self.response:"+str(self.response))
                #print(f"Received response {self.response!r} from {self.addr}")

                self.recv_queue.put(self.response) # pop out the queu
                # to prepare decode next frame in recv buffer
                self.response = None
                self._jsonheader_len = None
                self.jsonheader = None

            return True



    def process_request(self):
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_raw_buffer) >= content_len:
            return
        data = self._recv_raw_buffer[:content_len]
        self._recv_raw_buffer = self._recv_raw_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.request = self._json_decode(data, encoding)
            print(f"Received request {self.request!r} from {self.addr}")
        else:
            # Binary or unknown content-type
            self.request = data
            print(
                f"Received {self.jsonheader['content-type']} "
                f"request from {self.addr}"
            )
        # Set selector to listen for write events, we're done reading.
        #self._set_selector_events_mask("w")

    def get_recv_queu(self):
        if(self.recv_queue.empty()==False):
            return self.recv_queue.get()
        else: 
            return False



# tobo: edit below code 
class MiniSocketServer:

    def __init__(self,host="",port=12345,send_freq=500,socket_buffer_sz=4096):
        
        self.SERVER_MAX_SEND_RECV_FREQUENCY_HZ = send_freq
        self.socket_recv_buffer_sz = socket_buffer_sz
        self.user_message = ''
        self.user_message_queu = queue.Queue()
        self.sel = selectors.DefaultSelector()        
        self.create_listening_port(host,port)

        self.test_commu_thread = threading.Thread(target=self.test_commu_thread, args=(2,))
        self.test_commu_thread.daemon = True
        self.test_commu_thread.start()

        
        self.socket_thread_obj = threading.Thread(target=self.socket_thread, args=(2,))
        self.socket_thread_obj.daemon = True
        self.socket_thread_obj.start()
        self.recv_queues = queue.Queue()
        
        print("Mini socket server done init")

    def create_listening_port(self,host,port):
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        lsock.bind((host, port))
        lsock.listen()
        print(f"Listening on {(host, port)}")
        lsock.setblocking(False)
        #sel.register(lsock, selectors.EVENT_WRITE|selectors.EVENT_READ, data=None)
        self.sel.register(lsock, selectors.EVENT_READ, data=None)
        return True

    def push_sender_queu(self,user_input):
        self.user_message_queu.put(user_input)

    def pop_receiver_queue(self):
        if (self.recv_queues.empty()==False):
            return self.recv_queues.get()
        else:
            return False

  

    def socket_thread(self,name): 
        try:
            while True:
                self.sleep_freq_hz() 
                events = self.sel.select(None)

                # load data and events for each connected client 
                #if(self.user_message is not ''):  # if new data is coming from servos
                if(self.user_message_queu.empty() is  False):
                    self.user_message = self.user_message_queu.get()
                    #print("self.user_message: "+str(self.user_message))
                    for key, mask in events: # loop over each client connect objs
                        if key.data is not None:  # if connected to the client
                            libserver_obj = key.data
                            #print("socket libserver_obj will send： "+self.user_message)
                            libserver_obj.server_send_json(self.user_message)                                     
                    self.user_message = '' # clear out    
                else: 
                    self.sleep_freq_hz(50)
                    pass
                # parsing events
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        libserver_obj = key.data               
                        try:
                            libserver_obj.process_events(mask)

                            while(True): # loop over every element in recv buffer
                                # todo here: create a recv queue, save data to this recv queue. 
                                # the queue should also have an entry to identify data is from which server 
                                # 
                                onedata = libserver_obj.get_recv_queu()
                                if(onedata is not False):
                                    self.recv_queues.put(onedata)

                                    #print("---- received from client data: "+str(onedata))
                                else: 
                                    break

                            # clear libserver_obj out             
                        except Exception:
                            print(
                                f"Main: Error: Exception for {libserver_obj.addr}:\n"
                                f"{traceback.format_exc()}"
                            )
                            libserver_obj.close()

        except KeyboardInterrupt:
            print("---Caught keyboard interrupt, exiting")
        finally:
            self.sel.close()        
            pass


    def test_commu_thread(self,name):        
        counter = 0
        while(True):
            #str_usr = input("Type what you want to send: ")
            #print("This content will send to server: "+str_usr)
            counter = counter+1
            self.user_message = "server counter value: "+str(counter)
            time.sleep(0.01)


    def accept_wrapper(self,sock):
        conn, addr = sock.accept()  # Should be ready to read
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        libserver_obj = MessageServer(self.sel, conn, addr,self.socket_recv_buffer_sz)
        self.sel.register(conn, selectors.EVENT_READ| selectors.EVENT_WRITE, data=libserver_obj)


    def sleep_freq_hz(self,freq_hz=500):
        period_sec = 1.0/freq_hz
        time.sleep(period_sec)
