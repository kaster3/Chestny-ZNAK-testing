import json
import logging
from typing import Any, cast

from app.core.database.sqlalchemy import Data
from app.core.repositories.data import DataRepository
from app.core.repositories.documents import DocumentRepository

logger = logging.getLogger(__name__)


class ProcessDocumentsInteractor:
    def __init__(
        self, document_repository: DocumentRepository, data_repository: DataRepository
    ) -> None:
        self.document_repository = document_repository
        self.data_repository = data_repository

    async def __call__(self) -> bool:
        try:
            # 1) Получаем первый, необработанный, документ, согласно сортировки (received_at ASC)
            transfer_document = (
                await self.document_repository.get_unprocess_transfer_document_type()
            )
            if not transfer_document:
                logger.info("No unprocessed transfer documents found")
                return False
            logger.debug("Transfer document: %s", transfer_document)
            document_data = json.loads(cast(str, transfer_document.document_data))
            logger.debug("document data: %s", document_data)

            # 2) Получаем объекты из документа, включая содержимое упаковки (дочерний элемент)
            objects = document_data.get("objects", [])
            logger.debug("Objects from document: %s", objects)
            data_models = await self.__get_all_related_objects(objects)

            # 3) начинаем менять данные для объекта Data, проверя условие
            operation_details = document_data.get("operation_details", {})
            await self.__update_data_based_on_operation_details(data_models, operation_details)

            # 4) Отмечаем документ как обработанный
            await self.document_repository.mark_as_processed(transfer_document)

            # 5) Возвращаем результат
            logging.info("Document '%s' processed successfully!", transfer_document.doc_id)
            return True

        except Exception as e:
            logger.error(f"Error processing document: {e}")
            return False

    async def __get_all_related_objects(self, objects: list[str]) -> list[Data]:
        all_objects = []

        for _object in objects:
            # Добавляем саму упаковку
            data = await self.data_repository.get_data_by_object(_object)
            if data:
                all_objects.append(data)
                # Находим все дочерние объекты (содержимое упаковки)
                child_objects = await self.data_repository.get_data_by_parent(_object)
                if child_objects:
                    all_objects.extend(child_objects)

        return all_objects


    async def __update_data_based_on_operation_details(
        self, data_models: list[Data], operation_details: dict[str, dict[str, Any]]
    ) -> None:
        """Обновляет данные в таблице data на основе operation_details"""
        for data in data_models:
            # Флаг, чтобы отслеживать, были ли внесены изменения,
            # чтобы обновить 1 раз, в конце
            updated = False

            # Проверяем каждое поле из operation_details
            for field, values in operation_details.items():
                old_value = values.get("old")
                new_value = values.get("new")

                # Проверяем, совпадает ли текущее значение с old_value и обновляем это поле
                if getattr(data, field) == old_value:
                    setattr(data, field, new_value)
                    updated = True

            if updated:
                await self.data_repository.update_data(data)
