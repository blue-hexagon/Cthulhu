import os
import socket
from datetime import datetime

from colorama import Back, Fore


class Logger:
    width = os.get_terminal_size().columns

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
        print(f"{Fore.BLACK}{Back.LIGHTWHITE_EX}{Logger.get_message(msg)}".ljust(Logger.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def info(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.BLUE}{Logger.get_message(msg)}".ljust(Logger.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def success(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.GREEN}{Logger.get_message(msg)}".ljust(Logger.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def warning(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.YELLOW}{Logger.get_message(msg)}".ljust(Logger.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def error(msg: str) -> None:
        print(f"{Fore.LIGHTWHITE_EX}{Back.RED}{Logger.get_message(msg)}".ljust(Logger.width) + f"{Fore.RESET}{Back.RESET}")

    @staticmethod
    def critical(msg: str) -> None:
        print(f"{Fore.YELLOW}{Back.RED}{Logger.get_message(msg)}".ljust(Logger.width) + f"{Fore.RESET}{Back.RESET}")
