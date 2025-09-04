from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    url: str = (
        "postgresql+asyncpg://neondb_owner:npg_C3r1NDJZLQkf@ep-sparkling-mouse-ag7671ju-pooler.c-2.eu-central-1.aws.neon.tech/neondb"
    )
    echo: bool = False


settings = Settings()
