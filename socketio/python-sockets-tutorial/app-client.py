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
#format='%(filename)s,%(funcName)s,%(lineno)d,%(name)s ,%(process)d, %(levelname)s,%(message)s')

logging.basicConfig(level=logging.INFO, 
format='%(filename)s,%(funcName)s,%(lineno)d,%(name)s ,%(process)d, %(levelname)s,%(message)s')


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
    sock.connect_ex(addr)
    events = selectors.EVENT_READ
    #events = selectors.EVENT_READ| selectors.EVENT_WRITE
    message = libclient.Message(sel, sock, addr)
    sel.register(sock, events, data=message)


if len(sys.argv) !=3:
    print(f"Usage: {sys.argv[0]} <host> <port> ")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
start_connection(host, port)


try:
    while True:
        sleep_freq_hz()
        events = sel.select(None)
        for key, mask in events:
            message = key.data
            try:

                message.process_events(mask)
            except Exception:
                print(
                    f"Main: Error: Exception for {message.addr}:\n"
                    f"{traceback.format_exc()}"
                )
                message.close()
            onedata = message.get_recv_queu()    
            if(onedata is not False): 
                print("server data: "+str(onedata))            
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('This will get logged')
    #x = threading.Thread(target=socket_thread, args=(1,))
    #x1 = threading.Thread(target=servo_commu_thread, args=(1,))
    #x1.start()
    #x.start()
    #x1.join()
    #x.join()