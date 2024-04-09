from dataclasses import dataclass, field
from typing import List, Any, Dict, Union


@dataclass
class Hosts:
    use_group: str
    groupnames: List[str]
    use_list: str
    clientlist: List[str]


@dataclass
class ItertoolsFunc:
    cartesian_product: str
    permutations: str
    combinations: str
    combinations_with_replacement: str


@dataclass
class PasswordGenerator:
    itertools_func: ItertoolsFunc
    output: dict
    wordlist_matrix: List[List[Union[str, List[str]]]]
    bruteforce_table: dict


@dataclass
class Scheduler:
    first_in_first_out: str
    round_robin: str
    weighted_round_robin: str


@dataclass
class Distributor:
    sliding_window: str
    sw_size_initial_bits: int
    sw_size_min_bit: int
    sw_size_max_bits: int
    scheduler: Scheduler


@dataclass
class ProtocolOperation:
    kwargs: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        for key, value in self.kwargs.items():
            setattr(self, key, value)


@dataclass
class Frame:
    operations: List[ProtocolOperation]


@dataclass
class Profile:
    profile_id: str
    hosts: Hosts
    password_generator: PasswordGenerator
    distributor: Distributor
    FrameSequence: List[Frame]


@dataclass
class Playbook:
    profiles: List[Profile]



