import pickle
import socket
import sys
from datetime import datetime

from frame import Frame, FrameSequence
from protocol_operation import (
    NodeFireAuthAttack,
    NodeRecievePasswords,
    NodeSetAuthProtocol,
    NodeSetSleep,
    NodeSleepBetweenAuthAttempts,
    NodeStopAuthAttack,
    ProtocolOperation,
    RepeatNextCommands,
)


class Logger:
    def __init__(self, hostname) -> None:
        self.hostname = hostname

    def log_msg(self, info: str) -> None:
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {self.hostname}]: {info}')


class Formatter:
    @staticmethod
    def fprint(transmitter: str, msg: str | Frame | FrameSequence) -> None:
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {transmitter} -> {Formatter.get_localhost_name()}]:\n{msg}')

    @staticmethod
    def get_localhost_name() -> str:
        return socket.gethostbyaddr(socket.gethostname())[0]

    @staticmethod
    def get_peer_hostname(foreign_host_addr: str) -> str:
        return socket.gethostbyaddr(foreign_host_addr)[0]

    @staticmethod
    def get_localhost_addr(sc: socket.socket) -> str:
        return f"{sc.getsockname()[0]}:{sc.getsockname()[1]}"

    @staticmethod
    def get_peer_addr(sc) -> str:
        return f"{sc.getpeername()[0]}:{sc.getpeername()[1]}"


class TcpSocket:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def recv_all(self, sock: socket.socket, length: int = 1024 * 1024) -> str:
        data = b""
        while len(data) < length:
            try:
                more = sock.recv(length - len(data))
                if not more:
                    raise EOFError(f"socket closed at {len(data)} bytes into a {length}-byte message")
                else:
                    data += more
            except EOFError:
                break
        deserialized_data = pickle.loads(data)
        return deserialized_data

    def send_all(self, sock: socket.socket, msg: Frame | FrameSequence) -> None:
        serialized_data = pickle.dumps(msg.frames)
        sock.sendall(serialized_data)

    def _bytes(self, msg: str) -> bytes:
        return bytes(msg.encode("utf-8"))

    def _string(self, msg: bytes) -> str:
        return msg.decode("utf-8")


class TCPServer(TcpSocket):
    def __init__(self, s: socket.socket, host: str, port: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        s.bind((host, port))
        s.listen()

        log = Logger(Formatter.get_localhost_name()).log_msg
        fprint = Formatter.fprint

        log(f"Listening at {Formatter.get_localhost_addr(s)}")
        try:
            while True:
                sc: socket.socket
                sc, sockname = s.accept()
                log(f"Recieved a connection from {Formatter.get_peer_hostname(host)}@{Formatter.get_peer_addr(sc)}")
                while True:
                    frame_sequence = self.recv_all(sc)
                    fprint(Formatter.get_peer_hostname(host), frame_sequence)
                    # If type(frame_sequence[:-1].operation) == type(NodeEndConnection)
                    break
                sc.close()
        except TimeoutError:
            log("Connection timed out")
            sys.exit(0)


class TCPClient(TcpSocket):
    def __init__(self, s: socket.socket, host: str, port: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.log = Logger("Client").log_msg

        s.connect((host, port))
        self.log(f"You have been assigned socket name {Formatter.get_localhost_addr(s)}")
        packet_stream = FrameSequence(
            Frame(NodeSetSleep(time="3s")),
            Frame(NodeSetAuthProtocol(protocol="ssh")),
            Frame(RepeatNextCommands(repeat="5", next_n_commands="5")),
            Frame(NodeRecievePasswords(amount="25-100")),
            Frame(NodeFireAuthAttack(delay="10m")),
        )
        self.send_all(s, packet_stream)
        # self.send_all(s, Frame(message="", message_id="10", operation=NodeFireAuthAttack(delay="0s")))
        s.close()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(8)
    HOST_IP = "127.0.0.1"
    HOST_PORT = 1060
    REMOTE_IP = "127.0.0.1"
    REMOTE_PORT = 1060

    if sys.argv[1:] == ["server"]:
        TCPServer(s, HOST_IP, HOST_PORT)
    elif sys.argv[1:] == ["client"]:
        TCPClient(s, REMOTE_IP, REMOTE_PORT)
    else:
        print("Usage: dev.py server|client")
