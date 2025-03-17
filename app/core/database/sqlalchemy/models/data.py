from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.sqlalchemy.models.base import Base


class Data(Base):
    object: Mapped[str] = mapped_column(String(50), primary_key=True)
    status: Mapped[int]
    level: Mapped[int]
    parent: Mapped[str | None]
    owner: Mapped[str] = mapped_column(String(14))

    def __repr__(self):
        return (
            f"<Data(object={self.object}, status={self.status},"
            f" level={self.level}, parent={self.parent}, owner={self.owner})>"
        )
