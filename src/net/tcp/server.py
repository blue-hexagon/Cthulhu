import socket
from typing import List

from src.conf.app_server import AppServer
from src.net.protocol.core.frame import FrameSequence, Frame
from src.net.protocol.core.operation_result import OperationResult
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
            operation_results: List[OperationResult] = []
            while True:  # Runs while the socket is alive
                try:
                    frame_sequence: FrameSequence = self.rx(s)  # noqa
                    for frame in frame_sequence.frames:
                        for proto_op in frame.operations:
                            op_res: OperationResult = proto_op.execute(s)
                            operation_results.append(proto_op.execute(s))
                    # self.tx(s, FrameSequence(Frame(AnyInitiateConnection(SenderIdentity.Server, token))))
                    self.iterate_futures(operation_results)
                except (BreakException, EOFError) as e:
                    break

    def iterate_futures(self, operation_results):
        for operation_result in operation_results:
            if operation_result.change is not None:
                for change_func, change_arg in operation_result.change:
                    if change_arg is not None:
                        change_func(change_arg)
                    else:
                        change_func()
            operation_result.narrate()

        for operation_result in operation_results:
            if operation_result.reply is not None:
                for reply_func, reply_arg in operation_result.reply:
                    if reply_arg is not None:
                        reply_func(reply_arg)
                    else:
                        reply_func()
