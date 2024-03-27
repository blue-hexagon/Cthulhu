import socket
from datetime import datetime

from colorama import Back, Fore

from src.net.protocol.frame import Frame, FrameSequence
from src.net.terminal.narrator import Narrator


class Formatter:
    @staticmethod
    def fprint(transmitter: str, msg: str | Frame | FrameSequence) -> None:
        info_msg = f'[{datetime.now().strftime("%H:%M:%S")} – {transmitter} -> {Formatter.get_localhost_name()}]: FrameSequence recieved'
        print(f"{Fore.LIGHTWHITE_EX}{Back.GREEN}{info_msg}".ljust(Narrator.width) + f"{Fore.RESET}{Back.RESET}")
        # print(msg)

    @staticmethod
    def get_localhost_name() -> str:
        return socket.gethostbyaddr(socket.gethostname())[0]

    @staticmethod
    def get_peer_hostname(foreign_host_addr: str) -> str:
        return socket.gethostbyaddr(foreign_host_addr)[0]

    @staticmethod
    def get_localhost_addr(sc: socket.socket) -> str:
        return f"{sc.getsockname()[0]}:{sc.getsockname()[1]}"

    @staticmethod
    def get_peer_addr(sc: socket.socket) -> str:
        return f"{sc.getpeername()[0]}:{sc.getpeername()[1]}"
