from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = '.env'

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str


settings = Settings()
