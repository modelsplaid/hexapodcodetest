#!/usr/bin/env python3

import sys
import time
from libclient import MiniSocketClient
import logging

user_message = ''
logging.basicConfig(level=logging.INFO, 
format='%(filename)s,%(funcName)s,%(lineno)d,%(name)s ,%(process)d, %(levelname)s,%(libclient_obj)s')


if __name__ == '__main__':
    m_sock_server = MiniSocketClient()

    for i in range(5):
        m_sock_server.push_sender_queu("hello in main")
        time.sleep(0.5)
        print("in main")
    sys.exit()

