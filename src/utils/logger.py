import logging

from src.conf.logger_config import LoggerConfig, parse_toml_logger_config
from src.utils.singleton import Singleton


class Logger(metaclass=Singleton):
    LOGGER_NAME = 'dual_logger'
    FILE_HANDLER = 'file_handler'
    CONSOLE_HANDLER = 'console_handler'
    L_NOTSET = 0
    L_DEBUG = 10
    L_INFO = 20
    L_WARNING = 30
    L_ERROR = 40
    L_CRITICAL = 50

    def __init__(self) -> None:
        Logger.configure_logger()

    @classmethod
    def inverse_level(cls, level: int) -> int:
        if level == 0:
            return cls.L_NOTSET
        elif level == 10:
            return cls.L_CRITICAL
        elif level == 20:
            return cls.L_ERROR
        elif level == 30:
            return cls.L_WARNING
        elif level == 40:
            return cls.L_INFO
        elif level == 50:
            return cls.L_DEBUG
        else:
            raise ValueError("`level` must be increments of 10 between 0 and 50.")

    @classmethod
    def configure_logger(cls, log_config: LoggerConfig = parse_toml_logger_config()) -> None:
        logger = logging.getLogger(Logger.LOGGER_NAME)
        logger.setLevel(log_config.level)
        if log_config.file:
            if not cls.__has_handler(cls.FILE_HANDLER):
                file_handler = logging.FileHandler(log_config.filename)
                file_handler.setLevel(log_config.level)
                file_formatter = logging.Formatter('[%(levelname)s:%(asctime)s] %(message)s')
                file_handler.setFormatter(file_formatter)
                file_handler.set_name(cls.FILE_HANDLER)
                logger.addHandler(file_handler)
            else:
                handler = cls.__get_handler(cls.FILE_HANDLER)
                handler.setLevel(log_config.level)
        if log_config.console:
            if not cls.__has_handler(cls.CONSOLE_HANDLER):
                console_handler = logging.StreamHandler()
                console_handler.setLevel(log_config.level)
                console_formatter = logging.Formatter('[%(levelname)s:%(asctime)s] %(message)s')
                console_handler.setFormatter(console_formatter)
                console_handler.set_name(cls.CONSOLE_HANDLER)
                logger.addHandler(console_handler)
            else:
                handler = cls.__get_handler(cls.CONSOLE_HANDLER)
                handler.setLevel(log_config.level)
        if False:
            """ Test logger """
            get_logger().debug("debug")
            get_logger().info("info")
            get_logger().warning("warn")
            get_logger().error("error")
            get_logger().critical("crit")

    @classmethod
    def __has_handler(cls, handler_name: str) -> bool:
        specific_handler_found = False
        for handler in get_logger().handlers:
            if handler.get_name() == handler_name:
                specific_handler_found = True
                break
        return specific_handler_found

    @classmethod
    def __get_handler(cls, handler_name: str) -> logging.Handler | None:
        specific_handler = None
        for handler in get_logger().handlers:
            if handler.get_name() == handler_name:
                specific_handler = handler
                break
        return specific_handler

    @staticmethod
    def configure_logger_set_level(level: int) -> None:
        inverse_level = Logger.inverse_level(level)
        get_logger().debug(f"Inverse level: {inverse_level}")
        get_logger().debug(f"Previous logger level was: {inverse_level}")
        logging.getLogger(Logger.LOGGER_NAME).setLevel(inverse_level)
        logging.getLogger(Logger.CONSOLE_HANDLER).setLevel(inverse_level)
        logging.getLogger(Logger.FILE_HANDLER).setLevel(inverse_level)
        logging.getLogger("dual_logger").setLevel(inverse_level)
        get_logger().debug(f"New logger level is: {logging.getLogger('dual_logger').getEffectiveLevel()}")


def get_logger() -> logging.Logger:
    return logging.getLogger(Logger.LOGGER_NAME)


if __name__ == '__main__':
    logger = Logger()
    get_logger().debug("Debug")
    get_logger().info("Info")
    get_logger().warning("Warning")
    get_logger().error("Error")
    get_logger().critical("Critical")
