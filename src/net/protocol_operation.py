from inspect import isclass


class ProtocolOperation:
    """
    BaseClass. Added for any future work which may benefit from
    protocol operations having inherited features.
    -
    Note:
    If adding new classes which inherits from this class:
    All operation arguments should be strings
    this provides the simplest interface for parsing the operations
    on the recieving end.
    """

    def __init__(self, *args, **kwargs) -> None:
        pass


class RepeatNextCommands(ProtocolOperation):
    """
    Instructs the reciever to repeat the next x operation commands y times
    - Param repeat_n_times: '<number>' | Example: '5'
    - Param repeat: '<number>' | Example: '3'
    - Direction: Node -> Cthulhu.
    """

    def __init__(self, /, repeat: str, next_n_commands: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.repeat = repeat
        self.next_n_commands = next_n_commands


class NodeRecievePasswords(ProtocolOperation):
    """
    Cthulhu sends passwords to the node (Cthulhu chooses if it wants to use a generator for generating passwords or read passwords from a file)
    - Param amount: '<number>' | Example: '30'
    - Param amount: '<number>-<number>' | Example: '10-25'
    - Direction: Node -> Cthulhu.
    """

    def __init__(self, amount: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.amount = amount


class NodeFireAuthAttack(ProtocolOperation):
    """
    Instructs the node to fire the authentication attack (make sure you feed it or have fed it passwords)
    - Param delay: '<number>[ms|s|m|h]' | Example: '90m'
    - Direction: Cthulhu -> Node
    """

    def __init__(self, delay: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.delay = delay


class NodeStopAuthAttack(ProtocolOperation):
    """
    Instructs the node to stop the authentication attack
    - Param delay: '<number>[ms|s|m|h]' | Example: '90m'
    - Direction: Cthulhu -> Node
    """

    def __init__(self, delay: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.delay = delay


class NodeSetSleep(ProtocolOperation):
    """
    Make the node sleep for a duration
    - Param time: '<number>[ms|s|m|h]' | Example: '30m'
    - Direction: Cthulhu -> Node
    """

    def __init__(self, time: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.time = time


class NodeSleepBetweenAuthAttempts(ProtocolOperation):
    """
    Makes the node sleep between requests. The duration can be fixed or a random time between an interval.
    - Param time: '<number>[ms|s|m|h]' | Example: '25ms'
    - Param time: '<number>[ms|s|m|h]-<number>[ms|s|m|h]' | Example: '10-50ms'
    - Direction: Cthulhu -> Node
    """

    def __init__(self, time: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.time = time


class NodeSetAuthProtocol(ProtocolOperation):
    """
    Sets the protocol used for the authentication attack
    - Param protocol: Consult the readme for supported protocols. Use name convention used in readme.
    - Direction: Cthulhu -> Node
    """

    def __init__(self, protocol: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.protocol = protocol


class NodeEndConnection(ProtocolOperation):
    """
    Instructs node that cthulhu has closed it's connection to the node
    - Param None: %
    - Direction: Cthulhu -> Node
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class Help:
    @staticmethod
    def print():
        """Prints the classname followed by the docstring for all ProtocolOperations in this file"""
        class_list = list({element_name: element for element_name, element in globals().items() if isclass(element)})
        class_list.remove("ProtocolOperation")
        class_list.remove("Help")
        for name in class_list:
            print(name + eval(name).__doc__)
