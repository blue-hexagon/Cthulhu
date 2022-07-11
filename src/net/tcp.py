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

    def sendall(sock, message: str, operation=NodeSetSleep(time="3s")):
        message_id = FrameSegment(f"Message-ID: {22:<16}")
        operation = FrameSegment(f"Operation: {str(operation):<16}")
        message = FrameSegment(f"Message: {message:<901}")
        frame_size = FrameSegment(f"Frame-Length: {1024:<8}")

        frame_size = (
            f"Frame-Length: {message_id.segment_length + operation.segment_length + message.segment_length + frame_size.segment_length:<8}"
        )
        frame = Frame(
            frame_length=str(len(frame_size)),
            message_id=message_id.segment_string,
            operation=operation.segment_string,
            message=message.segment_string,
        )
        sock.sendall(bytes(pickle.dumps(frame)))

    def print_recv(transmitter, reciever, msg):
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {transmitter} -> {reciever}]:\n{msg}')

    def print_host(host, msg):
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {host}]: {msg}')

    def recv_all(sock, length):
        data = b""
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                raise EOFError(f"socket closed at {len(data)} bytes into a {length}-byte message")
            data += more
        return parse_message(pickle.loads(data))

    def parse_message(data):
        data = data.splitlines()
        frame_length = ""
        message_id = ""
        return data

    if sys.argv[1:] == ["server"]:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            print_host("Cthulhu", f"Listening at {s.getsockname()}")
            sc, sockname = s.accept()
            print_host("Cthulhu", f"We have accepted a connection from {sockname}")
            print_host("Cthulhu", f"Socket connects {sc.getsockname()} and {sc.getpeername()}")
            message = recv_all(sc, 1024)
            print_recv(sc.getpeername(), "Cthulhu", str(message))
            sendall(sc, "Farewell client")
            print_host("Cthulhu", "Reply sent, closing socket")
            message2 = recv_all(sc, 1024)
            sc.close()
    elif sys.argv[1:] == ["client"]:
        s.connect((HOST, PORT))
        print_host("Node", f"Client has been assigned socket name {s.getsockname()}")
        sendall(s, "Hi there, server!", NodeSetSleep(time="250ms"))
        reply = recv_all(s, 1024)
        if "Farewell client" in reply:
            print_recv("Cthulhu", s.getsockname(), str(reply))
            sendall(s, "1234567890abcdef")
            s.close()
    else:
        print(f"Usage: tcp.py server|client [host]")
