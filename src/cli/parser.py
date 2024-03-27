import argparse

from src.net.banner import Banner
from src.net.protocol.frame import Frame, FrameSequence
from src.net.protocol.ops import AnyInitiateConnection
from src.net.tcp.client import TCPClient
from src.net.tcp.server import TCPServer
from src.passgen.util import generate_password


class Parser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            prog="Cthulhu",
            description="Cthulhu is a password generator and distributed task runner (and a network protocol) for using thc-hydra in a distributed manner",
            epilog="https://github.com/blue-hexagon/Cthulhu",
        )  # noqa

        subparsers = self.parser.add_subparsers(dest="command", help="Subcommand to execute")

        token_parser = subparsers.add_parser("token", help="Generate a token for authentication between server and clients")

        client_parser = subparsers.add_parser("client", help="Start a client instance")
        client_parser.add_argument("--ip", default="127.0.0.1", help="Specify the destination IP (v4) address")
        client_parser.add_argument("--port", default="1060", help="Specify a port")

        server_parser = subparsers.add_parser("server", help="Start a server instance")
        server_parser.add_argument("--ip", default="127.0.0.1", help="Specify the server IP (v4) address - usually 127.0.0.1")
        server_parser.add_argument("--port", default="1060", help="...")

    def interpret(self) -> None:
        args = self.parser.parse_args()
        PAYLOAD = FrameSequence(Frame(AnyInitiateConnection(dict())))
        if args.command == "client":
            Banner()
            TCPClient(host=args.ip, port=int(args.port), payload=PAYLOAD, timeout=8)
        elif args.command == "server":
            Banner()
            TCPServer(host=args.ip, port=int(args.port), timeout=8)
        elif args.command == "token":
            print(f"Token: {generate_password()}")
        else:
            print(self.parser.print_help())
