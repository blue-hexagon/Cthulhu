import socket
from abc import ABC, abstractmethod

from src.net.protocol.directionality import OperationDirectionality
from src.net.terminal.narrator import Narrator
from src.utils.singleton import Singleton


class ServerState(metaclass=Singleton):
    def __init__(self):
        self.repeat: int = -1
        self.next_n_commands: int = -1
        self.pw_cache_limit: int = -1
        self.fire_attack_delay: int = -1
        self.stop_attack: bool = False


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

    @abstractmethod
    def transmit(self, s: socket.socket):
        pass

    @abstractmethod
    def recieve(self):
        pass
