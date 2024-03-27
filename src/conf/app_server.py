from dataclasses import dataclass
from typing import Any, List

import toml

from src.conf.path_manager import PathManager
from src.utils.singleton import Singleton


@dataclass
class AppServer:
    token: str
    server_ip: str
    server_port: int
    server_timeout: int

    @staticmethod
    def parse_toml_config() -> Any:
        """Retrieve the app config stored in the TOML (app_config.toml) configuration file"""
        with open(PathManager().app_config, "r+") as f:
            config = toml.load(f)
        return AppServer(*config["app"]["server"].values())


if __name__ == "__main__":
    print(AppServer.parse_toml_config())
