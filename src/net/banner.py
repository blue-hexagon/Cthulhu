import os

from src.net.terminal.utils import TermUtils


class Banner:
    (columns, lines) = TermUtils.terminal_size()
    banner = f"""

   █████████   █████    █████                 ████  █████                
  ███░░░░░███ ░░███    ░░███                 ░░███ ░░███                 
 ███     ░░░  ███████   ░███████   █████ ████ ░███  ░███████   █████ ████
░███         ░░░███░    ░███░░███ ░░███ ░███  ░███  ░███░░███ ░░███ ░███ 
░███           ░███     ░███ ░███  ░███ ░███  ░███  ░███ ░███  ░███ ░███ 
░░███     ███  ░███ ███ ░███ ░███  ░███ ░███  ░███  ░███ ░███  ░███ ░███ 
 ░░█████████   ░░█████  ████ █████ ░░████████ █████ ████ █████ ░░████████
  ░░░░░░░░░     ░░░░░  ░░░░ ░░░░░   ░░░░░░░░ ░░░░░ ░░░░ ░░░░░   ░░░░░░░░ 
    """
    line_len = len(banner.splitlines()[len(banner.splitlines()) // 2])
    whitespace_prefix = (columns - line_len) // 2
    for idx, line in enumerate(banner.splitlines()):
        print(f"{' ' * whitespace_prefix}{line}")
