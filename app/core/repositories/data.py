from abc import abstractmethod
from typing import Protocol

from app.core.database.sqlalchemy import Data
from app.core.repositories.base import Repository


class DataRepository(Protocol):
    @abstractmethod
    async def get_data_by_object(self, _object: str) -> Data | None:
        raise NotImplementedError

    @abstractmethod
    async def update_data(self, data: Data) -> None:
        raise NotImplementedError


class IDataRepository(Repository):
    """
    Класс, реализующий интерфейс DataRepository, для работы с Data моделью,
    наследуем init от Repository для получения сессии
    """

    async def get_data_by_object(self, _object: str) -> Data | None:
        data = await self.session.get(Data, _object)
        return data

    async def update_data(self, data: Data) -> None:
        self.session.add(data)
        await self.session.commit()
