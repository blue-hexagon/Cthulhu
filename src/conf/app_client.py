from dataclasses import dataclass
from typing import Any, List, Self

import toml

from src.conf.path_manager import PathManager
from src.utils.singleton import Singleton


@dataclass
class AppClient:
    token: str
    server_ip: str
    server_port: int
    nodes: List[str]
    node_timeout: int

    @staticmethod
    def parse_toml_config() -> Any:
        """Retrieve the app config stored in the TOML (app_config.toml) configuration file"""
        with open(PathManager().app_config, "r+") as f:
            config = toml.load(f)
        return AppClient(*config["app"]["client"].values())


if __name__ == "__main__":
    print(AppClient.parse_toml_config())
