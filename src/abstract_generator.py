import itertools
from abc import ABC, abstractmethod
from typing import List, Tuple, Generator


class PWGenerator(ABC):
    CARTESIAN_PRODUCT = itertools.product
    COMBINATIONS = itertools.combinations
    COMBINATIONS_WITH_REPLACEMENT = itertools.combinations_with_replacement
    PERMUTATIONS = itertools.permutations

    def __init__(self):
        super().__init__()

    @abstractmethod
    def use_filewriter(self, input_data: Tuple | List) -> None:
        pass

    @abstractmethod
    def use_generator(self, input_data: Tuple | List) -> Generator:
        pass
