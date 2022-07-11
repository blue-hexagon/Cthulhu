from collections import namedtuple


class ProtocolOperation:
    def __init__(self, *args, **kwargs):
        pass


class FetchPasswords(ProtocolOperation):
    """
    Node instructs Cthulhu to feed it passwords (Cthulhu chooses if it wants to use a generator for generating passwords or read passwords from a file)
    - Param amount: '<number>' | Example: '30'
    - Param amount_range: '<number>-<number>' | Example: '10-25'
    - Direction: Node -> Cthulhu.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.amount: str
        self.amount_range: str


class NodeFireAuthAttack(ProtocolOperation):
    """
    Instructs the node to fire the authentication attack (make sure you feed it or have fed it passwords)
    - Param delay: '<number>[ms|s|m|h]' | Example: '90m'
    - Direction: Cthulhu -> Node
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delay: str


class NodeStopAuthAttack(ProtocolOperation):
    """
    Instructs the node to stop the authentication attack
    - Param delay: '<number>[ms|s|m|h]' | Example: '90m'
    - Direction: Cthulhu -> Node
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delay: str


class NodeSetSleep(ProtocolOperation):
    """
    Make the node sleep for a duration
    - Param time: '<number>[ms|s|m|h]' | Example: '30m'
    - Direction: Cthulhu -> Node
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time: str


class NodeSleepBetweenAuthAttempts(ProtocolOperation):
    """
    Makes the node sleep between requests. The duration can be fixed or a random time between an interval.
    - Param time: '<number>[ms|s|m|h]' | Example: '25ms'
    - Param time_range: '<number>[ms|s|m|h]-<number>[ms|s|m|h]' | Example: '10-50ms'
    - Direction: Cthulhu -> Node
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time: str
        self.time_range: str


class NodeSetAuthProtocol(ProtocolOperation):
    """
    Sets the protocol used for the authentication attack
    - Param protocol: Consult the readme for supported protocols. Use name convention used in readme. TODO: Make a cli arg with argparse that returns supported protocols.
    - Direction: Cthulhu -> Node
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.protocol: str
