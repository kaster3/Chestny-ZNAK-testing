import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from app import CONFIG_PATH
from app.core.logger.init_logger import init_logger
from app.core.settings import build_settings
from app.core.use_cases.proccess_document import ProcessDocumentsInteractor
from app.ioc.init_container import init_container


@asynccontextmanager
async def lifespan(settings) -> None:
    """
    Инициализируем логер c нашим конфигом и ioc контейнер с зависимостями, а также правильно
    освобождаем ресурсы.
    """
    init_logger(settings=settings.logger)
    container = init_container(settings=settings)
    logging.info("Application started successfully!")

    yield container

    logging.info("Closing the application...")
    await container.close()
    logging.info("Application closed successfully!")


async def main(config_path: Path) -> None:
    """
    Загружаем наш конфиг для логера и бд, открываем контекст для управления ресурсами
    и выполняем в нем нашу логику.
    """
    settings = build_settings(config_path)
    async with lifespan(settings) as container:
        logging.debug("Start some application logic")

        async with container() as request_container:
            process_interactor: ProcessDocumentsInteractor = await request_container.get(
                ProcessDocumentsInteractor
            )
            # Обрабатываем только один (первый по условию) документ, согласно заданию
            await process_interactor()

        logging.debug("End some application logic")


if __name__ == "__main__":
    asyncio.run(main(Path(CONFIG_PATH)))
