import asyncio
import itertools
import random
from dataclasses import dataclass
from enum import Enum, auto
from time import time
from typing import Dict, Generator, List, Never

from src.conf.app_load_balancer import AppLoadBalancer
from src.passgen.bruteforce_fabricator import BruteforcePWFabricator
from src.passgen.char_class import CharacterClass
from src.utils.exceptions import PayloadExhaustedException
from src.utils.singleton import Singleton


class SlidingWindowAction(Enum):
    """Used for switching in the ObjectTracker and LoadBalancer class"""

    INCREMENT = auto()
    DECREMENT = auto()
    NOOP = auto()


class ObjectTracker(metaclass=Singleton):
    """Tracks Clients by keeping a dictionary of {cliet_hash:last_seen} items.
    This is used to scale up/down the delivered password payload"""

    # The following two thresholds defines when the query-size/payload scales up or down
    config = AppLoadBalancer.parse_toml_config()
    INCREMENT_WHEN_SEEN_WITHIN_LAST_N_SECONDS = config.scale_up_interval
    DECREMENT_WHEN_SEEN_AT_LEAST_N_SECONDS_AGO = config.scale_down_interval

    def __init__(self):
        self.hash_timestamps: Dict[int, float] = {}

    def update_timestamp(self, obj_hash: int) -> None:
        self.hash_timestamps[obj_hash] = time()

    def get_last_seen_timestamp(self, obj_hash: int) -> float:
        return self.hash_timestamps.get(obj_hash)

    def get_last_seen_seconds_difference(self, obj_hash: int) -> int:
        return int(time() - self.get_last_seen_timestamp(obj_hash))

    def get_sliding_window_action(self, obj_hash: int) -> SlidingWindowAction:
        if not AppLoadBalancer.parse_toml_config().use_scaling:
            return SlidingWindowAction.NOOP

        obj_last_seen = self.get_last_seen_seconds_difference(obj_hash)
        action: SlidingWindowAction
        if obj_last_seen <= self.INCREMENT_WHEN_SEEN_WITHIN_LAST_N_SECONDS:
            action = SlidingWindowAction.INCREMENT
        elif obj_last_seen >= self.DECREMENT_WHEN_SEEN_AT_LEAST_N_SECONDS_AGO:
            action = SlidingWindowAction.DECREMENT
        else:
            action = SlidingWindowAction.NOOP
        return action


@dataclass
class Client:
    """A proxy class for real clients.
    Instantiate real clients witht his class to use the load balancer
    """

    ipv4_addr: str
    port: int
    weight: int = 0
    sliding_window_multiplier: int = 2
    # sliding_window_multiplier starts at 2, queue_size compensates for this in the Load Balancer class
    # doing it this way just makes it easier to work with.
    tracker: ObjectTracker = ObjectTracker()

    def __post_init__(self):
        """Sets the initial timestamp"""
        self.tracker.update_timestamp(hash(self))
        if self.sliding_window_multiplier <= 1:
            raise ValueError("Sliding window multiplier must be 2 or greater")
        if self.sliding_window_multiplier % 2 != 0:
            raise ValueError("Sliding window multiplier must be % 2 == 0")

    def increment_sliding_window(self) -> None:
        self.sliding_window_multiplier *= 2

    def decrement_sliding_window(self) -> None:
        if self.sliding_window_multiplier % 2 != 0:
            raise RuntimeError("Sliding window multiplier is not divisible by 2")
        if (
            self.sliding_window_multiplier >= 4 and self.sliding_window_multiplier <= 2**8
        ):  # noqa Don't decrement if multiplier is less than four!
            self.sliding_window_multiplier //= 2

    def __str__(self) -> str:
        return f"{self.ipv4_addr}:{self.port}; window_mult={self.sliding_window_multiplier}"

    def __hash__(self):
        """Only hash non-changing properties"""
        return hash((self.ipv4_addr, self.port))


class RoundRobinLoadBalancer(metaclass=Singleton):
    """Password distribution system - aka. a load-balancer"""

    def __init__(self, queue_size, generator) -> None:  # noqa
        self.client_queue: asyncio.Queue[Client] = asyncio.Queue(maxsize=0)
        self.queue_size: int = queue_size // 2  # Halved because our sliding window multiplier starts at 2, for it's very own reason :-)
        self.pw_generator: Generator = generator
        self.current_client_index = 0

    async def add_client(self, client: Client) -> None:
        await self.client_queue.put(client)
        client.tracker.update_timestamp(hash(client))

    def remove_client(self) -> None:
        self.client_queue.get_nowait()

    async def get_next_client(self) -> Client:
        client: Client = await self.client_queue.get()
        slw_action = client.tracker.get_sliding_window_action(hash(client))
        if slw_action == SlidingWindowAction.INCREMENT:
            client.increment_sliding_window()
        elif slw_action == SlidingWindowAction.DECREMENT:
            client.decrement_sliding_window()
        elif slw_action == SlidingWindowAction.NOOP:
            pass
        return client

    def retrieve_payload(self, current_client: Client) -> List[str]:
        payload: List[str] = []
        for _ in range(0, self.queue_size * current_client.sliding_window_multiplier):
            try:
                payload.append(next(self.pw_generator))
            except StopIteration:
                pass
        return payload

    async def await_clients(self):
        clients = [
            Client(ipv4_addr="127.0.0.1", port=8001, sliding_window_multiplier=2, weight=2),
            Client(ipv4_addr="127.0.0.1", port=8002, sliding_window_multiplier=2, weight=1),
            Client(ipv4_addr="127.0.0.1", port=8003, sliding_window_multiplier=2, weight=3),
        ]
        while True:
            for i in range(random.randint(1, 5)):
                await self.add_client(clients[random.randint(0, len(clients) - 1)])
            await asyncio.sleep(random.uniform(0.1, 2.4))

    async def run(self) -> Never:
        while True:
            if self.client_queue.empty():
                await asyncio.sleep(0.125)  # 1/8th, just to my liking..
                continue
            current_client = await self.get_next_client()
            current_data = self.retrieve_payload(current_client)
            if not current_data:
                raise PayloadExhaustedException()
            print(
                f"{current_client} secs:{current_client.tracker.get_last_seen_seconds_difference(hash(current_client))} -> {current_data}"
            )


async def main():
    pass_gen: Generator = BruteforcePWFabricator(1, 3, combinatoric_iterator=itertools.product).use_generator(
        [CharacterClass.DIGITS, CharacterClass.HEXDIGITS_UPPER]
    )  # noqa. This just returns a generator that spits out passwords-permutations of uppercase hexadecimal characters length 1 to 3
    rbl = RoundRobinLoadBalancer(queue_size=4, generator=pass_gen)
    load_balancer = asyncio.create_task(rbl.run())
    await_clients = asyncio.create_task(rbl.await_clients())
    await asyncio.gather(load_balancer, await_clients)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except PayloadExhaustedException:
        pass
