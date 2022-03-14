#!/usr/bin/env python3

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65433  # The port used by the server

s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.setblocking(0)
data = b'foobar\n'*10*1024*1024

counter = 0
while True: 
    sentnumdata = s.send(data)
    counter = counter +1
    print("counter val: "+ str(counter)+"sent num data: " +str(sentnumdata)+ "total data: "+str(len(data)) )
