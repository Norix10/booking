from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from core.settings import settings


class DataBaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
            autocommit=False,
        )


db_helper = DataBaseHelper(
    url=settings.url,
    echo=settings.echo,
)

