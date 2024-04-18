import socket
from datetime import datetime

from colorama import Back, Fore, init

from src.net.terminal.utils import TermUtils
from src.utils.singleton import Singleton


class Narrator:
    def __new__(cls, *args, **kwargs):
        raise RuntimeError()

    @staticmethod
    def debug(msg: str, status_code=None) -> None:
        print(Narrative.debug(msg, status_code))

    @staticmethod
    def info(msg: str, status_code=None) -> None:
        print(Narrative.info(msg, status_code))

    @staticmethod
    def success(msg: str, status_code=None) -> None:
        print(Narrative.success(msg, status_code))

    @staticmethod
    def warning(msg: str, status_code=None) -> None:
        print(Narrative.warning(msg, status_code))

    @staticmethod
    def error(msg: str, status_code=None) -> None:
        print(Narrative.error(msg, status_code))

    @staticmethod
    def critical(msg: str, status_code=None) -> None:
        print(Narrative.critical(msg, status_code))


class Narrative(metaclass=Singleton):
    (width, height) = TermUtils().terminal_size()

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
    def get_message(msg: str, log_level_name_abbr: str, status_code: str) -> str:
        # @formatter:off
        _ = ""
        if status_code:
            prefix = f'[{datetime.now().strftime("%H:%M:%S")}{_}–{_}[{log_level_name_abbr}{_}-{_}{status_code}]{_}–{_}{socket.gethostname()}]:'
        else:
            prefix = f'[{datetime.now().strftime("%H:%M:%S")}{_}–{_}[{log_level_name_abbr}{_}-{_}000]{_}–{_}{socket.gethostname()}]:'
        print_str = f"{prefix} {msg}".ljust(Narrative.width, "\u2002")
        return print_str
        # @formatter:on

    @staticmethod
    def debug(msg: str, status_code) -> str:
        return (f"{Fore.BLACK}{Back.LIGHTWHITE_EX}{Narrative.get_message(msg, 'D', status_code)}".ljust(
            Narrative.width) + f" {Fore.RESET}{Back.RESET}")

    @staticmethod
    def info(msg: str, status_code) -> str:
        return (f"{Fore.LIGHTWHITE_EX}{Back.BLUE}{Narrative.get_message(msg, 'I', status_code)}".ljust(
            Narrative.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def success(msg: str, status_code) -> str:
        return (f"{Fore.LIGHTWHITE_EX}{Back.GREEN}{Narrative.get_message(msg, 'S', status_code)}".ljust(
            Narrative.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def warning(msg: str, status_code) -> str:
        return (f"{Fore.LIGHTWHITE_EX}{Back.YELLOW}{Narrative.get_message(msg, 'W', status_code)}".ljust(
            Narrative.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def error(msg: str, status_code) -> str:
        return (f"{Fore.LIGHTWHITE_EX}{Back.RED}{Narrative.get_message(msg, 'E', status_code)}".ljust(
            Narrative.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def critical(msg: str, status_code) -> str:
        return (
                f"{Fore.LIGHTWHITE_EX}{Back.LIGHTRED_EX}{Narrative.get_message(msg, 'C', status_code)}".ljust(
                    Narrative.width) + f" {Fore.RESET}{Back.RESET}"
        )
