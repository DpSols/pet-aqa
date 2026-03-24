import sys

from loguru import logger


def configure_logging() -> None:
    logger.remove()
    logger.add(
        sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
    )


def get_logger(name: str) -> logger:
    return logger.bind(logger_name=name)
