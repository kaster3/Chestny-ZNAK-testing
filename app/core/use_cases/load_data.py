import logging

from app.core.repositories.load_repository import LoadDataRepository


class LoadDataInteractor:
    def __init__(self, repository: LoadDataRepository) -> None:
        self.repository = repository

    async def load_data(self, data: list[dict]) -> None:
        logging.info("Starting load the data...")
        repository = self.repository
        for item in data:
            await repository.load_data(item)
        logging.info("The data loaded successfully")

    async def load_documents(self, documents: list[dict]) -> None:
        logging.info("Starting load the documents...")
        repository = self.repository
        for document in documents:
            await repository.load_documents(document)
        logging.info("The documents loaded successfully")
