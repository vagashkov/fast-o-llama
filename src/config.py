from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import Environment


class Config(BaseSettings):
    """
    Project environment settings storage definition
    """

    APP_VERSION: str = "0.1"
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Config()
