from abc import abstractmethod
from typing import Protocol

from app.core.database.sqlalchemy import Data, Document
from app.core.repositories.base import Repository


class LoadDataRepository(Protocol):
    @abstractmethod
    async def load_data(self, data: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    async def load_documents(self, documents: dict) -> None:
        raise NotImplementedError


class ILoadDataRepository(Repository):
    """
    Класс, реализующий интерфейс LoadDataRepository, для загрузки data и documents в базу данных,
    наследуем init от Repository для получения сессии
    """

    async def load_data(self, data: dict) -> None:
        data = Data(**data)
        self.session.add(data)
        await self.session.commit()

    async def load_documents(self, documents: dict) -> None:
        data = Document(**documents)
        self.session.add(data)
        await self.session.commit()
