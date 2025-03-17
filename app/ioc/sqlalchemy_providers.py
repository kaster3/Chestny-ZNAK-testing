from typing import AsyncGenerator

from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.core.database.sqlalchemy.engine import AsyncDatabaseEngine
from app.core.database.sqlalchemy.session_factory import AsyncSessionManager
from app.core.repositories.data import DataRepository, IDataRepository
from app.core.repositories.documents import DocumentRepository, IDocumentRepository
from app.core.repositories.load_repository import ILoadDataRepository, LoadDataRepository
from app.core.settings import Settings
from app.core.use_cases.load_data import LoadDataInteractor
from app.core.use_cases.proccess_document import ProcessDocumentsInteractor


class SQLAlchemyProvider(Provider):
    scope = Scope.APP
    settings = from_context(Settings)

    @provide
    async def get_async_engine(self, settings: Settings) -> AsyncEngine:
        db_engine = AsyncDatabaseEngine(
            url=settings.db.url,
        )
        return db_engine.engine

    @provide
    async def get_async_session_manager(
        self,
        engine: AsyncEngine,
    ) -> AsyncSessionManager:
        return AsyncSessionManager(engine=engine)

    @provide(scope=Scope.REQUEST)
    async def get_async_session(
        self,
        session_manager: AsyncSessionManager,
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_manager.session_factory() as session:
            yield session


class DataLoadProvider(Provider):
    scope = Scope.REQUEST

    load_repository = provide(ILoadDataRepository, provides=LoadDataRepository)
    service = provide(LoadDataInteractor)


class ProcessDocumentsProvider(Provider):
    scope = Scope.REQUEST

    data_repository = provide(IDataRepository, provides=DataRepository)
    document_repository = provide(IDocumentRepository, provides=DocumentRepository)
    service = provide(ProcessDocumentsInteractor)
