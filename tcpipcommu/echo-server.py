# echo-server.py

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65433  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("listen")
    s.listen()
    print("sccept")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:

            print("conn.recv")
            data = conn.recv(1024)
            if not data:
                print("break")
                break
            conn.sendall(data)

