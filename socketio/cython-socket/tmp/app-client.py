#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback
import time
import libclient
import logging
import threading

#logging.basicConfig(filename='app.log', level=logging.DEBUG,filemode='w', 
#format='%(filename)s,%(funcName)s,%(lineno)d,%(name)s ,%(process)d, %(levelname)s,%(libclient_obj)s')
user_message = ''
logging.basicConfig(level=logging.INFO, 
format='%(filename)s,%(funcName)s,%(lineno)d,%(name)s ,%(process)d, %(levelname)s,%(libclient_obj)s')


sel = selectors.DefaultSelector()

SERVER_MAX_SEND_RECV_FREQUENCY_HZ = 500
def sleep_freq_hz(freq_hz=500):
    period_sec = 1.0/freq_hz
    time.sleep(period_sec)

def start_connection(host, port):
    addr = (host, port)
    print(f"Starting connection to {addr}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    connectstat=sock.connect_ex(addr)
    print("connectstat: "+str(connectstat))
    print("sock: "+str(sock))
    #events = selectors.EVENT_READ
    events = selectors.EVENT_READ| selectors.EVENT_WRITE
    libclient_obj = libclient.Message(sel, sock, addr)
    sel.register(sock, events, data=libclient_obj)

    return True

#if len(sys.argv) !=3:
#    print(f"Usage: {sys.argv[0]} <host> <port> ")
#    sys.exit(1)
#
#host, port = sys.argv[1], int(sys.argv[2])

#start_connection(host, port)

user_message = '' # clear out    
def socket_thread(name): 
    global user_message
    
    try:
        runstatus = True
        while  runstatus:
            sleep_freq_hz()
            events = sel.select(1)
           
            # load data and events for each connected client 
            if(user_message is not ''):  # if new data is coming from servos
                #print("user_message: "+str(user_message))
                for key, mask in events: # loop over each client connect objs
                    if key.data is not None:  # if connected to the client
                        libclient_obj = key.data
                        #print("socket libclient_obj will send： "+user_message)
                        libclient_obj.client_send_json(user_message)                                     
            
            
                user_message = '' # clear out    
            else: 
                #sleep longer to decrease cpu rate
                sleep_freq_hz(100)

            for key, mask in events:
                libclient_obj = key.data
                try:

                    if(libclient_obj.process_events(mask)==False):
                        runstatus = False
                    onedata = libclient_obj.get_recv_queu()                      
                    if(onedata is not False): 
                        print("++++ received from server data: "+str(onedata))  
                except Exception:
                    print(
                        f"Main: Error: Exception for {libclient_obj.addr}:\n"
                        f"{traceback.format_exc()}"
                    )
                    libclient_obj.close()

                
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                print("get_map")
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
        return
    finally:
        print("---sel.close")
        sel.close()
        return
    


def servo_commu_thread(name):
    global user_message
    counter = 0
    while(True):
        #str_usr = input("Type what you want to send: ")
        #print("This content will send to client: "+str_usr)
        counter = counter+1
        user_message = "client counter value: "+str(counter)
        time.sleep(0.01)

class MiniSocketServer:
    def __init__(self):
        
        self.SERVER_MAX_SEND_RECV_FREQUENCY_HZ = 500
        
        self.sel = selectors.DefaultSelector()        
        self.start_connection("", 12345)

        self.servo_commu_thread = threading.Thread(target=self.servo_commu_thread, args=(2,))
        self.servo_commu_thread.daemon = True
        self.servo_commu_thread.start()

        self.socket_thread_obj = threading.Thread(target=self.socket_thread, args=(2,))
        self.socket_thread_obj.daemon = True
        self.socket_thread_obj.start()

        print("Mini socket server done init")

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
        libclient_obj = libclient.Message(self.sel, sock, addr)
        self.sel.register(sock, events, data=libclient_obj)

        return True


    def socket_thread(self,name): 
        

        try:
            runstatus = True
            while  runstatus:
                sleep_freq_hz()
                events = self.sel.select(1)

                # load data and events for each connected client 
                if(self.user_message is not ''):  # if new data is coming from servos
                    #print("user_message: "+str(self.user_message))
                    for key, mask in events: # loop over each client connect objs
                        if key.data is not None:  # if connected to the client
                            libclient_obj = key.data
                            #print("socket libclient_obj will send： "+self.user_message)
                            libclient_obj.client_send_json(self.user_message)                                     


                    self.user_message = '' # clear out    
                else: 
                    #sleep longer to decrease cpu rate
                    sleep_freq_hz(100)

                for key, mask in events:
                    libclient_obj = key.data
                    try:

                        if(libclient_obj.process_events(mask)==False):
                            runstatus = False
                        onedata = libclient_obj.get_recv_queu()                      
                        if(onedata is not False): 
                            print("++++ received from server data: "+str(onedata))  
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


    def servo_commu_thread(self,name):
        
        counter = 0
        while(True):
            #str_usr = input("Type what you want to send: ")
            #print("This content will send to client: "+str_usr)
            counter = counter+1
            self.user_message = "client counter value: "+str(counter)
            time.sleep(0.01)
    def sleep_freq_hz(freq_hz=500):
        period_sec = 1.0/freq_hz
        time.sleep(period_sec)

if __name__ == '__main__':
    m_sock_server = MiniSocketServer()

    for i in range(5):
        time.sleep(0.5)
        print("in main")
    sys.exit()
    '''
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('This will get logged')
    x = threading.Thread(target=socket_thread, args=(1,))
    x1 = threading.Thread(target=servo_commu_thread, args=(1,))
    x1.start()
    x.start()
    x1.join()
    x.join()
    ''' 
