from enum import Enum


class HTTPMethod(str, Enum):
    # Supported HTTP methods
    GET = "GET"
    POST = "POST"


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


OLLAMA_SCHEMA = "http"
OLLAMA_HOST = "localhost"
OLLAMA_PORT = "11434"

BASE_URL = "{}://{}:{}".format(
    OLLAMA_SCHEMA, OLLAMA_HOST, OLLAMA_PORT
)
LIST_ALL_MODELS_URL = "{}/api/tags".format(BASE_URL)
LIST_ACTIVE_MODELS_URL = "{}/api/ps".format(BASE_URL)
MODEL_DETAILS_URL = "{}/api/show".format(BASE_URL)

ERROR = "error"
ERROR_GETTING_MODELS_LIST = "Error getting models list: {}"
ERROR_VALIDATING_MODELS_LIST = "Error validating models list: {}"
ERROR_GETTING_MODEL_DETAILS = "Error getting model details: {}"
ERROR_MODEL_NOT_FOUND = "Model {}:{} not found"
ERROR_VALIDATING_MODEL_DETAILS = "Error validating model details: {}"
