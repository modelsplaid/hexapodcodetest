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
        time.sleep(0.01)
    sys.exit()

