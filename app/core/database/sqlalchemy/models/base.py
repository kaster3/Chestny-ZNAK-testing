from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from app.utils import camel_case_to_snake_case, pluralize


class Base(DeclarativeBase):
    __abstract__ = True

    # переопределяем базовою metadata потому что у алхимии есть проблема с constraints из-за
    # которых alembic генерирует миграции с их добавлением только на индексы, а на остальные
    # без naming conventions нужно будет вводить вручную
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    # автоматическая генерация имени таблицы на основе название класса (CamelCase -> snake_case)
    # декоратор показывает что нужно сделать это в момент объявление класса, а
    # не создания экземпляра
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{pluralize(camel_case_to_snake_case(cls.__name__))}"
