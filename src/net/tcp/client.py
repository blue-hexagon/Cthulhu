import random
import time
import uuid
from time import sleep

from src.conf.app_client import AppClient
from src.net.protocol.core.frame import FrameSequence, Frame
from src.net.protocol.enums.sender_identity import SenderIdentity
from src.net.protocol.operations.initiate_connection import AnyInitiateConnection
from src.net.protocol.operations.sleep import SleepForDuration
from src.net.protocol.operations.terminate_connection import TerminateConnection
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
                    Frame(AnyInitiateConnection(SenderIdentity.Client, token)),
                    Frame(SleepForDuration(10)),
                ))
                # for frame in frame_sequence.frames:
                #     for proto_op in frame.operations:
                #         op_type = type(proto_op)
                #         if op_type is AnyInitiateConnection:
                #             raise BreakException
                #             proto_op.execute(self.s)
                #         else:
                #             self.narrator.error(f"Protocol operation not recognized: ignoring.")
            except (BreakException, EOFError) as e:
                self.s.close()
                self.narrator.error(f"{e}")
                break
