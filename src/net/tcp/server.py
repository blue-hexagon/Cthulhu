import socket

from src.conf.app_server import AppServer
from src.net.protocol.core.frame import FrameSequence, Frame
from src.net.protocol.enums.sender_identity import SenderIdentity
from src.net.protocol.operations.initiate_connection import AnyInitiateConnection
from src.net.tcp.socket import TcpSocket
from src.utils.exceptions import BreakException


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
                    frame_sequence: FrameSequence = self.rx(s)  # noqa
                    for frame in frame_sequence.frames:
                        for proto_op in frame.operations:
                            (res, status) = proto_op.execute(s)
                            if res is None:
                                self.narrator.error(f"{status}")
                            else:
                                self.narrator.success(f"{res}")
                    self.tx(s, FrameSequence(Frame(AnyInitiateConnection(SenderIdentity.Server, token))))
                except (BreakException, EOFError):
                    break
