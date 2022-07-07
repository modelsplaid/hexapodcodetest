#!/usr/bin/env python3

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65434  # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

try:
    while True: 
        conn, addr = s.accept()
        print(f"Connected by {addr}")
        #data = conn.recv(10240)
        #while data:
            # print("redeived num data: "+str( len(data)))
            # data = conn.recv(10240)

except KeyboardInterrupt:
    s.close
