from time import sleep

from src.conf.app_client import AppClient
from src.net.protocol.frame import Frame, FrameSequence
from src.net.protocol.ops import AnyInitiateConnection
from src.net.protocol.sender_identity import SenderIdentity
from src.net.tcp.socket import TcpSocket


class TCPClient(TcpSocket):
    """Client code goes here"""

    app_client = AppClient.parse_toml_config()

    def __init__(
        self,
        host: str = app_client.server_ip,
        port: int = app_client.server_port,
        token: str = app_client.token,
        timeout=app_client.node_timeout,
    ) -> None:
        super().__init__(host, port, timeout, server=False, client=True)
        while True:
            self.send_all(
                self.s,
                FrameSequence(
                    Frame(AnyInitiateConnection(SenderIdentity.Client, token)),
                    Frame(AnyInitiateConnection(SenderIdentity.Client, "bad-token")),
                ),
            )
            # sFormatter.fprint(self.peername(host), self.recv_all(self.s))
            break
        self.s.close()
