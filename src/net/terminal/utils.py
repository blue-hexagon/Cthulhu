import os
from typing import Tuple

from src.utils.singleton import Singleton


class TermUtils(metaclass=Singleton):
    """Class for retrieving the used terminals dimensions - falls back to default values"""

    @staticmethod
    def terminal_size() -> Tuple[int, int]:
        try:
            term = os.get_terminal_size()
            return term.columns, term.lines
        except OSError:
            # Failed to retrieve terminal size. Using default size.
            return 80, 24

    @property
    def terminal_width(self) -> int:
        return self.terminal_size()[0]

    @property
    def terminal_height(self) -> int:
        return self.terminal_size()[1]
