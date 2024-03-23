import sys

from src.net.tcp.socket import TCPClient, TCPServer

if __name__ == "__main__":
    """Set addresses and ports for the server and client"""
    HOST_IP = "127.0.0.1"
    HOST_PORT = 1060
    REMOTE_IP = "127.0.0.1"
    REMOTE_PORT = 1060

    """ Run either the server or client """
    if sys.argv[1:] == ["server"]:
        TCPServer(HOST_IP, HOST_PORT, timeout=8)
    elif sys.argv[1:] == ["client"]:
        TCPClient(REMOTE_IP, REMOTE_PORT, timeout=8)
    else:
        print("Usage: dev.py server|client")
