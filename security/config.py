"""
This modules defines a class that inherits a BaseSettings.
It reads a environment  variables from a env file
ref: https://pydantic-docs.helpmanual.io/usage/settings/
"""
from pydantic import BaseSettings


class AuthorizationSettings(BaseSettings):
    """
    It reads environment variables from a .env file. The file path and
    the file encoding must be passed to the Config nested class.
    Args:
        BaseSettings (BaseSettings):
        ref: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    secret_key: str
    algorithm: str
    lifetime: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
