from abc import ABC, abstractmethod

from src.net.protocol.directionality import OperationDirectionality
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

    @abstractmethod
    def transmit(self):
        pass

    @abstractmethod
    def recieve(self):
        pass
