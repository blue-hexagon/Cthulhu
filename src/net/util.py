import re

from src.utils.singleton import Singleton


class Utils(metaclass=Singleton):
    ms_to_sec = 1000
    sec_to_min = 60
    min_to_hour = 60
    hour_to_day = 24
    day_to_week = 7

    @classmethod
    def get_ms_delay(cls, delay: str) -> str | ValueError:
        delay_int = re.sub("[^0-9]", "", delay)
        # @formatter:off
        if delay.endswith("ms"):
            return delay
        elif delay.endswith("s"):
            return str(int(delay_int) * cls.ms_to_sec)
        elif delay.endswith("m"):
            return str(int(delay_int) * cls.ms_to_sec * cls.sec_to_min)
        elif delay.endswith("h"):
            return str(int(delay_int) * cls.ms_to_sec * cls.sec_to_min * cls.min_to_hour)
        elif delay.endswith("d"):
            return str(int(delay_int) * cls.ms_to_sec * cls.sec_to_min * cls.min_to_hour * cls.hour_to_day)
        elif delay.endswith("w"):
            return str(int(delay_int) * cls.ms_to_sec * cls.sec_to_min * cls.min_to_hour * cls.hour_to_day * cls.day_to_week)
        raise ValueError(
            "Wrong attack delay specified. Param delay: '<number>[ms|s|m|h|d|w]' | Example: '90m' or '2w' or '800s'"
        )  # noqa: E501
        # @formatter:on
