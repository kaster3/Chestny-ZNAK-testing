from abc import abstractmethod
from datetime import datetime
from typing import Protocol

from sqlalchemy import select

from app.core.database.sqlalchemy import Document
from app.core.repositories.base import Repository


class DocumentRepository(Protocol):
    @abstractmethod
    async def get_all_documents(self) -> list[Document | None]:
        raise NotImplementedError

    @abstractmethod
    async def get_unprocess_transfer_document_type(self) -> Document | None:
        raise NotImplementedError

    @abstractmethod
    async def mark_as_processed(self, document: Document) -> None:
        raise NotImplementedError


class IDocumentRepository(Repository):
    """
    Класс, реализующий интерфейс DocumentRepository, для работы с Data моделью,,
    наследуем init от Repository для получения сессии
    """

    async def get_by_id(self, _id) -> Document | None:
        document = await self.session.get(Document, _id)
        return document

    async def get_all_documents(self) -> list[Document | None]:
        stmt = select(Document).order_by(Document.received_at)
        documents = await self.session.scalars(stmt)
        return list(documents)

    async def get_unprocess_transfer_document_type(self) -> Document | None:
        stmt = (
            select(Document)
            .where(
                Document.document_type == "transfer_document",
                Document.processed_at.is_(None),
            )
            .order_by(Document.received_at)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def mark_as_processed(self, document: Document) -> None:
        document.processed_at = datetime.now()
        self.session.add(document)
        await self.session.commit()
