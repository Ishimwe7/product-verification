from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mysql_url: str
    mongo_url: str

    class Config:
        env_file = ".env"

settings = Settings()