#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback
import time
import libserver
import threading
import logging
from libserver import MiniSocketServer
#sel = selectors.DefaultSelector()

#logging.basicConfig(filename='app.log',level=logging.DEBUG,filemode='w', 
logging.basicConfig(level=logging.INFO,filemode='w', 
format='%(filename)s,%(funcName)s,%(lineno)d,%(name)s ,%(process)d, %(levelname)s,%(libserver_obj)s')
logging.debug('This will get logged')

if __name__ == '__main__':
    m_sock_server=MiniSocketServer()
    i = 0
    while True:
        i=i+1
        m_sock_server.push_sender_queu("server sent msg: " +str(i))

        while True: 
            one_frame=m_sock_server.pop_receiver_queue()
            if(one_frame is not False): 
                print("++++ received from client data: "+str(one_frame))
            else:
                break

        time.sleep(0.01)

    sys.exit()
