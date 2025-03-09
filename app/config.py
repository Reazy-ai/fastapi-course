import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "../.env")

settings = Settings()

