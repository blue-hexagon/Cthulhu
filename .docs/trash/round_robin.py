import itertools
import random
from dataclasses import dataclass
from threading import Thread
from time import sleep
from typing import Generator, List, Tuple

from src.passgen.bruteforce_fabricator import BruteforcePWFabricator
from src.passgen.char_class import CharacterClass


@dataclass
class Client:
    ipv4: str
    port: int
    weight: int
    sliding_window_multiplier: int


class RoundRobinLoadBalancer:
    """Password distribution system - aka. a load-balancer"""

    def __init__(self, clients, queue_size, generator, weights=None):  # noqa
        self.clients: List[Client] = clients
        self.queue_size: int = queue_size
        self.weights: List[int] | None = weights  # TODO: implement
        self.current_server_index = 0
        self.pw_generator: Generator = generator
        t = Thread(target=self.run, name="Thread-1")
        t.start()
        t.join(timeout=10)

    def get_next_server(self):
        server = self.clients[self.current_server_index]
        self.current_server_index = (self.current_server_index + 1) % len(self.clients)
        return server

    def retrieve_payload(self, current_client):
        payload: List[str] = []
        for _ in range(0, self.queue_size * current_client.sliding_window_multiplier):
            try:
                payload.append(next(self.pw_generator))
            except StopIteration:
                pass
        return payload

    def run(self):  # noqa
        while True:
            current_server = self.get_next_server()
            current_data = self.retrieve_payload(current_server)
            if not current_data:
                break
            print(f"{current_server} -> {current_data}")
            sleep(random.randint(1, 2) / random.randint(10, 100))


if __name__ == "__main__":
    pass_gen = BruteforcePWFabricator(1, 4, combinatoric_iterator=itertools.product).use_generator(
        [CharacterClass.DIGITS, CharacterClass.HEXDIGITS_UPPER]
    )  # This just returns a generator that spits out passwords-permutations of uppercase hexadecimal characters length 1 to 3
    clients = [
        Client(ipv4="127.0.0.1", port=8001, sliding_window_multiplier=1, weight=2),
        Client(ipv4="127.0.0.1", port=8002, sliding_window_multiplier=1, weight=1),
        Client(ipv4="127.0.0.1", port=8002, sliding_window_multiplier=1, weight=3),
    ]
    RoundRobinLoadBalancer(clients=clients, queue_size=4, generator=pass_gen)


"""
('127.0.0.1', 8001) -> ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
('127.0.0.1', 8002) -> ['01', '02', '03', '04', '05', '06', '07', '08', '09', '0A', '0B', '0C', '0D', '0E', '0F', '10']
('127.0.0.1', 8003) -> ['12', '13', '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D', '1E', '1F', '20', '21']
('127.0.0.1', 8001) -> ['23', '24', '25', '26', '27', '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31', '32']
('127.0.0.1', 8002) -> ['34', '35', '36', '37', '38', '39', '3A', '3B', '3C', '3D', '3E', '3F', '40', '41', '42', '43']
('127.0.0.1', 8003) -> ['45', '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F', '50', '51', '52', '53', '54']
('127.0.0.1', 8001) -> ['56', '57', '58', '59', '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63', '64', '65']
('127.0.0.1', 8002) -> ['67', '68', '69', '6A', '6B', '6C', '6D', '6E', '6F', '70', '71', '72', '73', '74', '75', '76']
('127.0.0.1', 8003) -> ['78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81', '82', '83', '84', '85', '86', '87']
('127.0.0.1', 8001) -> ['89', '8A', '8B', '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95', '96', '97', '98']
('127.0.0.1', 8002) -> ['9A', '9B', '9C', '9D', '9E', '9F', 'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
('127.0.0.1', 8003) -> ['AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA']
('127.0.0.1', 8001) -> ['BC', 'BD', 'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'CA', 'CB']
('127.0.0.1', 8002) -> ['CD', 'CE', 'CF', 'D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB', 'DC']
('127.0.0.1', 8003) -> ['DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED']
('127.0.0.1', 8001) -> ['EF', 'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'FA', 'FB', 'FC', 'FD', 'FE']
('127.0.0.1', 8002) -> ['012', '013', '014', '015', '016', '017', '018', '019', '01A', '01B', '01C', '01D', '01E', '01F', '021', '023']
('127.0.0.1', 8003) -> ['024', '025', '026', '027', '028', '029', '02A', '02B', '02C', '02D', '02E', '02F', '031', '032', '034', '035']
('127.0.0.1', 8001) -> ['036', '037', '038', '039', '03A', '03B', '03C', '03D', '03E', '03F', '041', '042', '043', '045', '046', '047']
... and so on
"""
