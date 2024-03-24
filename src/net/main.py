import sys

from src.net.banner import Banner
from tcp.socket import TCPServer, TCPClient

if __name__ == "__main__":
    """ Set addresses and ports for the server and client """
    HOST_IP = "127.0.0.1"
    HOST_PORT = 1060
    REMOTE_IP = "127.0.0.1"
    REMOTE_PORT = 1060

    Banner()

    """ Run either the server or client """
    if sys.argv[1:] == ["server"]:
        TCPServer(HOST_IP, HOST_PORT, timeout=8)
    elif sys.argv[1:] == ["client"]:
        TCPClient(REMOTE_IP, REMOTE_PORT, timeout=8)
    elif sys.argv[1:] in [["-h"], ["--help"], ["help"]]:
        print("Usage: net.py server|client|[-h,--help,help]|<empty>")
    else:
        choice = input("(s)erver or (c)lient?")
        if choice.lower() not in ['s', 'c']:
            raise RuntimeError("Invalid input.")
        elif choice.lower() == 's':
            TCPServer(HOST_IP, HOST_PORT, timeout=8)
        elif choice.lower() == 'c':
            TCPClient(REMOTE_IP, REMOTE_PORT, timeout=8)
