import socket
import logging

class Node:
    """ A node recieves requests from Cthulhu """

    def __init__(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format="[ %(asctime)s ] - [%(name)s-%(lineno)d] - [%(levelname)s] %(message)s"
        )
        logger = logging.getLogger("node-logger")
        logger.info(f"Setting up node: {socket.gethostname()}@{socket.gethostbyname(socket.gethostname())}")
        self.hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(socket.gethostname())
        print(Node.get_ipaddr_from_hostname())
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(None)

    @staticmethod
    def get_ipaddr_from_hostname(hostname="www.google.com"):
        return socket.gethostbyname(hostname)
    @staticmethod
    def convert_byteorder(data,byteorder):
        """
        htonl() translates an unsigned long integer into network byte order.
        htons() translates an unsigned short integer into network byte order.
        ntohl() translates an unsigned long integer into host byte order.
        ntohs() translates an unsigned short integer into host byte order.
        """
        """
            node = Node()
            data = 10
            print(node.convert_byteorder(data,"htonl"))
            print(node.convert_byteorder(data,"htons"))
            print(node.convert_byteorder(data,"ntohl"))
            print(node.convert_byteorder(data,"ntohs"))
        """
        match byteorder:
            case "htonl":
                return socket.htonl(data)
            case "htons":
                return socket.htons(data)
            case "ntohl":
                return socket.ntohl(data)
            case "ntohs":
                return socket.ntohs(data)
            case _:
                raise KeyError("Invalid byteorder")

    def __str__(self):
        pass

    def __repr__(self):
        pass


if __name__ == '__main__':
    pass