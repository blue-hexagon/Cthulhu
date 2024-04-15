import argparse
import subprocess
import threading
from typing import Callable

from src.net.banner import Banner
from src.net.protocol.frame import Frame, FrameSequence
from src.net.protocol.ops import AnyInitiateConnection
from src.net.tcp.c2 import socksrv
from src.net.tcp.c2.socksrv import CnC, RatServer
from src.net.tcp.client import TCPClient
from src.net.tcp.server import TCPServer
from src.passgen.util import generate_password


class Parser:
    def __init__(self, *args) -> None:
        """Takes an optional args string (not a list og strings!)"""
        self.args = args
        self.match_found = False
        self.parser = argparse.ArgumentParser(
            prog="Cthulhu",
            description="Cthulhu is a password generator and distributed task runner (and a network protocol) for using thc-hydra in a distributed manner",
            epilog="https://github.com/blue-hexagon/Cthulhu",
        )  # noqa
        # @formatter:off
        subparsers = self.parser.add_subparsers(dest="command", help="Subcommand to execute")
        token_parser = subparsers.add_parser("token", help="Generate a token for authentication between server and clients")  # noqa
        client_parser = subparsers.add_parser("client", help="Start a client instance")
        server_parser = subparsers.add_parser("server", help="Start a server instance")
        ratclient_parser = subparsers.add_parser("ratclient", help="Start a ratclient instance")
        ratserver_parser = subparsers.add_parser("ratserver", help="Start a ratserver instance")
        # @formatter:on

    def interpret(self) -> None:
        args = self.parser.parse_args(self.args if self.args else None)
        self.__actor(args.command == "client", self.__handle_client)
        self.__actor(args.command == "server", self.__handle_server)
        self.__actor(args.command == "ratserver", self.__handle_ratserver)
        self.__actor(args.command == "ratclient", self.__handle_ratclient)
        self.__actor(args.command == "token", self.__handle_token)
        if not self.match_found:
            self.parser.print_help()
        self.match_found = False

    def __actor(self, command_match: bool, handler: Callable, args=None):
        if command_match:
            if args:
                handler(args)
            else:
                handler()
            self.match_found = True

    @staticmethod
    def __handle_client():
        Banner()
        TCPClient()
        # threading.Thread(target=TCPClient, name="Client Thread").start()

    @staticmethod
    def __handle_server():
        Banner()
        TCPServer()
        # threading.Thread(target=TCPServer,name="Server Thread").start()

    @staticmethod
    def __handle_ratclient():
        Banner()
        threading.Thread(target=CnC().connect).start()

    @staticmethod
    def __handle_ratserver():
        Banner()
        threading.Thread(target=RatServer().launch).start()

    @staticmethod
    def __handle_token():
        print(f"Token: {generate_password()}")
