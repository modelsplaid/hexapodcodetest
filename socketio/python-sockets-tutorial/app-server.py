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


def socket_thread(name):
    print("name: "+str(name))
    try:
        while True:
            print("sel.select")
            events = sel.select(timeout=1)
            print("events:"+str(events))
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    message = key.data
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

def servo_commu_thread(name):
    while(True):
        print("running in servo commu ")
        time.sleep(1)


if __name__ == '__main__':
    print("in main")
    x = threading.Thread(target=socket_thread, args=(1,))
    x1 = threading.Thread(target=servo_commu_thread, args=(1,))
    print("x1.start()")
    x1.start()
    print("x.start()")
    x.start()
    print("x1.join")
    x1.join()
    print("x.join()")
    x.join()
