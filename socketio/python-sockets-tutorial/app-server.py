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
format='%(filename)s,%(funcName)s,%(lineno)d,%(name)s ,%(process)d, %(levelname)s,%(message)s')
logging.debug('This will get logged')

user_message = ''

SERVER_MAX_SEND_RECV_FREQUENCY_HZ = 500
def sleep_freq_hz(freq_hz=500):
    period_sec = 1.0/freq_hz
    time.sleep(period_sec) 

def create_request(action, value):
    if action == "search":
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=action, value=value),
        )
    else:
        return dict(
            type="binary/custom-client-binary-type",
            encoding="binary",
            content=bytes(action + value, encoding="utf-8"),
        )


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)

    request=create_request("search", "value")
    message = libserver.Message(sel, conn, addr,request)
    sel.register(conn, selectors.EVENT_READ| selectors.EVENT_WRITE, data=message)


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
    print("name: "+str(name))
    global user_message
    try:
        while True:
            sleep_freq_hz() 
            events = sel.select(None)

            # parsing events
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    message = key.data               
                    try:
                        message.process_events(mask)
                        # clear message out             
                    except Exception:
                        print(
                            f"Main: Error: Exception for {message.addr}:\n"
                            f"{traceback.format_exc()}"
                        )
                        message.close()
            # load data and events for each connected client 
            if(user_message is not ''):  # if new data is coming from servos
                #print("user_message: "+str(user_message))
                for key, mask in events: # loop over each client connect objs
                    if key.data is not None:  # if connected to the client
                        message = key.data
                        logging.debug("socket message will send： "+user_message)
                        message.queue_request(user_message)
                        message.response_created = False
                        message._set_selector_events_mask("rw")                        
                user_message = '' # clear out                         
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()

def servo_commu_thread(name):
    global user_message
    counter = 0
    while(True):
        #str_usr = input("Type what you want to send: ")
        #print("This content will send to client: "+str_usr)
        counter = counter+1
        user_message = "counter value: "+str(counter)
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
