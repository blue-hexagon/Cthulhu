from dataclasses import dataclass
from typing import Any, List

import toml

from src.conf.path_manager import PathManager
from src.utils.singleton import Singleton


@dataclass
class AppLoadBalancer:
    use_scaling: bool
    scale_up_interval: int
    scale_down_interval: int
    window_start_size_bits: int
    window_max_size_bits: int

    @staticmethod
    def parse_toml_config() -> Any:
        """Retrieve the app config stored in the TOML (app_config.toml) configuration file"""
        with open(PathManager().app_config, "r+") as f:
            config = toml.load(f)
        return AppLoadBalancer(*config["app"]["load_balancer"].values())


if __name__ == "__main__":
    print(AppLoadBalancer.parse_toml_config())
