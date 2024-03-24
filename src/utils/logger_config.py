from dataclasses import dataclass
from pathlib import Path
import toml

from src.conf.path_manager import PathManager


@dataclass
class LoggerConfig:
    file: bool
    console: bool
    level: int
    path: Path = PathManager().out_root
    filename: str = "app_log.txt"


def parse_toml_logger_config() -> LoggerConfig:
    """ Retrieve the logging config stored in the TOML (config.toml) configuration file """
    with open(PathManager().app_config, 'r+') as f:
        config = toml.load(f)
    return LoggerConfig(*config['app']['logger'].values())


if __name__ == '__main__':
    print(parse_toml_logger_config())
