import socket
from datetime import datetime

from colorama import Back, Fore, init

from src.net.terminal.utils import TermUtils
from src.utils.singleton import Singleton


class Narrator(metaclass=Singleton):
    (width, height) = TermUtils.terminal_size()

    def __init__(self, colors: bool = True) -> None:
        # TODO: Check if can be shortened as using a singleton - should be, but test.
        __is_initialized = False

        if not __is_initialized:
            init(convert=True)
            __is_initialized = True

        if not colors:
            Fore.LIGHTWHITE_EX = ""
            Fore.YELLOW = ""
            Back.BLACK = ""
            Back.GREEN = ""
            Back.YELLOW = ""
            Back.RED = ""

    @staticmethod
    def get_message(msg: str, log_level_name_abbr: str) -> str:
        return f'[{datetime.now().strftime("%H:%M:%S")} – [{log_level_name_abbr}] – {socket.gethostname()}]: {msg}'

    @staticmethod
    def debug(msg: str) -> None:
        print(f"{Fore.BLACK}{Back.LIGHTWHITE_EX}{Narrator.get_message(msg, 'D')}".ljust(Narrator.width) + f" {Fore.RESET}{Back.RESET}")

    @staticmethod
    def info(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.BLUE}{Narrator.get_message(msg, 'I')}".ljust(Narrator.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def success(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.GREEN}{Narrator.get_message(msg, 'S')}".ljust(Narrator.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def warning(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.YELLOW}{Narrator.get_message(msg, 'W')}".ljust(Narrator.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def error(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.RED}{Narrator.get_message(msg, 'E')}".ljust(Narrator.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def critical(msg: str) -> None:
        print(
            f"{Fore.LIGHTWHITE_EX}{Back.LIGHTRED_EX}{Narrator.get_message(msg, 'C')}".ljust(Narrator.width) + f" {Fore.RESET}{Back.RESET}"
        )
