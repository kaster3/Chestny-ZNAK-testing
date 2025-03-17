import logging
import tomllib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Literal


@dataclass
class DatabaseConfig:
    url: str


class LogLevel(str, Enum):
    LOCAL = "LOCAL"
    DEV = "DEV"
    PROD = "PROD"


# Использую этот словарь для сопоставления режима работы приложения, заданный пользователем с
# уровнями логирования в logging
LOG_LEVELS = {
    LogLevel.LOCAL: logging.DEBUG,
    LogLevel.DEV: logging.INFO,
    LogLevel.PROD: logging.INFO,
}


@dataclass
class LoggerConfig:
    log_level: Literal[
        LogLevel.LOCAL,
        LogLevel.DEV,
        LogLevel.PROD,
    ] = (
        LogLevel.PROD
    )  # ставим по умолчанию PROD, чтобы не выкатить DEBUG на прод, забыл указать режим
    format: str = "%(asctime)s - %(levelname)s - %(message)s"


@dataclass
class Settings:
    db: DatabaseConfig
    logger: LoggerConfig


def build_settings(path: Path) -> Settings:
    """Функция для создания настроек, подгружаем из томл файлика значения"""
    with path.open("rb") as file:
        data = tomllib.load(file)

    # Преобразуем строку из конфига в LogLevel, чтобы валидировать значение
    log_level_str = data["logger"]["log_level"].upper()
    log_level = LogLevel(log_level_str)

    return Settings(
        db=DatabaseConfig(url=data["database"]["url"]),
        logger=LoggerConfig(log_level=log_level, format=data["logger"]["format"]),
    )
