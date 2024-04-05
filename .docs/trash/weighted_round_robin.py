import itertools
from typing import Generator, List

from src.passgen.bruteforce_fabricator import BruteforcePWFabricator
from src.passgen.char_class import CharacterClass


class WeightedRoundRobinLoadBalancer:
    def __init__(self, servers, queue_size, generator):
        self.servers = servers
        self.current_index = 0
        self.weights = [weight for _, weight in servers]
        self.max_weight = max(self.weights)
        self.gcd = self._compute_gcd(self.weights)
        self.length = sum(self.weights) // self.gcd
        self.queue = list(itertools.chain.from_iterable([index] * (weight // self.gcd) for index, weight in enumerate(self.weights)))
        print(self.queue)
        self.pw_generator: Generator = generator
        self.queue_size: int = queue_size

    def _compute_gcd(self, nums):
        x = nums[0]
        for num in nums[1:]:
            x = self._gcd(x, num)
        return x

    @staticmethod
    def _gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def get_next_server(self):
        while True:
            index = self.queue[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.queue)
            server = self.servers[index]
            return server

    def retrieve_payload(self):
        payload: List[str] = []
        for _ in range(0, self.queue_size):
            try:
                payload.append(next(self.pw_generator))
            except StopIteration:
                pass
        return payload

    def run(self):  # noqa
        while True:
            current_server = self.get_next_server()
            current_data = self.retrieve_payload()
            if not current_data:
                break
            print(f"{current_server} -> {current_data}")


if __name__ == "__main__":
    pass_gen = BruteforcePWFabricator(1, 3, combinatoric_iterator=itertools.permutations).use_generator(
        [CharacterClass.DIGITS, CharacterClass.HEXDIGITS_UPPER]
    )  # This just returns a generator that spits out passwords-permutations of uppercase hexadecimal characters length 1 to 3
    WeightedRoundRobinLoadBalancer(
        servers=[(("127.0.0.1", 8001), 2), (("127.0.0.1", 8002), 1), (("127.0.0.1", 8003), 3)], queue_size=16, generator=pass_gen
    ).run()
