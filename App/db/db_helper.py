from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from collections.abc import AsyncGenerator
from App.core.settings import settings


class DataBaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

        self.scoped_session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.scoped_session
        try:
            yield session
        finally:
            await session.remove()

db_helper = DataBaseHelper(
    url=settings.url,
    echo=settings.echo,
)
