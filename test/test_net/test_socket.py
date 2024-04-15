from threading import Thread

from src.net.protocol.core.frame import FrameSequence, Frame
from src.net.protocol.ops import MakeAnySleepForDuration
from src.net.tcp.client import TCPClient
from src.net.tcp.server import TCPServer

HOST = "127.0.0.1"
PORT = 12345
MESSAGE = "Hello from client"


class TestSocketCommunication:

    @classmethod
    def setup_class(cls) -> None:
        cls.server_thread = Thread(target=TCPServer, args=("127.0.0.1", 1060, 8), daemon=True).start()

    def test_client_server_communication(self) -> None:
        payload = FrameSequence(
            Frame(MakeAnySleepForDuration(time="3s")),
        )
        TCPClient("127.0.0.1", 1060, payload, timeout=8)
