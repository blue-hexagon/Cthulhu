from src.net.protocol.frame import FrameSequence
from src.net.tcp.socket import TcpSocket


class TCPClient(TcpSocket):
    """Client code goes here"""

    def __init__(self, host: str, port: int, payload: FrameSequence, timeout=0) -> None:
        super().__init__(host, port, timeout, server=False, client=True)
        while True:
            TcpSocket.send_all(self.s, payload)
            # sFormatter.fprint(self.peername(host), self.recv_all(self.s))
            break
        self.s.close()
