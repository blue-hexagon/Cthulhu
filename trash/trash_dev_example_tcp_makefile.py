import socket
import sys
import time
from datetime import datetime
from time import sleep

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = sys.argv.pop() if len(sys.argv) == 3 else "127.0.0.1"
    PORT = 1060

    def print_recv(transmitter, reciever, msg):
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {transmitter} -> {reciever}]:\n{msg}')

    def print_host(host, msg):
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {host}]: {msg}')

    def send(fd, cmd):
        fd.writelines(cmd + "\n")
        fd.flush()

    def read(fd) -> str:
        msg = fd.readline()
        return msg[:-1]

    if sys.argv[1:] == ["server"]:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            print_host("Server", f"Listening at {s.getsockname()}")
            sc, sockname = s.accept()
            frw = sc.makefile("rw")

            print_host("Server", f"Accepted a connection from {sockname}")
            print_host("Server", f"Socket connects {sc.getsockname()} and {sc.getpeername()}")
            while True:
                print_recv("Client", "Server", reply := read(frw))
                if reply in [""]:
                    # if recieve FIN - how do I
                    print("Recived FIN - closing file descriptor and socket.")
                    frw.close()
                    sc.close()
                    break
                send(frw, "Hello Node!")

    elif sys.argv[1:] == ["client"]:
        s.connect((HOST, PORT))
        frw = s.makefile("rw")
        print_host("Node", f"Client has been assigned socket name {s.getsockname()}")
        while True:
            if time.localtime().tm_sec % 5 == 0:
                print_host("Node", f"Shutdown requested. Closing file descriptor, socket and exiting process..")

                s.shutdown(socket.SHUT_RDWR)
                frw.close()
                s.close()
                sys.exit(0)
            else:
                send(frw, "Hello server!")
            print_recv(s.getpeername(), "Node", read(frw))
            sleep(1)

    else:
        print(f"Usage: tcp_1.py server|client [host]")
