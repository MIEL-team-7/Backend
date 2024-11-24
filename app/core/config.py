from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class ConfigDict:
        env_file = ".env"

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str


settings = Settings()
