from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    # Application running modes
    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"

    @property
    def is_developed(self) -> bool:
        return self in (self.DEVELOPMENT, )

    @property
    def is_deployed(self) -> bool:
        return self in (self.PRODUCTION, )


class Config(BaseSettings):
    """
    Project environment settings storage definition
    """

    APP_VERSION: str = "0.1"
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    OLLAMA_SCHEMA: str = "http"
    OLLAMA_HOST: str = "localhost"
    OLLAMA_PORT: str = "11434"

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Config()
