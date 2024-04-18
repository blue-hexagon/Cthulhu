import socket
from typing import Tuple

from _socket import SHUT_RDWR

from src.conf.app_client import AppClient
from src.conf.app_server import AppServer
from src.net.protocol.core.operation_abc import ProtocolOperation, OperationResult
from src.net.protocol.enums.codes import StatusCode
from src.net.protocol.enums.directionality import OperationDirectionality
from src.net.protocol.enums.sender_identity import SenderIdentity
from src.net.terminal.narrator import Narrator
from src.utils.exceptions import BreakException


class AnyInitiateConnection(ProtocolOperation):
    def __init__(self, sender_identity: SenderIdentity, token: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [
            OperationDirectionality.NodeFirst,
        ]
        self.sender_identity = sender_identity
        self.transmitted_token = (
            token
            # This is the token that was set when the object was instantiated - i.e., the transmitted and then recieved token
            # It's transmitted "over the wire" by pickling the object instance and sending it to a reciever
        )

    def _perform_operation(self, s: socket.socket) -> OperationResult:

        # @formatter:off
        if ((self.sender_identity.matches_identity(SenderIdentity.Server) and self.transmitted_token == AppServer.parse_toml_config().token) or (self.sender_identity.matches_identity(SenderIdentity.Client)  and self.transmitted_token == AppClient.parse_toml_config().token)):

            return OperationResult(
                narrator=Narrator.success,
                narrative="Token match - authorization granted",
                status=StatusCode.OPERATION_COMPLETED,
                change=None,
                result=None,
                reply=None
            )
        else:
            def change_func():
                s.shutdown(SHUT_RDWR)
                s.close()
            return OperationResult(
                narrator=Narrator.error,
                narrative="Token mismatch - authorization denied",
                change=[(change_func,None)],
                status=StatusCode.TOKEN_MISMATCH,
                result=None,
                reply=None
            )
        # @formatter:on
