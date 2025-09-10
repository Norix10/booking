from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path

BASEDIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASEDIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASEDIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    url: str = (
        "postgresql+asyncpg://neondb_owner:npg_C3r1NDJZLQkf@ep-sparkling-mouse-ag7671ju-pooler.c-2.eu-central-1.aws.neon.tech/neondb"
    )
    echo: bool = False
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
