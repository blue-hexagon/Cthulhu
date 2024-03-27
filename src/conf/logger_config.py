from dataclasses import dataclass
from pathlib import Path
from typing import Any

import toml

from src.conf.path_manager import PathManager


@dataclass
class LoggerConfig:
    file: bool
    console: bool
    level: int
    path: Path = PathManager().out_root
    filename: str = "app_log.txt"

    @staticmethod
    def parse_toml_config() -> Any:
        """Retrieve the logging config stored in the TOML (app_config.toml) configuration file"""
        with open(PathManager().app_config, "r+") as f:
            config = toml.load(f)
        return LoggerConfig(*config["app"]["logger"].values())


if __name__ == "__main__":
    print(LoggerConfig.parse_toml_config())
