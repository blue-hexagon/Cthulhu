import socket
from _socket import SHUT_RDWR

from src.conf.app_client import AppClient
from src.conf.app_server import AppServer
from src.net.protocol.core.operation_abc import ProtocolOperation
from src.net.protocol.core.operation_result import TrueResult
from src.net.protocol.enums.directionality import OperationDirectionality
from src.net.protocol.enums.sender_identity import SenderIdentity
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

    def _perform_operation(self, s: socket.socket) -> None:
        # @formatter:off
        if self.sender_identity.matches_identity(SenderIdentity.Server) and self.transmitted_token == AppServer.parse_toml_config().token:
            self.narrator.success("[SenderIdentity.Server] Token match - authorization granted")
            return TrueResult
        elif self.sender_identity.matches_identity(SenderIdentity.Client) and self.transmitted_token == AppClient.parse_toml_config().token:
            self.narrator.success("[SenderIdentity.Client] Token match - authorization granted")
            return TrueResult
        else:
            self.narrator.error("Token mismatch - socket shutdown and close")
            s.shutdown(SHUT_RDWR)
            s.close()
            raise BreakException()
        # @formatter:on
