import math
import pickle
import random
import socket
import sys
from datetime import datetime

from frame import Frame, FrameSegment
from protocol_operation import *

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = sys.argv.pop() if len(sys.argv) == 3 else "127.0.0.1"
    PORT = 1060
    message_id_seed = 20

    def print_recv(transmitter, reciever, msg):
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {transmitter} -> {reciever}]:\n{msg}')

    def print_host(host, msg):
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {host}]: {msg}')

    def send_all(sock, message: str, operation=NodeSetSleep(time="3s")):
        message_id = FrameSegment(f"Message-ID: {22:<16}")
        operation = FrameSegment(f"Operation: {str(operation):<16}")
        message = FrameSegment(f"Message: {message}")

        frame = Frame(
            message_id=message_id.segment_string,
            operation=operation.segment_string,
            message=message.segment_string,
        )
        frame_length = len(f.encode("utf-8"))
        frame = str(f"{frame_length:<4}{frame}").encode("utf-8")
        frame = pickle.dumps(frame)
        # frame = frame[2:]
        # frame =  frame[:-1]
        print("-" * 20)
        print(len(pickle.dumps(frame)))
        print(frame)
        print("-" * 20)

        frame = bytes(frame)
        sock.sendall(frame)

    def recv_all(sock) -> bytes:
        data = b""  # TODO: Increasing a bytes object is not very performant, better to store the parts in an array and do: b"".join(data) when data is fully transmitted.
        length = int(sock.recv(4))
        print("+" * 20)
        print("Frame-Size:'" + str(length) + "'")
        print("+" * 20)

        while len(data) < length:

            more = sock.recv(length - len(data))
            if not more:
                print("-" * 15 + " EOF " + "-" * 15)
                break
                raise EOFError(f"socket closed at {len(data)} bytes into a {length}-byte message")
            data += more
        print("*" * 20)
        print(data)
        print(pickle.loads(data))
        print("*" * 20)
        deserialized_data = pickle.loads(data)

        return deserialized_data

    def parse_message(data: bytes):
        frame_length = ""
        message_id = ""
        deserialized_data = pickle.loads(data)
        return deserialized_data

    if sys.argv[1:] == ["server"]:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            print_host("Cthulhu", f"Listening at {s.getsockname()}")
            sc, sockname = s.accept()
            print_host("Cthulhu", f"We have accepted a connection from {sockname}")
            print_host("Cthulhu", f"Socket connects {sc.getsockname()} and {sc.getpeername()}")
            message = recv_all(sc)
            print_recv(sc.getpeername(), "Cthulhu", str(message))
            send_all(sc, "Farewell client")
            print_host("Cthulhu", "Reply sent, closing socket")
            message2 = recv_all(sc)
            sc.close()
    elif sys.argv[1:] == ["client"]:
        s.connect((HOST, PORT))
        print_host("Node", f"Client has been assigned socket name {s.getsockname()}")
        send_all(s, "Hi there, server!", NodeSetSleep(time="250ms"))
        reply = recv_all(s)
        if b"Farewell client" in reply:
            print_recv("Cthulhu", s.getsockname(), str(reply))
            send_all(s, "1234567890abcdef")
            s.close()
    else:
        print(f"Usage: tcp.py server|client [host]")
