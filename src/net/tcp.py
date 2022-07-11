import math
import random
import socket
import sys
import time
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from collections import namedtuple
import pickle
from typing import Tuple, NamedTuple

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = sys.argv.pop() if len(sys.argv) == 3 else '127.0.0.1'
    PORT = 1060
    message_id_seed = 20


    class ProtocolOperation():
        def __init__(self, operation_name, *args):
            self.operation_name = operation_name
            for param in args:
                setattr(self,)
        """ See each docstring for usage examples and info """

        """
        GET_PASSWORD_LIST(sample_size='10')
        GET_PASSWORD_LIST(sample_size_between='10-30')
        - Node -> Cthulhu.
        - Node instructs Cthulhu to feed it passwords (Cthulhu chooses if it wants to use a generator for generating passwords or read passwords from a file)
        """
        GET_PASSWORD_LIST = namedtuple('GET_PASSWORD_LIST', ['sample_size_or_range'])

        """
        FIRE_AUTH_ATTACK(delay_simple_time_string='90m')
        - Cthulhu -> Node
        - Instructs the node to fire the authentication attack (make sure you feed it or have fed it passwords)
        """
        FIRE_AUTH_ATTACK = namedtuple('FIRE_AUTH_ATTACK', ['delay_simple_time_string'])

        """
        STOP_AUTH_ATTACK(delay_simple_time_string='2h')
        - Cthulhu -> Node
        - Instructs the node to stop the authentication attack
        """
        STOP_AUTH_ATTACK = namedtuple('STOP_AUTH_ATTACK', ['delay_simple_time_string'])

        """
        NODE_SLEEP(simple_time_string='10s') - ms, s, m, h
        - Cthulhu -> Node
        - Make the node sleep for a duration
        """
        NODE_SLEEP_NOOP = namedtuple('NODE_SLEEP', ['simple_time_string'])

        """
        NODE_SLEEP_BETWEEN_REQUEST(simple_time_string='25-175ms')
        - Cthulhu -> Node
        - Makes the node sleep between requests. The duration can be fixed or a random time between an interval.
        """
        NODE_SLEEP_BETWEEN_REQUEST = namedtuple('NODE_SLEEP_BETWEEN_REQUEST', ['simple_time_string'])
        """
        AUTH_PROTOCOL(protocol='ssh')
        - Cthulhu -> Node
        - Sets the protocol used for the authentication attack
        """
        AUTH_PROTOCOL = namedtuple('AUTH_PROTOCOL', ['protocol'])


    class FrameSegment():
        def __init__(self, segment):
            self.segment_string = segment
            self.segment_length = len(segment)


    @dataclass
    class Frame():
        frame_length: str
        message_id: str
        operation: str
        message: str

        def get_framelength(self):
            return self.frame_length

        def get_id(self):
            return self.message_id

        def get_operation(self):
            return self.operation

        def get_message(self):
            return self.message


    def sendall(sock, message: str, operation):
        message_id = FrameSegment(f"Message-ID: {22:<16}")
        operation = FrameSegment(f"Operation: {str(ProtocolOperation.NODE_SLEEP_NOOP(simple_time_string='3s')):<16}")
        message = FrameSegment(f"Message: {message:<901}")
        frame_size = FrameSegment(f"Frame-Length: {1024:<8}")

        frame_size = f"Frame-Length: {message_id.segment_length + operation.segment_length + message.segment_length + frame_size.segment_length:<8}"
        frame = Frame(frame_length=str(len(frame_size)), message_id=message_id.segment_string, operation=operation.segment_string, message=message.segment_string)
        sock.sendall(bytes(pickle.dumps(frame)))


    def print_recv(transmitter, reciever, msg):
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {transmitter} -> {reciever}]:\n{msg}')


    def print_host(host, msg):
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {host}]: {msg}')


    def recv_all(sock, length):
        data = b''
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                raise EOFError(f'socket closed at {len(data)} bytes into a {length}-byte message')
            data += more
        return parse_message(pickle.loads(data))


    def parse_message(data):
        data = data.splitlines()
        frame_length = ''
        message_id = ''
        return data


    if sys.argv[1:] == ['server']:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            print_host('Cthulhu', f'Listening at {s.getsockname()}')
            sc, sockname = s.accept()
            print_host('Cthulhu', f'We have accepted a connection from {sockname}')
            print_host('Cthulhu', f'Socket connects {sc.getsockname()} and {sc.getpeername()}')
            message = recv_all(sc, 1024)
            print_recv(sc.getpeername(), 'Cthulhu', str(message))
            sendall(sc, "Farewell client", ProtocolOperation.NODE_SLEEP_NOOP(simple_time_string='2s'))
            print_host('Cthulhu', 'Reply sent, closing socket')
            message2 = recv_all(sc, 1024)
            sc.close()
    elif sys.argv[1:] == ['client']:
        s.connect((HOST, PORT))
        print_host('Node', f'Client has been assigned socket name {s.getsockname()}')
        sendall(s, "Hi there, server!", ProtocolOperation.NODE_SLEEP_NOOP(simple_time_string='3s'))
        reply = recv_all(s, 1024)
        if "Farewell client" in reply:
            print_recv('Cthulhu', s.getsockname(), str(reply))
            sendall(s, "1234567890abcdef", ProtocolOperation.NODE_SLEEP_NOOP(simple_time_string='3s'))
            s.close()
    else:
        print(f"Usage: tcp.py server|client [host]")
