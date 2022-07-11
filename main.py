import itertools
import os
import socket
import sys
from datetime import datetime

from src.bruteforce_fabricator import BruteforcePWFabricator, CharacterClass
from src.wordlist_fabricator import WordlistPWFabricator


def use_bruteforce():
    BruteforcePWFabricator(4, 4, filename="hex_upper__4_4.txt", combinatoric_iterator=itertools.product).use_filewriter(
        [CharacterClass.DIGITS, CharacterClass.HEXDIGITS_UPPER]
    )
    bruteforce_map = BruteforcePWFabricator(1, 3, combinatoric_iterator=itertools.permutations).use_generator(["abc"])
    while 1:
        try:
            print(next(bruteforce_map))
        except StopIteration:
            break


def use_wordlist():
    WordlistPWFabricator(filename="wl_common__4_4.txt").use_filewriter((["app", "app-"], ["script"], ["-ch2", "-ch1"]))
    wordlist_generator = WordlistPWFabricator().use_generator(
        (
            ["København", "københavn", "Copenhagen", "copenhagen"],
            ["!", "!1", "*", "123", "2600", "2600!"],
        )
    )
    while 1:
        try:
            print(next(wordlist_generator))
        except StopIteration:
            break


if __name__ == "__main__":

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MAX = 65535
    SERVER_PORT = 1061
    SERVER_IP = "0.0.0.0"

    def prompt_tr(transmitter, reciever):
        return f'[{datetime.now().strftime("%H:%M:%S")} – {transmitter} -> {reciever}]:'

    def prompt_init(host):
        return f'[{datetime.now().strftime("%H:%M:%S")} – {host}]:'

    if sys.argv[1:] == ["server"]:
        wordlist_generator = WordlistPWFabricator().use_generator(
            (
                ["København", "københavn", "Copenhagen", "copenhagen"],
                ["!", "!1", "*", "123", "2600", "2600!"],
            )
        )
        try:
            s.bind((SERVER_IP, SERVER_PORT))
            print(f'{prompt_init("Cthulhu")} Listening on {SERVER_IP}:{SERVER_PORT}')
        except OSError:
            print(f'{prompt_tr("Cthulhu","Node")}: Socket {SERVER_IP, SERVER_PORT} already in use.')
            sys.exit(1)
        while True:
            data, address = s.recvfrom(MAX)
            if data.decode("utf-8") == "EOF":
                s.close()
                print(f'{prompt_tr("Node", "Cthulhu")} {data.decode("utf-8")}')
                sys.exit(0)
            else:
                print(f'{prompt_tr("Node","Cthulhu")} {data.decode("utf-8")}')
            try:
                s.sendto(bytes(f"{next(wordlist_generator)}", "utf-8"), address)
            except StopIteration:
                s.sendto(bytes("EOF", "utf-8"), address)
    elif sys.argv[1:] == ["client"]:
        SERVER_IP = "127.0.0.1"
        s.connect((SERVER_IP, SERVER_PORT))
        while True:
            try:
                s.send(b"GET")
                data = s.recv(MAX)
                if data.decode("utf-8") == "EOF":
                    print(f'{prompt_tr("Cthulhu","Node")} {data.decode("utf-8")}')
                    s.send(b"EOF")
                    s.close()
                    sys.exit(0)
                print(f'{prompt_tr("Cthulhu","Node")} {data.decode("utf-8")}')
            except ConnectionResetError:
                print(f"{prompt_init('Node')} Could not connect to server {SERVER_IP, SERVER_PORT}")
                sys.exit(1)
    else:
        print(sys.stderr, "usage: *.py server | client")
    # use_bruteforce()
    # use_wordlist()
