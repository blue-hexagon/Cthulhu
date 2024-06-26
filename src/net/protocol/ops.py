import socket

from src.net.protocol.core.operation_abc import ProtocolOperation
from src.net.protocol.enums.directionality import OperationDirectionality
from src.net.protocol.operations.proxy_factory import OperationProxyFactory


class MakeAnyRepeatNextCommands(ProtocolOperation):
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

    def reply(self, s: socket.socket):
        raise NotImplementedError()

    def recieve(self):
        raise NotImplementedError()


class SubjectAsksCthulhuForPasswords(ProtocolOperation):
    """
    Direction: Node -> Cthulhu -> Node
    Node send a "im ready" request to Cthulhu, telling Cthulhu it should passwords to Node
    Cthulhu sends passwords to the node (Cthulhu chooses if it wants to use a generator for generating passwords or read passwords from a file)
    - Param amount: '<number>' | Example: '30'
    """

    def __init__(self, amount: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [
            OperationDirectionality.NodeTR,
        ]
        self.amount = amount

    def reply(self, s: socket.socket):
        raise NotImplementedError()

    def recieve(self):
        raise NotImplementedError()


class CthulhuTellsSubjectToAttack(ProtocolOperation):
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

    def reply(self, s: socket.socket):
        raise NotImplementedError()

    def recieve(self):
        raise NotImplementedError()


class CthulhuTellsNodeToStopAuthAttack(ProtocolOperation):
    """
    Direction: Cthulhu -> Node
    Instructs the node to stop the authentication attack
    - Param delay: '<number>[ms|s|m|h]' | Example: '90m'
    """

    def __init__(self, delay: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [OperationDirectionality.CthulhuFirst]
        self.delay = delay

    def reply(self, s: socket.socket):
        raise NotImplementedError()

    def recieve(self):
        raise NotImplementedError()


class MakeAnySleepForDuration(ProtocolOperation):
    """
    Direction: Cthulhu -> Node
    Make the node sleep for a duration
    - Param time: '<number>[ms|s|m|h]' | Example: '30m'
    """

    def __init__(self, time: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [OperationDirectionality.CthulhuFirst]
        self.time = time

    def reply(self, s: socket.socket):
        raise NotImplementedError()

    def recieve(self):
        raise NotImplementedError()


class CthulhuInstructsSubjectToSleepBetweenAuthAttempts(ProtocolOperation):
    """
    Direction: Cthulhu -> Node
    Makes the node sleep between requests. The duration can be fixed or a random time between an interval.
    - Param time: '<number>[ms|s|m|h]' | Example: '25ms'
    - Param time: '<number>[ms|s|m|h]-<number>[ms|s|m|h]' | Example: '10-50ms'
    """

    def __init__(self, time: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [OperationDirectionality.CthulhuFirst]
        self.time = time

    def reply(self, s: socket.socket):
        raise NotImplementedError()

    def recieve(self):
        raise NotImplementedError()


class CthulhuInstructsSubjectAboutAttackProtocol(ProtocolOperation):
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

    def reply(self, s: socket.socket):
        raise NotImplementedError()

    def recieve(self):
        raise NotImplementedError()


class CthulhuEndsSubjectConnection(ProtocolOperation):
    """
    Direction: Cthulhu -> Node
    Instructs node that cthulhu is about to close it's connection to the node # TODO: how to perform the shutdown.
    - Param None: %
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [OperationDirectionality.CthulhuFirst]

    def reply(self, s: socket.socket):
        raise NotImplementedError()

    def recieve(self):
        raise NotImplementedError()


class SubjectInformsCthulhuAboutCredentials(ProtocolOperation):
    """
    Direction: Node -> Cthulhu
    Sends authentication credentials from the Node to Cthulhu for verification.
    - Param username: Username for authentication.
    - Param password: Password for authentication.
    """

    def __init__(self, username: str, password: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [
            OperationDirectionality.NodeFirst,
        ]
        self.username = username
        self.password = password

    def reply(self, s: socket.socket):
        raise NotImplementedError()

    def recieve(self):
        raise NotImplementedError()


class AnySendsResponseCode(ProtocolOperation):
    """
    Direction: Cthulhu -> Node
    Sends a response from Cthulhu to the Node in response to a request.
    - Param response_code: Code indicating the status or outcome of the operation.
    - Param message: Optional message providing additional information.
    """

    RESPONSE_CODES = {"ACK": 100}

    def __init__(self, response_code: str, message: str = "", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [
            OperationDirectionality.CthulhuFirst,
        ]
        self.response_code = response_code
        self.message = message

    def reply(self, s: socket.socket):
        raise NotImplementedError()

    def recieve(self):
        raise NotImplementedError()


class NodeTellsCthulhuItIsAlive(ProtocolOperation):
    """
    Direction: Node -> Cthulhu
    Sends a ping message from the Node to Cthulhu to check for connectivity.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operation_directionality = [
            OperationDirectionality.NodeFirst,
        ]

    def reply(self, s: socket.socket):
        raise NotImplementedError()

    def recieve(self):
        raise NotImplementedError()


if __name__ == "__main__":
    op = OperationProxyFactory("AnyInitiateConnection", "dsakmkmdsa", "s")
    print(vars(op))
