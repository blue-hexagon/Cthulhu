import re


class Utils:
    @staticmethod
    def get_ms_delay(delay: str) -> str | ValueError:
        delay_int = re.sub("[^0-9]", "", delay)
        if delay.find("ms"):
            return delay
        elif delay.find("s"):
            return str(int(delay_int) * 1000)
        elif delay.find("m"):
            return str(int(delay_int) * 1000 * 60)
        elif delay.find("h"):
            return str(int(delay_int) * 1000 * 60 * 60)
        raise ValueError("Wrong attack delay specified. Param delay: '<number>[ms|s|m|h]' | Example: '90m'")
