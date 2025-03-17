from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.sqlalchemy.models.base import Base


class Document(Base):
    doc_id: Mapped[str] = mapped_column(primary_key=True)
    received_at: Mapped[datetime | None] = mapped_column(DateTime)
    document_type: Mapped[str]
    document_data: Mapped[dict] = mapped_column(JSONB)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime)

    def __repr__(self):
        return (
            f"<Documents(doc_id={self.doc_id}, received_at={self.received_at},"
            f" document_type={self.document_type}, document_data={self.document_data},"
            f" processed_at={self.processed_at})>"
        )
