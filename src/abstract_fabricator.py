from abc import ABC, abstractmethod
from typing import Generator, List, Tuple


class PasswordFabricator(ABC):
    """
    -- Implemented --
    itertools.product('ABCD', repeat=2):
    - AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
    - Args: p, q, … [repeat=1]
    - cartesian product, equivalent to a nested for-loop

    itertools.permutations('ABCD', 2):
    - AB AC AD BA BC BD CA CB CD DA DB DC
    - Args: p[, r]
    - r-length tuples, all possible orderings, no repeated elements

    -- Not Implemented --
    itertools.combinations('ABCD', 2):
    - AB AC AD BC BD CD
    - Args: p, r
    - r-length tuples, in sorted order, no repeated elements

    itertools.combinations_with_replacement('ABCD', 2):
    - AA AB AC AD BB BC BD CC CD DD
    - Args: p, r
    - r-length tuples, in sorted order, with repeated elements
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def use_filewriter(self, input_data: Tuple | List) -> None:
        pass

    @abstractmethod
    def use_generator(self, input_data: Tuple | List) -> Generator:
        pass
