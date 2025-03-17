from dishka import AsyncContainer, make_async_container

from app.core.settings import Settings
from app.ioc.sqlalchemy_providers import (
    DataLoadProvider,
    ProcessDocumentsProvider,
    SQLAlchemyProvider,
)


def init_container(settings: Settings = None) -> AsyncContainer:
    container = make_async_container(
        SQLAlchemyProvider(),
        DataLoadProvider(),
        ProcessDocumentsProvider(),
        context={
            Settings: settings,
        },
    )
    return container
