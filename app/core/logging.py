import sys
from pathlib import Path

from loguru import logger

from app.core.config import settings

LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def setup_logging() -> None:
    logger.remove()

    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    file_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
        "{name}:{function}:{line} - {message}"
    )

    logger.add(
        sys.stdout,
        format=console_format,
        level="DEBUG" if settings.DEBUG else "INFO",
        colorize=True,
    )

    logger.add(
        LOG_DIR / "app_{time:YYYY-MM-DD}.log",
        format=file_format,
        level="DEBUG",
        rotation="1 day",
        retention="30 days",
        compression="gz",
        enqueue=True,
    )

    logger.add(
        LOG_DIR / "error_{time:YYYY-MM-DD}.log",
        format=file_format,
        level="ERROR",
        rotation="1 day",
        retention="30 days",
        compression="gz",
        enqueue=True,
    )

    logger.info("Loguru logging configured | log_dir={}", LOG_DIR)
