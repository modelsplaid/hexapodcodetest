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
user_message = ''
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
    #coninfo = sock.connect_ex(addr)
    coninfo = sock.connect_ex(addr)
    print("coninfo: "+str(coninfo))
    events = selectors.EVENT_READ
    #events = selectors.EVENT_READ| selectors.EVENT_WRITE
    message = libclient.Message(sel, sock, addr)
    sel.register(sock, events, data=message)


if len(sys.argv) !=3:
    print(f"Usage: {sys.argv[0]} <host> <port> ")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])



def socket_thread(name): 

    while True:
        start_connection(host, port)
        try:
            while True:
                sleep_freq_hz()
                print("1")
                events = sel.select(1)
                print("2")
                for key, mask in events:
                    message = key.data
                    try:

                        message.process_events(mask)
                        onedata = message.get_recv_queu()                      
                        if(onedata is not False): 
                            print("server data: "+str(onedata))  
                    except Exception:
                        print(
                            f"Main: Error: Exception for {message.addr}:\n"
                            f"{traceback.format_exc()}"
                        )
                        message.close()
                        break

                    
                # Check for a socket being monitored to continue.
                if not sel.get_map():
                    break
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
            return
        finally:
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
        time.sleep(1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('This will get logged')
    x = threading.Thread(target=socket_thread, args=(1,))
    #x1 = threading.Thread(target=servo_commu_thread, args=(1,))
    #x1.start()
    x.start()
    #x1.join()
    x.join()


# todo: add multi thread and send to server function    
