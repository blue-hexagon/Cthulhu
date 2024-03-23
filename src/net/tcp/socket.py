import pickle
import socket
import sys

from src.net.fmt import Formatter
from src.net.logger import Logger
from src.net.protocol.frame import Frame, FrameSequence
from src.net.protocol.ops import (
    CthulhuEndsSubjectConnection,
    CthulhuInstructsSubjectAboutAttackProtocol,
    CthulhuInstructsSubjectToSleepBetweenAuthAttempts,
    CthulhuTellsNodeToStopAuthAttack,
    CthulhuTellsSubjectToAttack,
    MakeAnyRepeatNextCommands,
    MakeAnySleepForDuration,
    SubjectAsksCthulhuForPasswords,
)
from src.net.util import Utils


class TcpSocket:
    def __init__(self, host: str, port: int, timeout: int, server: bool, client: bool) -> None:
        """Setup and configure sockets"""
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.log = Logger()
        self.fprint = Formatter.fprint
        self.hostname = Formatter.get_localhost_name
        self.peername = Formatter.get_peer_hostname
        self.hostaddr = Formatter.get_localhost_addr
        self.peeraddr = Formatter.get_peer_addr
        if server and not client:
            self.s.settimeout(timeout)
            self.s.bind((host, port))
            self.s.listen()
            self.log.info(f"Listening at {self.hostaddr(self.s)}")
        elif client and not server:
            self.s.settimeout(timeout)
            try:
                self.s.connect((host, port))
            except ConnectionRefusedError:
                self.log.error(f"Connection to {self.peername(host)} refused")
                sys.exit(1)
            except TimeoutError:
                self.log.error("Connection timed out")
                sys.exit(1)
            else:
                self.log.info(f"You have been assigned socket: {self.hostaddr(self.s)}")
        else:
            raise ValueError("Client and server bool params to TcpSocket is misconfigured.")

    def accept_incoming_connection(self) -> socket.socket:
        try:
            s, sockname = self.s.accept()
            self.log.success(f"Recieved a connection from {self.peername(self.host)}@{self.peeraddr(s)}")
            return s
        except TimeoutError:
            self.log.error("Connection timed out")
            sys.exit(1)

    @staticmethod
    def recv_all(sock: socket.socket, length: int = 1024 * 1024) -> str:
        """Recieve the pickled data then unpickle it and return the unpickled data"""
        data = b""  # TODO switch data to be type of bytes array and then join the bytesarray before deserializing (this should be faster)
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

    @staticmethod
    def send_all(sock: socket.socket, msg: FrameSequence) -> None:
        """Pickle the FrameSequence then send the pickle"""
        serialized_data = pickle.dumps(msg)
        sock.sendall(serialized_data)

    @staticmethod
    def trx(sock: socket.socket, msg: FrameSequence):
        """Transmit then recieve"""
        TcpSocket.send_all(sock, msg)  # Send all
        recv = TcpSocket.recv_all(sock)  # Recieve all
        return recv

    @staticmethod
    def rtx(sock: socket.socket, msg: FrameSequence):
        """Recieve then transmit"""
        recv = TcpSocket.recv_all(sock)  # Recieve all
        TcpSocket.send_all(sock, msg)  # Send all
        return recv

    @staticmethod
    def _bytes(msg: str) -> bytes:
        """Convert a string to UTF-8 encoded bytes"""
        return bytes(msg.encode("utf-8"))

    @staticmethod
    def _string(msg: bytes) -> str:
        """Convert UTF-8 encoded bytes to a string"""
        return msg.decode("utf-8")


class TCPServer(TcpSocket):
    """Server code goes here"""

    def __init__(self, host: str, port: int, timeout=0) -> None:
        self.repeat: int = -1
        self.next_n_commands: int = -1
        self.pw_cache_limit: int = -1
        self.fire_attack_delay: int = -1
        self.stop_attack: bool = False
        super().__init__(host, port, timeout, server=True, client=False)
        while True:
            s: socket.socket = self.accept_incoming_connection()
            while True:
                try:
                    frame_sequence = TcpSocket.recv_all(s)
                except EOFError:
                    break
                self.fprint(self.peername(host), frame_sequence)
                for frame in frame_sequence.frames:
                    op = frame.operation
                    op_type = type(frame.operation)
                    if op_type is MakeAnyRepeatNextCommands:
                        self.repeat = op.repeat
                        self.next_n_commands = op.next_n_commands
                        Logger.debug(f"Repeat {self.repeat} times the next {self.next_n_commands} commands.")

                    elif op_type is SubjectAsksCthulhuForPasswords:
                        self.pw_cache_limit = op.amount
                        Logger.debug(f"Password cache set to {self.pw_cache_limit}.")

                    elif op_type is CthulhuTellsSubjectToAttack:
                        self.fire_attack_delay = Utils.get_ms_delay(op.delay)
                        Logger.debug(f"Fire delay set to {op.delay}.")

                    elif op_type is CthulhuTellsNodeToStopAuthAttack:
                        self.stop_attack_delay = Utils.get_ms_delay(op.delay)
                        Logger.debug(f"Stop delay set to {op.delay}.")

                    elif op_type is MakeAnySleepForDuration:
                        print("hit")

                    elif op_type is CthulhuInstructsSubjectToSleepBetweenAuthAttempts:
                        print("hit")

                    elif op_type is CthulhuInstructsSubjectAboutAttackProtocol:
                        print("hit")

                    elif op_type is CthulhuEndsSubjectConnection:
                        print("hit")

                    else:
                        Logger.error(f"Protocol operation not recognized. Ignoring: {op}.")
            s.close()


class TCPClient(TcpSocket):
    """Client code goes here"""

    PAYLOAD = [
        FrameSequence(
            Frame(AnyInitiateConnection()),
        ),
        FrameSequence(
            Frame(MakeAnySleepForDuration(time="3s")),
            Frame(CthulhuInstructsSubjectAboutAttackProtocol(protocol="ssh")),
            Frame(MakeAnyRepeatNextCommands(repeat="5", next_n_commands="5")),
            Frame(SubjectAsksCthulhuForPasswords(amount="25-100")),
            Frame(CthulhuTellsSubjectToAttack(delay="10m")),
        ),
        FrameSequence(
            Frame(MakeAnySleepForDuration(time="3s")),
        ),
        FrameSequence(
            Frame(CthulhuEndsSubjectConnection()),
        ),
    ]

    def __init__(self, host: str, port: int, timeout=0) -> None:
        super().__init__(host, port, timeout, server=False, client=True)
        packet_stream = TCPClient.PAYLOAD
        while True:
            TcpSocket.send_all(self.s, packet_stream)
            # Formatter.fprint(self.peername(host), self.recv_all(s))
            break
        self.s.close()
