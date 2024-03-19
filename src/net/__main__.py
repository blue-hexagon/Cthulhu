import os
import pickle
import re
import socket
import sys
from datetime import datetime

from colorama import Back, Fore
from frame import Frame, FrameSequence
from protocol_operation import (
    NodeFireAuthAttack,
    NodeRecievePasswords,
    NodeSetAuthProtocol,
    NodeSetSleep,
    NodeSleepBetweenAuthAttempts,
    NodeStopAuthAttack,
    ProtocolOperation,
    RepeatNextCommands, NodeEndConnection,
)


class Logger:
    width = os.get_terminal_size().columns

    def __init__(self, colors: bool = True) -> None:
        if not colors:
            Fore.LIGHTWHITE_EX = ""
            Fore.YELLOW = ""
            Back.BLACK = ""
            Back.GREEN = ""
            Back.YELLOW = ""
            Back.RED = ""

    @staticmethod
    def get_message(msg: str):
        return f'[{datetime.now().strftime("%H:%M:%S")} – {socket.gethostname()}]: {msg}'

    @staticmethod
    def debug(msg: str) -> None:
        print(f"{Fore.BLACK}{Back.LIGHTWHITE_EX}{Logger.get_message(msg)}".ljust(
            Logger.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def info(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.BLUE}{Logger.get_message(msg)}".ljust(
            Logger.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def success(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.GREEN}{Logger.get_message(msg)}".ljust(
            Logger.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def warning(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.YELLOW}{Logger.get_message(msg)}".ljust(
            Logger.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def error(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.RED}{Logger.get_message(msg)}".ljust(
            Logger.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def critical(msg: str) -> None:
        print(f"{Fore.YELLOW}{Back.RED}{Logger.get_message(msg)}".ljust(Logger.width) + f"{Fore.RESET}{Back.RESET}")


class Formatter:
    @staticmethod
    def fprint(transmitter: str, msg: str | Frame | FrameSequence) -> None:
        info_msg = f'[{datetime.now().strftime("%H:%M:%S")} – {transmitter} -> {Formatter.get_localhost_name()}]: FrameSequence recieved'
        print(f"{Fore.LIGHTWHITE_EX}{Back.GREEN}{info_msg}".ljust(Logger.width) + f"{Fore.RESET}{Back.RESET}")
        print(msg)

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
    def get_peer_addr(sc: socket.socket) -> str:
        return f"{sc.getpeername()[0]}:{sc.getpeername()[1]}"


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


class Utils():
    @staticmethod
    def get_ms_delay(delay):
        delay_int = re.sub("[^0-9]", "", delay)
        if delay.find("ms"):
            return delay
        elif delay.find("s"):
            return str(int(delay_int) * 1000)
        elif delay.find("m"):
            return str(int(delay_int) * 1000 * 60)
        elif delay.find("h"):
            return str(int(delay_int) * 1000 * 60 * 60)
        raise ValueError("Wrong attack delay specified. Param delay: '<number>[ms|s|m|h]' | Example: '90m'")


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
                    if type(frame.operation) is RepeatNextCommands:
                        self.repeat = op.repeat
                        self.next_n_commands = op.next_n_commands
                        Logger.debug(f"Repeat {self.repeat} times the next {self.next_n_commands} commands.")

                    elif type(frame.operation) is NodeRecievePasswords:
                        self.pw_cache_limit = op.amount
                        Logger.debug(f"Password cache set to {self.pw_cache_limit}.")

                    elif type(frame.operation) is NodeFireAuthAttack:
                        self.fire_attack_delay = Utils.get_ms_delay(op.delay)
                        Logger.debug(f"Fire delay set to {op.delay}.")

                    elif type(frame.operation) is NodeStopAuthAttack:
                        self.stop_attack_delay = Utils.get_ms_delay(op.delay)
                        Logger.debug(f"Stop delay set to {op.delay}.")

                    elif type(frame.operation) is NodeSetSleep:
                        print("hit")

                    elif type(frame.operation) is NodeSleepBetweenAuthAttempts:
                        print("hit")

                    elif type(frame.operation) is NodeSetAuthProtocol:
                        print("hit")

                    elif type(frame.operation) is NodeEndConnection:
                        print("hit")

                    else:
                        Logger.error(f"Protocol operation not recognized. Ignoring: {op}.")

                # If type(frame_sequence[:-1].operation) == type(NodeEndConnection)
            s.close()


class TCPClient(TcpSocket):
    """Client code goes here"""

    def __init__(self, host: str, port: int, timeout=0) -> None:
        super().__init__(host, port, timeout, server=False, client=True)
        packet_stream = FrameSequence(
            Frame(NodeSetSleep(time="3s")),
            Frame(NodeSetAuthProtocol(protocol="ssh")),
            Frame(RepeatNextCommands(repeat="5", next_n_commands="5")),
            Frame(NodeRecievePasswords(amount="25-100")),
            Frame(NodeFireAuthAttack(delay="10m")),
        )
        while True:
            TcpSocket.send_all(self.s, packet_stream)
            # Formatter.fprint(self.peername(host), self.recv_all(s))
            break
        self.s.close()


if __name__ == "__main__":
    """Set addresses and ports for the server and client"""
    HOST_IP = "127.0.0.1"
    HOST_PORT = 1060
    REMOTE_IP = "127.0.0.1"
    REMOTE_PORT = 1060

    """ Run either the server or client """
    if sys.argv[1:] == ["server"]:
        TCPServer(HOST_IP, HOST_PORT, timeout=8)
    elif sys.argv[1:] == ["client"]:
        TCPClient(REMOTE_IP, REMOTE_PORT, timeout=8)
    else:
        print("Usage: dev.py server|client")
