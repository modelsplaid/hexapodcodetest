#!/usr/bin/env python3

import sys
import time
from libclient import MiniSocketClient
import logging

logging.basicConfig(level=logging.INFO, 
format='%(filename)s,%(funcName)s,%(lineno)d,%(name)s ,%(process)d, %(levelname)s,%(libclient_obj)s')


if __name__ == '__main__':
    m_sock_client = MiniSocketClient()

    for i in range(200):
        m_sock_client.push_sender_queu("client sent msg: " +str(i))
        while True:
            one_frame=m_sock_client.pop_receiver_queue()
            if(one_frame is not False): 
                 print("---- received from server data: "+str(one_frame))
            else: 
                break
        time.sleep(0.01)
    sys.exit()

