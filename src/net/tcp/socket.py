import pickle
import socket
import sys

from src.net.protocol.core.frame import FrameSequence
from src.net.tcp.shortcuts import Formatter
from src.net.terminal.narrator import Narrator


class TcpSocket:
    """Base class for TcpServer and TcpClient - don't instantiate, or modify - use the derived classes"""

    narrator = Narrator

    def __init__(self, host: str, port: int, timeout: int, server: bool, client: bool) -> None:
        """Setup and configure sockets"""
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.fprint = Formatter.fprint
        self.hostname = Formatter.get_localhost_name
        self.peername = Formatter.get_peer_hostname
        self.hostaddr = Formatter.get_localhost_addr
        self.peeraddr = Formatter.get_peer_addr
        if server and not client:
            self.s.settimeout(timeout)
            self.s.bind((host, port))
            self.s.listen()
            self.narrator.info(f"Role set to server")
            self.narrator.info(f"Timeout set to {timeout}")
            self.narrator.info(f"Listening at {self.hostaddr(self.s)}")
        elif client and not server:
            self.narrator.info(f"Role set to client")
            self.s.settimeout(timeout)
            self.narrator.info(f"Timeout set to {timeout}")
            try:
                self.narrator.info(f"Trying to connect to {(host, port)}")
                self.s.connect((host, port))
            except BlockingIOError:
                pass
            except ConnectionRefusedError:
                self.narrator.error(f"Connection to {self.peername(host)} refused")
                sys.exit(1)
            except TimeoutError:
                self.narrator.error("Connection timed out")
                sys.exit(1)
            else:
                self.narrator.info(f"You have been assigned socket: {self.hostaddr(self.s)}")
        else:
            raise ValueError("Client and server bool params to TcpSocket is misconfigured.")

    def accept_incoming_connection(self) -> socket.socket:
        try:
            s, sockname = self.s.accept()
            self.narrator.success(f"Recieved a connection from {self.peername(self.host)}@{self.peeraddr(s)}")
            return s
        except TimeoutError:
            self.narrator.error("Connection timed out")
            sys.exit(1)

    @classmethod
    def rx(cls, sock: socket.socket, buffer_size: int = 1024 * 8) -> FrameSequence:
        """Recieve the pickled data then unpickle it and return the unpickled (unserialized) data"""
        data = bytearray()  # TODO switch data to be type of bytes array and then join the bytesarray before deserializing (this should be faster)
        while True:
            try:
                chunk = sock.recv(buffer_size)
                data += chunk
                if len(chunk) < buffer_size:
                    break
                if not chunk:
                    raise EOFError(f"socket closed at {len(data)} bytes into a recieve call.")
            except EOFError:
                break
        deserialized_data: FrameSequence = pickle.loads(data)
        cls.narrator.debug(f"Recieved FS: {deserialized_data}")
        return deserialized_data

    @classmethod
    def tx(cls, sock: socket.socket, msg: FrameSequence) -> None:
        """Pickle the FrameSequence then send the pickle"""
        cls.narrator.debug(f"Sending FS: {msg}")
        serialized_data = pickle.dumps(msg)
        sock.sendall(serialized_data)

    @staticmethod
    def trx(sock: socket.socket, msg: FrameSequence) -> FrameSequence:
        """Transmit then recieve"""
        TcpSocket.tx(sock, msg)  # Send all
        recv = TcpSocket.rx(sock)  # Recieve all
        return recv

    @staticmethod
    def rtx(sock: socket.socket, msg: FrameSequence) -> FrameSequence:
        """Recieve then transmit"""
        recv = TcpSocket.rx(sock)  # Recieve all
        TcpSocket.tx(sock, msg)  # Send all
        return recv

    #
    @staticmethod
    def _bytes(msg: str) -> bytes:
        """Convert a string to UTF-8 encoded bytes"""
        return bytes(msg.encode("utf-8"))

    @staticmethod
    def _string(msg: bytes) -> str:
        """Convert UTF-8 encoded bytes to a string"""
        return msg.decode("utf-8")
