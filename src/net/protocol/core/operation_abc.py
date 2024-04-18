from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Callable, Any

from src.net.protocol.core.operation_result import OperationResult
from src.net.protocol.enums.codes import StatusCode
from src.net.protocol.enums.directionality import OperationDirectionality
from src.net.protocol.exceptions import ProtocolException
from src.net.protocol.state.server_state import ServerState
from src.net.terminal.narrator import Narrator


class ProtocolOperation(ABC):
    """
    BaseClass. Added for any future work which may benefit from
    protocol operations having inherited features.
    -
    Note:
    If adding new classes which inherits from this class:
    All operation arguments should be strings this provides the simplest interface for parsing the operations
    on the recieving end.
    """

    def __init__(self, *args, **kwargs) -> None:
        pass
        # self.operation_directionality = [OperationDirectionality.Undefined]
        self.narrator = Narrator
        # self.server_state = ServerState()
        # self.replies: bool
        # self.request_status: StatusCode

    @abstractmethod
    def _perform_operation(self, *args, **kwargs) -> OperationResult:
        pass

    def execute(self, *args, **kwargs) -> OperationResult | Tuple[None, StatusCode.code]:
        try:
            operation_result = self._perform_operation(*args, **kwargs)
            return operation_result
        except ProtocolException:
            return None, StatusCode.INTERNAL_SERVER_ERROR
