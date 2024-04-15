from src.utils.singleton import Singleton


class ServerState(metaclass=Singleton):
    def __init__(self):
        self.repeat: int = -1
        self.next_n_commands: int = -1
        self.pw_cache_limit: int = -1
        self.fire_attack_delay: int = -1
        self.stop_attack: bool = False
