from pydantic_settings import BaseSettings
from pydantic import computed_field

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    PORT: int = 8000
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_NAME: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@localhost:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


settings = Settings()
