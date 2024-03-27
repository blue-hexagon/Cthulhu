from src.net.terminal.utils import TermUtils


class TestTerminalUtils:

    def test_term_size(self) -> None:
        tu = TermUtils()
        (width, height) = tu.terminal_size()
        assert width == tu.terminal_width
        assert height == tu.terminal_height
