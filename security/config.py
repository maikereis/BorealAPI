from pydantic import BaseSettings


class AuthorizationSettings(BaseSettings):
    secret_key: str
    algorithm: str
    lifetime: int = 30

    class Config():
        env_file = '.env'
        env_file_encoding = 'utf-8'
