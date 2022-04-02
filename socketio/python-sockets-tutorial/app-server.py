#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback
import time
import libserver
import threading
import logging
sel = selectors.DefaultSelector()

#logging.basicConfig(filename='app.log',level=logging.DEBUG,filemode='w', 
logging.basicConfig(level=logging.INFO,filemode='w', 
format='%(filename)s,%(funcName)s,%(lineno)d,%(name)s ,%(process)d, %(levelname)s,%(libserver_obj)s')
logging.debug('This will get logged')

user_message = ''

SERVER_MAX_SEND_RECV_FREQUENCY_HZ = 500
def sleep_freq_hz(freq_hz=500):
    period_sec = 1.0/freq_hz
    time.sleep(period_sec) 

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    libserver_obj = libserver.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ| selectors.EVENT_WRITE, data=libserver_obj)


if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_WRITE|selectors.EVENT_READ, data=None)

glob_events = [] 

def socket_thread(name):
    global glob_events
    global user_message
    try:
        while True:
            sleep_freq_hz() 
            events = sel.select(None)

            # load data and events for each connected client 
            if(user_message is not ''):  # if new data is coming from servos
                #print("user_message: "+str(user_message))
                for key, mask in events: # loop over each client connect objs
                    if key.data is not None:  # if connected to the client
                        libserver_obj = key.data
                        #print("socket libserver_obj will send： "+user_message)
                        libserver_obj.server_send_json(user_message)                                     
                user_message = '' # clear out    

            # parsing events
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    libserver_obj = key.data               
                    try:
                        libserver_obj.process_events(mask)
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
        sel.close()

def servo_commu_thread(name):
    global user_message
    counter = 0
    while(True):
        #str_usr = input("Type what you want to send: ")
        #print("This content will send to client: "+str_usr)
        counter = counter+1
        user_message = "server counter value: "+str(counter)
        time.sleep(1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('This will get logged')
    x = threading.Thread(target=socket_thread, args=(1,))
    x1 = threading.Thread(target=servo_commu_thread, args=(1,))
    x1.start()
    x.start()
    x1.join()
    x.join()
