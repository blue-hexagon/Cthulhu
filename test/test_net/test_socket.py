import unittest
from threading import Thread
import time

from src.net.tcp.socket import TCPServer, TCPClient

HOST = '127.0.0.1'
PORT = 12345
MESSAGE = "Hello from client"

class TestSocketCommunication(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_thread = Thread(target=TCPServer, args=("127.0.0.1", 1060, 8))
        cls.server_thread.daemon = True
        cls.server_thread.start()

    def test_client_server_communication(self):
        TCPClient("127.0.0.1", 1060)

if __name__ == '__main__':
    unittest.main()