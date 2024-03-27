import socket

from src.conf.app_server import AppServer
from src.net.protocol.ops import AnyInitiateConnection
from src.net.tcp.socket import TcpSocket
from src.utils.exceptions import BreakException
from src.utils.singleton import Singleton


class ServerState(metaclass=Singleton):
    def __init__(self):
        self.repeat: int = -1
        self.next_n_commands: int = -1
        self.pw_cache_limit: int = -1
        self.fire_attack_delay: int = -1
        self.stop_attack: bool = False


class TCPServer(TcpSocket):
    """Server code goes here"""

    server_conf = AppServer.parse_toml_config()

    def __init__(
        self,
        host: str = server_conf.server_ip,
        port: int = server_conf.server_port,
        token: str = server_conf.token,
        timeout=server_conf.server_timeout,
    ) -> None:
        self.token = token
        self.srv_state = ServerState()  # TODO: move to ops?
        super().__init__(host, port, timeout, server=True, client=False)
        while True:  # Runs until timeout if no incoming connections, then exits when timeout reached.
            s: socket.socket = self.accept_incoming_connection()
            # print(f"s: {type(s)}\n{s}{s.type}")
            while True:  # Runs while the socket is alive
                try:
                    frame_sequence = TcpSocket.recv_all(s)
                except EOFError:
                    break
                # self.fprint(self.peername(host), frame_sequence)
                try:
                    for frame in frame_sequence.frames:
                        op = frame.operation
                        op_type = type(frame.operation)
                        if op_type is AnyInitiateConnection:
                            op.check(s, self.token)
                        else:
                            self.narrator.error(f"Protocol operation not recognized. Ignoring: {op}.")
                except BreakException:
                    break
