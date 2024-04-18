import socket
from _socket import SHUT_RDWR

from src.net.protocol.core.operation_abc import ProtocolOperation
from src.net.protocol.enums.directionality import OperationDirectionality
from src.utils.exceptions import BreakException


class TerminateConnection(ProtocolOperation):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [
            OperationDirectionality.NodeFirst,
        ]

    def _perform_operation(self, s: socket.socket) -> None:
        s.shutdown(SHUT_RDWR)
        s.close()
        raise BreakException("Recieved TerminateConnection - terminating connection")
