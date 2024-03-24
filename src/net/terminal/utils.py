import os

from src.utils.singleton import Singleton


class TermUtils(metaclass=Singleton):
    @staticmethod
    def terminal_size():
        try:
            term = os.get_terminal_size()
            return term.columns, term.lines
        except OSError:
            # Failed to retrieve terminal size. Using default size.
            return 80, 24

    @property
    def terminal_width(self):
        return self.terminal_size()[0]

    @property
    def terminal_height(self):
        return self.terminal_size()[1]
