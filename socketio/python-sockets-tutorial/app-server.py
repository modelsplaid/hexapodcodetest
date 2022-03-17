#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback
import libserver
import time

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)
    return message

    
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

print("lsock: "+str(lsock) )
registerkey = sel.register(lsock, selectors.EVENT_READ, data=None)


messageobjs = []
try:
    while True:
        #print("in sel.select")
        events = sel.select(timeout=None)
        #print("out sel.select")
        for key, mask in events:
            if key.data is None:
                print("key.fileobj: "+str(key.fileobj))
                print("key: "+str(key))
                messageobj=accept_wrapper(key.fileobj)
                while(True):
                    print("sending data ...")
                    messageobj.send_servo_data()
                    time.sleep(0.5)

            else:
                print("key.data is not none")


except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()



'''
try:
    while True:
        #print("in sel.select")
        events = sel.select(timeout=None)
        #print("out sel.select")
        #sel.get_key()
        for key, mask in events:
            if key.data is None:
                print("key.fileobj: "+str(key.fileobj))
                print("key: "+str(key))
                accept_wrapper(key.fileobj)
            else:
                messagekey = registerkey
                message = key.data

                print("messagekey: "+str(messagekey))
                print("message: "+str(message))
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        f"Main: Error: Exception for {message.addr}:\n"
                        f"{traceback.format_exc()}"
                    )
                    message.close()
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
'''