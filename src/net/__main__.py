import pickle
import socket
import sys
from datetime import datetime

from frame import Frame, FrameSegment
from protocol_operation import (
    FetchPasswords,
    NodeFireAuthAttack,
    NodeSetAuthProtocol,
    NodeSetSleep,
    NodeSleepBetweenAuthAttempts,
    NodeStopAuthAttack,
    ProtocolOperation,
)


class Logger:
    def __init__(self, hostname):
        self.hostname = hostname

    def log_msg(self, info):
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {self.hostname}]: {info}')


class Formatter:
    def __init__(self, hostname):
        self.hostname = hostname

    def fprint(self, transmitter, msg):
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {transmitter} -> {self.hostname}]:\n{msg}')

    def sock_addr_format(self, sc):
        return f"{sc.getsockname()[0]}:{sc.getsockname()[1]}"

    def sock_peer_format(self, sc):
        return f"{sc.getpeername()[0]}:{sc.getpeername()[1]}"


class TcpSocket:
    def __init__(self):
        pass

    def recv_all(self, sock, length=1024 * 10) -> str:
        data = b""
        while len(data) < length:
            more = sock.recv(length - len(data))
            if (
                not more
            ):  # Alternatively an EOFError could be raised but this would beget a lot of try catch clauses and some rewriting of this method.
                break
            data += more
        deserialized_data = pickle.loads(data)
        return deserialized_data

    def send_all(self, sock: socket.socket, msg) -> None:
        serialized_data = pickle.dumps(msg)
        sock.sendall(serialized_data)

    def _bytes(self, msg: str):
        return bytes(msg.encode("utf-8"))

    def _string(self, msg: bytes):
        return msg.decode("utf-8")


class TCPServer(TcpSocket):
    def __init__(self, s, host, port):
        super().__init__()
        log = Logger("Server").log_msg
        fmt = Formatter("Client")
        fprint = fmt.fprint

        s.bind((host, port))
        s.listen()
        log(f"Listening at {fmt.sock_addr_format(s)}")
        while True:
            sc, sockname = s.accept()
            log(f"server@{fmt.sock_addr_format(sc)} connected with client@{fmt.sock_peer_format(sc)}")
            message = self.recv_all(sc)
            fprint("Client", message)

            sc.close()


class TCPClient(TcpSocket):
    def __init__(self, s, host, port):
        super().__init__()
        log = Logger("Client").log_msg
        fmt = Formatter("Server")
        fprint = fmt.fprint

        s.connect((host, port))
        log(f"You have been assigned socket name {fmt.sock_addr_format(s)}")
        self.send_all(s, Frame(message="Hello from Client!", message_id="10", operation=NodeSetSleep(time="3s")))
        self.send_all(s, Frame(message="", message_id="10", operation=NodeFireAuthAttack(delay="0s")))
        s.close()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = sys.argv.pop() if len(sys.argv) == 3 else "127.0.0.1"
    PORT = 1060

    if sys.argv[1:] == ["server"]:
        TCPServer(s, HOST, PORT)
    elif sys.argv[1:] == ["client"]:
        TCPClient(s, HOST, PORT)
    else:
        print("Usage: dev.py server|client")
