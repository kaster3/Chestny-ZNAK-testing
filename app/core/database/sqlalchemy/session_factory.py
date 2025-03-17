from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


class AsyncSessionManager:
    def __init__(self, engine: AsyncEngine) -> None:
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=engine,
            autoflush=False,
            expire_on_commit=False,
        )
