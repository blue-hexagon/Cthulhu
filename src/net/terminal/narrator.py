import socket
from datetime import datetime

from colorama import Back, Fore

from src.net.terminal.utils import TermUtils


class Narrator:
    (width, height) = TermUtils.terminal_size()

    def __init__(self, colors: bool = True) -> None:
        if not colors:
            Fore.LIGHTWHITE_EX = ""
            Fore.YELLOW = ""
            Back.BLACK = ""
            Back.GREEN = ""
            Back.YELLOW = ""
            Back.RED = ""

    @staticmethod
    def get_message(msg: str):
        return f'[{datetime.now().strftime("%H:%M:%S")} – {socket.gethostname()}]: {msg}'

    @staticmethod
    def debug(msg: str) -> None:
        print(f"{Fore.BLACK}{Back.LIGHTWHITE_EX}{Narrator.get_message(msg)}".ljust(
            Narrator.width) + f" {Fore.RESET}{Back.RESET}")

    @staticmethod
    def info(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.BLUE}{Narrator.get_message(msg)}".ljust(
            Narrator.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def success(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.GREEN}{Narrator.get_message(msg)}".ljust(
            Narrator.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def warning(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.YELLOW}{Narrator.get_message(msg)}".ljust(
            Narrator.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def error(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.RED}{Narrator.get_message(msg)}".ljust(
            Narrator.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def critical(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.LIGHTRED_EX}{Narrator.get_message(msg)}".ljust(Narrator.width) + f" {Fore.RESET}{Back.RESET}")

if __name__ == '__main__':
    Narrator.debug("Debussg msg")
    Narrator.debug("Debug msg")
    Narrator.info("Info msg")
    Narrator.success("Success msg")
    Narrator.warning("Warning msg")
    Narrator.error("Error msg")
    Narrator.critical("Critical msg")
