from src.utils.singleton import Singleton


class ConnectionState(metaclass=Singleton):
    def __init__(self):
        connection_has_been_initiated_from_this_end: bool
        connection_has_initiated_on_both_ends: bool
        connection_has_been_terminated_from_this_end: bool
        connection_has_been_terminated_on_both_ends: bool
