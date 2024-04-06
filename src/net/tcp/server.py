import socket

from src.conf.app_server import AppServer
from src.net.protocol.frame import FrameSequence
from src.net.protocol.operation import ProtocolOperation
from src.net.protocol.ops import AnyInitiateConnection, CthulhuEndsSubjectConnection
from src.net.tcp.socket import TcpSocket
from src.utils.exceptions import BreakException
from src.utils.singleton import Singleton


class TCPServer(TcpSocket):
    """Server code goes here"""

    server_conf = AppServer.parse_toml_config()

    def __init__(
        self,
        host: str = server_conf.server_ip,
        port: int = server_conf.server_port,
        token: str = server_conf.token,
        timeout=server_conf.server_timeout,
    ) -> None:
        super().__init__(host, port, timeout, server=True, client=False)
        while True:  # Runs until timeout if no incoming connections, then exits when timeout reached.
            s: socket.socket = self.accept_incoming_connection()
            while True:  # Runs while the socket is alive
                try:
                    frame_sequence: FrameSequence = TcpSocket.recv_all(s)  # noqa
                    for frame in frame_sequence.frames:
                        op: ProtocolOperation = frame.operation
                        op_type = type(frame.operation)
                        if op_type is AnyInitiateConnection:
                            op.check_token(s)
                            # op.transmit(s)  # s.send(CthulhuEndsSubjectConnection())
                        else:
                            self.narrator.error(f"Protocol operation not recognized: ignoring.")
                except (BreakException, EOFError):
                    break
