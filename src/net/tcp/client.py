import random
import time
import uuid
from time import sleep

from src.conf.app_client import AppClient
from src.net.protocol.frame import Frame, FrameSequence
from src.net.protocol.ops import AnyInitiateConnection
from src.net.protocol.sender_identity import SenderIdentity
from src.net.tcp.socket import TcpSocket
from src.utils.exceptions import BreakException


class TCPClient(TcpSocket):
    """Client code goes here"""

    app_client = AppClient.parse_toml_config()

    def __init__(
            self,
            host: str = app_client.server_ip,
            port: int = app_client.server_port,
            token: str = app_client.token,
            timeout=app_client.node_timeout,
    ) -> None:
        super().__init__(host, port, timeout, server=False, client=True)

        while True:
            try:
                frame_sequence: FrameSequence = self.trx(self.s, FrameSequence(
                    Frame(AnyInitiateConnection(SenderIdentity.Client, token))
                ))
                for frame in frame_sequence.frames:
                    for proto_op in frame.operations:
                        op_type = type(proto_op)
                        if op_type is AnyInitiateConnection:
                            proto_op.check_token(self.s)
                        else:
                            self.narrator.error(f"Protocol operation not recognized: ignoring.")
            except (BreakException, EOFError):
                self.s.close()
                break
