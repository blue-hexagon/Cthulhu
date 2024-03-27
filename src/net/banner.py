from src.net.terminal.utils import TermUtils


class Banner:
    """Prints a banner in the terminal when starting the application.
    Instantiation of the class prints the banner.
    """

    def __init__(self) -> None:
        (columns, lines) = TermUtils().terminal_size()
        banner = """

   █████████   █████    █████                 ████  █████
  ███░░░░░███ ░░███    ░░███                 ░░███ ░░███
 ███     ░░░  ███████   ░███████   █████ ████ ░███  ░███████   █████ ████
░███         ░░░███░    ░███░░███ ░░███ ░███  ░███  ░███░░███ ░░███ ░███
░███           ░███     ░███ ░███  ░███ ░███  ░███  ░███ ░███  ░███ ░███
░░███     ███  ░███ ███ ░███ ░███  ░███ ░███  ░███  ░███ ░███  ░███ ░███
 ░░█████████   ░░█████  ████ █████ ░░████████ █████ ████ █████ ░░████████
  ░░░░░░░░░     ░░░░░  ░░░░ ░░░░░   ░░░░░░░░ ░░░░░ ░░░░ ░░░░░   ░░░░░░░░
        """

        """ Center the banner horizontally in the terminal """
        line_len = len(banner.splitlines()[len(banner.splitlines()) // 2])
        whitespace_prefix = (columns - line_len) // 2
        for idx, line in enumerate(banner.splitlines()):
            print(f"{' ' * whitespace_prefix}{line}")
