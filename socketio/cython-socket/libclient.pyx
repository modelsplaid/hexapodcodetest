import sys
import selectors
import json
import io
import struct
import logging
import queue
import time
import threading
import traceback
import socket


class MessageClient:
    def __init__(self, selector, sock, addr,socket_buffer_sz=4096):
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
        self.request = self.create_request('')
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
            data = self.sock.recv(self.socket_recv_buffer_sz)
            #print("received data in _read(): "+str(data) )
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            print("Resource temporarily unavailable (errno EWOULDBLOCK")
            return False
    
        except ConnectionRefusedError:
            print("Connection refused")
            return False
        else:
            if data:
                self._recv_raw_buffer += data
            else:
                print("---peer closed")
                return False
        return True



    def write(self):
        if len(self._send_buffer)>0:
            
            #print(f"Sending {self._send_buffer!r} to {self.addr}")
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
            self.read()
            
        if mask & selectors.EVENT_WRITE:
            self.write()
        
        return True

    def client_send_json(self,json_data):
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
        self.hdrlen = 2 # first two bytes is header, contains message length info
        if len(self._recv_raw_buffer) >= self.hdrlen:
            self._jsonheader_len = struct.unpack(
                ">H", self._recv_raw_buffer[:self.hdrlen]
            )[0]
            self._recv_raw_buffer = self._recv_raw_buffer[self.hdrlen:]
            logging.debug("self._jsonheader_len:"+str(self._jsonheader_len))

    def process_jsonheader(self):
        if len(self._recv_raw_buffer) >= self._jsonheader_len:
            self.jsonheader = self._json_decode(
                self._recv_raw_buffer[:self._jsonheader_len], "utf-8"
            )
            self._recv_raw_buffer = self._recv_raw_buffer[self._jsonheader_len:]
            for reqhdr in (
                "byteorder","content-length",
                "content-type","content-encoding",):

                if reqhdr not in self.jsonheader:
                    raise ValueError(f"Missing required header '{reqhdr}'.")
            return True  # means the raw buffer contains all json header content, and processed it 
        else: 
            print("!!!!!!THIIS WARNING MEANS: RECEIVE BUFFER SIZE  IS NOT ENOUGH, CONSIDER TO INCREASE BUFFER SIZE, OR YOU MAY LOSE DATA !!!!!")
            return False

    def process_response(self):
        content_len = self.jsonheader["content-length"]

        #logging.debug("len(self._recv_raw_buffer):"+str(len(self._recv_raw_buffer))+" content_len:"+str(content_len))
        
        # if not received full data pack 
        if  content_len > len(self._recv_raw_buffer):
            logging.error("not received full data pack. if not len(self._recv_raw_buffer) >= content_len")
            print("!!!!!!not received full data pack. return process_response")
            return False

        else:
            # if  received full data pack, start to process it 
            data = self._recv_raw_buffer[:content_len]
            self._recv_raw_buffer = self._recv_raw_buffer[content_len:]

            if self.jsonheader["content-type"] == "text/json":
                encoding = self.jsonheader["content-encoding"]
                self.response = self._json_decode(data, encoding)
                logging.debug("self.response:"+str(self.response))
                #print(f"Received response {self.response!r} from {self.addr}")

                self.recv_queue.put(self.response) # pop out the queu
                # to prepare decode next frame in buffer
                self.response = None
                self._jsonheader_len = None                
                self.jsonheader = None
            return True
    def get_recv_queu(self):
        if(self.recv_queue.empty()==False):
            return self.recv_queue.get()
        else: 
            return False


class MiniSocketClient:
    def __init__(self,host="",port=12345,send_freq=500,socket_buffer_sz=4096):
        self.socket_recv_buffer_sz = socket_buffer_sz
        self.SERVER_MAX_SEND_RECV_FREQUENCY_HZ = send_freq
        self.user_message = ''
        self.user_message_queu = queue.Queue()
        self.sel = selectors.DefaultSelector()        
        self.start_connection(host, port)

        #self.test_commu_thread = threading.Thread(target=self.test_commu_thread, args=(2,))
        #self.test_commu_thread.daemon = True
        #self.test_commu_thread.start()

        self.socket_thread_obj = threading.Thread(target=self.socket_thread, args=(2,))
        self.socket_thread_obj.daemon = True
        self.socket_thread_obj.start()
        self.recv_queues = queue.Queue()
        
        print("Mini socket client done init")

    def push_sender_queu(self,user_input):
        self.user_message_queu.put(user_input)

    def pop_receiver_queue(self):
        if (self.recv_queues.empty()==False):
            return self.recv_queues.get()
        else:
            return False

    def start_connection(self,host, port):
        addr = (host, port)
        print(f"Starting connection to {addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        connectstat=sock.connect_ex(addr)
        print("connectstat: "+str(connectstat))
        print("sock: "+str(sock))
        #events = selectors.EVENT_READ
        events = selectors.EVENT_READ| selectors.EVENT_WRITE
        libclient_obj = MessageClient(self.sel, sock, addr,self.socket_recv_buffer_sz)
        self.sel.register(sock, events, data=libclient_obj)

        return True


    def socket_thread(self,name): 
        
        try:
            runstatus = True
            while  runstatus:
                self.sleep_freq_hz()
                events = self.sel.select(1)

                # load data and events for each connected client 
                #if(self.user_message is not ''):  # if new data is coming from servos
                #print("self.user_message_queu.empty(): "+str(self.user_message_queu.empty()) )
                if(self.user_message_queu.empty() is  False):
                    self.user_message = self.user_message_queu.get()
                    #print("user_message: "+str(self.user_message))
                    for key, mask in events: # loop over each client connect objs
                        if key.data is not None:  # if connected to the client
                            libclient_obj = key.data
                            #print("socket libclient_obj will send： "+self.user_message)
                            libclient_obj.client_send_json(self.user_message)                                     


                    self.user_message = '' # clear out    
                else: 
                    #sleep longer to decrease cpu rate
                    self.sleep_freq_hz(100)
                    pass
                for key, mask in events:
                    libclient_obj = key.data
                    try:

                        if(libclient_obj.process_events(mask)==False):
                            runstatus = False

                        while(True): # loop over every element in recv buffer
                            onedata = libclient_obj.get_recv_queu()   

                            if(onedata is not False): 
                                self.recv_queues.put(onedata)
                                #print("++++ received from server data: "+str(onedata))  
                            else:
                                break

                    except Exception:
                        print(
                            f"Main: Error: Exception for {libclient_obj.addr}:\n"
                            f"{traceback.format_exc()}"
                        )
                        libclient_obj.close()

                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    print("get_map")
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
            return
        finally:
            print("---self.sel.close")
            self.sel.close()
            return


    def test_commu_thread(self,name):        
        counter = 0
        while(True):
            #str_usr = input("Type what you want to send: ")
            #print("This content will send to client: "+str_usr)
            counter = counter+1
            self.user_message = "client counter value: "+str(counter)
            time.sleep(0.01)

    def sleep_freq_hz(self,freq_hz=500):
        period_sec = 1.0/freq_hz
        time.sleep(period_sec)
