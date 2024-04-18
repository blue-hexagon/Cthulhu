import socket
import time

from _socket import SHUT_RDWR

from src.net.protocol.core.operation_abc import ProtocolOperation
from src.net.protocol.core.operation_result import OperationResult
from src.net.protocol.enums.codes import StatusCode
from src.net.protocol.enums.directionality import OperationDirectionality
from src.net.terminal.narrator import Narrator
from src.utils.exceptions import BreakException


class SleepForDuration(ProtocolOperation):
    def __init__(self, duration,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.duration = duration

    def _perform_operation(self, s: socket.socket):
        return OperationResult(
            narrator=Narrator.success,
            narrative="Slept for 10 seconds",
            status=StatusCode.SUCCESS,
            change=[(time.sleep,[self.duration])],
            result=None,
            reply=None
        )
