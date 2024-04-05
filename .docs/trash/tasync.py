import asyncio
import itertools
from dataclasses import dataclass
from typing import Generator, List

from src.passgen.bruteforce_fabricator import BruteforcePWFabricator
from src.passgen.char_class import CharacterClass
from src.utils.singleton import Singleton


@dataclass
class Client:
    ipv4: str
    port: int
    weight: int
    sliding_window_multiplier: int

    def increment_sliding_window(self) -> None:
        self.sliding_window_multiplier *= 2

    def decrement_sliding_window(self) -> None:
        if self.sliding_window_multiplier >= 2 and self.sliding_window_multiplier % 2 == 0:
            self.sliding_window_multiplier //= 2
        else:
            raise ValueError("Sliding window multiplier mod 2 != 0")


class RoundRobinLoadBalancer(metaclass=Singleton):
    """Password distribution system - aka. a load-balancer"""

    def __init__(self, queue_size, generator):  # noqa
        self.clients: List[Client] = []
        self.queue_size: int = queue_size
        self.pw_generator: Generator = generator
        self.current_client_index = 0

    def add_client(self, client: Client):
        self.clients.append(client)

    def remove_client(self, client: Client):
        self.clients.remove(client)

    def get_next_client(self):
        self.current_client_index = (self.current_client_index + 1) % len(self.clients)
        return self.clients[self.current_client_index]

    async def retrieve_payload(self, current_client):
        payload: List[str] = []
        for _ in range(0, self.queue_size * current_client.sliding_window_multiplier):
            try:
                payload.append(next(self.pw_generator))
            except StopIteration:
                pass
        return payload

    async def process_clients(self):
        while True:
            if not self.clients:
                await asyncio.sleep(1)
                continue

            current_client = self.get_next_client()
            current_data = await self.retrieve_payload(current_client)
            if not current_data:
                break
            print(f"{current_client} -> {current_data}")
            await asyncio.sleep(0.1)  # Adjust as needed


if __name__ == "__main__":
    pass_gen = BruteforcePWFabricator(1, 3, combinatoric_iterator=itertools.product).use_generator(
        [CharacterClass.DIGITS, CharacterClass.HEXDIGITS_UPPER]
    )  # This just returns a generator that spits out passwords-permutations of uppercase hexadecimal characters length 1 to 3

    load_balancer = RoundRobinLoadBalancer(queue_size=4, generator=pass_gen)

    # Add some initial clients
    clients = [
        Client(ipv4="127.0.0.1", port=8001, sliding_window_multiplier=1, weight=2),
        Client(ipv4="127.0.0.1", port=8002, sliding_window_multiplier=1, weight=1),
        Client(ipv4="127.0.0.1", port=8003, sliding_window_multiplier=1, weight=3),
    ]
    for client in clients:
        load_balancer.add_client(client)

    # Simulate adding clients dynamically
    async def add_clients():
        await asyncio.sleep(5)  # Wait for 5 seconds before adding new clients
        new_clients = [
            Client(ipv4="10.8.8.1", port=8004, sliding_window_multiplier=1, weight=1),
            Client(ipv4="60.1.9.1", port=8005, sliding_window_multiplier=1, weight=2),
        ]
        for client in new_clients:
            load_balancer.add_client(client)
            print(f"Added new client: {client}")
        new_clients[0].increment_sliding_window()
        new_clients[0].increment_sliding_window()
        clients[1].increment_sliding_window()

    asyncio.run(add_clients())

    # Simulate removing clients dynamically
    async def remove_clients():
        await asyncio.sleep(5)  # Wait for 5 seconds before removing clients
        clients[1].decrement_sliding_window()
        for client in new_clients:
            load_balancer.remove_client(client)
            print(f"Removed client: {client}")

    asyncio.run(remove_clients())

    # Add clients again
    async def add_clients_again():
        await asyncio.sleep(5)
        for client in clients:
            client.increment_sliding_window()
            load_balancer.add_client(client)

    asyncio.run(add_clients_again())

    # Run the load balancer asynchronously
    asyncio.run(load_balancer.process_clients())
