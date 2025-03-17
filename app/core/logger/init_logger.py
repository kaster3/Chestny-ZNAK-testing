import logging

from app.core.settings import LOG_LEVELS, LoggerConfig


def init_logger(settings: LoggerConfig) -> None:
    """
    Инициализируем логер с полученными настройками и выводим его режим работы (LOCAL, DEV, PROD),
    сопоставив с режимом из logging
    """
    log_level = LOG_LEVELS.get(settings.log_level)
    logging.basicConfig(
        level=log_level,
        format=settings.format,
    )
    logging.info("Starting the application in %s MODE...", settings.log_level.value)
