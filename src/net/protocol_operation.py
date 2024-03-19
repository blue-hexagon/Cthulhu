import re
from enum import Enum
from inspect import isclass
from typing import List


class OperationDirectionality(Enum):
    """
    Enum representing the directionality of operations in the protocol.

    Each enum member corresponds to a specific direction or mode of communication.
    The directionality can be either from Cthulhu to Node or from Node to Cthulhu.

    Members:
    - Undefined: Represents an undefined or unspecified directionality.
    - CthulhuTX: Represents transmission from Cthulhu to Node.
    - CthulhuRX: Represents reception from Cthulhu to Node.
    - CthulhuTRX: Represents bidirectional communication between Cthulhu and Node with Cthulhu speaking and then responding.
    - CthulhuRTX: Represents bidirectional communication between Cthulhu and Node with Cthulhu responding and then speaking.
    - NodeTX: Represents transmission from Node to Cthulhu.
    - NodeRX: Represents reception from Node to Cthulhu.
    - NodeTRX: Represents bidirectional communication between Node and Cthulhu with Node speaking and then responding..
    - NodeRTX: Represents bidirectional communication between Node and Cthulhu with Node responding and then speaking.
    """  # noqa: E501
    Undefined = -1
    CthulhuT = 1
    CthulhuR = 3
    CthulhuTR = 5
    CthulhuRT = 7
    CthulhuAnyT = 9
    CthulhuAnyR = 11
    CthulhuFirst = 13
    CthulhuAny = 15
    NodeT = 2
    NodeR = 4
    NodeTR = 6
    NodeRT = 8
    NodeAnyT = 10
    NodeAnyR = 12
    NodeFirst = 14
    NodeAny = 16

    def __str__(self):
        return self.value


class ProtocolOperation:
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
        self.operation_directionality = [
            OperationDirectionality.Undefined
        ]
        self.catalog_ref = ProtocolOperationsCatalog()
        self.catalog_ref.register_protocol_operation(self)


class ProtocolOperationsCatalog:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProtocolOperationsCatalog, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.catalog: List[ProtocolOperation] = list()

    def register_protocol_operation(self, operation: ProtocolOperation):
        self.catalog.append(operation)

    def build_catalog(self):
        for operation in self.catalog:
            operation()


class RepeatNextCommands(ProtocolOperation):
    """
    Direction: Node -> Cthulhu.
    Instructs the reciever to repeat the next x operation commands y times
    - Param repeat_n_times: '<number>' | Example: '5'
    - Param repeat: '<number>' | Example: '3'
    """

    def __init__(self, /, repeat: str, next_n_commands: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [
            OperationDirectionality.CthulhuFirst,
        ]
        self.repeat = repeat
        self.next_n_commands = next_n_commands


class NodeRecievePasswords(ProtocolOperation):
    """
    Direction: Node -> Cthulhu.
    Cthulhu sends passwords to the node (Cthulhu chooses if it wants to use a generator for generating passwords or read passwords from a file)
    - Param amount: '<number>' | Example: '30'
    """

    def __init__(self, amount: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [
            OperationDirectionality.NodeFirst,
        ]
        self.amount = amount


class NodeFireAuthAttack(ProtocolOperation):
    """
    Direction: Cthulhu -> Node
    Instructs the node to fire the authentication attack (make sure you feed it or have fed it passwords)
    - Param delay: '<number>[ms|s|m|h]' | Example: '90m'
      Defaults to ms if no time specifier [ms|s|m|h] is added.
    """

    def __init__(self, delay: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [
            OperationDirectionality.CthulhuFirst,
        ]
        self.delay = delay




class NodeStopAuthAttack(ProtocolOperation):
    """
    Direction: Cthulhu -> Node
    Instructs the node to stop the authentication attack
    - Param delay: '<number>[ms|s|m|h]' | Example: '90m'
    """

    def __init__(self, delay: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [
            OperationDirectionality.CthulhuFirst
        ]
        self.delay = delay


class NodeSetSleep(ProtocolOperation):
    """
    Direction: Cthulhu -> Node
    Make the node sleep for a duration
    - Param time: '<number>[ms|s|m|h]' | Example: '30m'
    """

    def __init__(self, time: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [
            OperationDirectionality.CthulhuFirst
        ]
        self.time = time


class NodeSleepBetweenAuthAttempts(ProtocolOperation):
    """
    Direction: Cthulhu -> Node
    Makes the node sleep between requests. The duration can be fixed or a random time between an interval.
    - Param time: '<number>[ms|s|m|h]' | Example: '25ms'
    - Param time: '<number>[ms|s|m|h]-<number>[ms|s|m|h]' | Example: '10-50ms'
    """

    def __init__(self, time: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [
            OperationDirectionality.CthulhuFirst
        ]
        self.time = time


class NodeSetAuthProtocol(ProtocolOperation):
    """
    Direction: Cthulhu -> Node
    Sets the protocol used for the authentication attack
    - Param protocol: Consult the readme for supported protocols. Use name convention used in readme.
    """

    def __init__(self, protocol: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [
            OperationDirectionality.CthulhuFirst,
        ]
        self.protocol = protocol


class NodeEndConnection(ProtocolOperation):
    """
    Direction: Cthulhu -> Node
    Instructs node that cthulhu is about to close it's connection to the node # TODO: how to perform the shutdown.
    - Param None: %
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [
            OperationDirectionality.CthulhuFirst
        ]


class Help:
    @staticmethod
    def print():
        """ Prints the classname followed by the docstring for all ProtocolOperations in this file """
        class_list = list({element_name: element for element_name, element in globals().items() if isclass(element)})
        class_list.remove("Help")
        class_list.remove("Enum")
        for name in class_list:
            try:
                print(name + eval(name).__doc__)
            except TypeError:
                print(name)


if __name__ == '__main__':
    Help.print()
