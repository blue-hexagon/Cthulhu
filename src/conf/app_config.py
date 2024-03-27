from dataclasses import dataclass
from typing import Any, Self

import toml

from src.conf.path_manager import PathManager


@dataclass
class AppConfig:
    token: str
    host_ip: str
    host_port: int
    remote_ip: str
    remote_port: int

    @staticmethod
    def parse_toml_config() -> Any:
        """Retrieve the app config stored in the TOML (app_config.toml) configuration file"""
        with open(PathManager().app_config, "r+") as f:
            config = toml.load(f)
        return AppConfig(*config["app"]["setup"].values())
