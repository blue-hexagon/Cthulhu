from enum import Enum


class OperationDirectionality(Enum):
    """
    Enum representing the directionality of operations in the protocol.

    Each enum member corresponds to a specific direction or mode of communication.
    The directionality can be either from Cthulhu to Node or from Node to Cthulhu.

    Members:
    - Undefined: Represents an undefined or unspecified directionality - for testing purposes only.
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

    def __str__(self) -> int:
        return self.value
