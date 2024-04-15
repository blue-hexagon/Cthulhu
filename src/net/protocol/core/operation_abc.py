from abc import ABC, abstractmethod

from src.net.protocol.enums.codes import PentestStatus, PentestError
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
        self.operation_directionality = [OperationDirectionality.Undefined]
        self.narrator = Narrator()
        self.server_state = ServerState()
        self.replies: bool
        self.success_code: PentestStatus | None = None
        self.error_code: PentestError | None = None

    def execute(self, *args, **kwargs):
        try:
            result = self._perform_operation(*args, **kwargs)
            return result, self.success_code
        except ProtocolException:
            return None, self.error_code

    @abstractmethod
    def _perform_operation(self, *args, **kwargs):
        pass


