from enum import Enum

from src.config import settings


class HTTPMethod(str, Enum):
    # Supported HTTP methods
    GET = "GET"
    POST = "POST"


BASE_URL = "{}://{}:{}".format(
    settings.OLLAMA_SCHEMA,
    settings.OLLAMA_HOST,
    settings.OLLAMA_PORT
)
LIST_ALL_MODELS_URL = "{}/api/tags".format(BASE_URL)
LIST_ACTIVE_MODELS_URL = "{}/api/ps".format(BASE_URL)
MODEL_PULL_URL = "{}/api/pull".format(BASE_URL)
MODEL_DETAILS_URL = "{}/api/show".format(BASE_URL)
MODEL_GENERATE_URL = "{}/api/generate".format(BASE_URL)
MODEL_CHAT_URL = "{}/api/chat".format(BASE_URL)

SYSTEM_ROLE = "system"
SYSTEM_MESSAGE = "You are a coding assistant. "
"Keep your responses focused on software development and technical topics. "
"Be concise and provide practical code examples when relevant. "
"Limit explanations to 2-3 sentences unless code examples are needed."

USER_ROLE = "user"

ERROR = "error"
ERROR_GETTING_MODELS_LIST = "Error getting models list: {}"
ERROR_VALIDATING_MODELS_LIST = "Error validating models list: {}"
ERROR_PULLING_MODEL = "Error pulling model: {}"
ERROR_GETTING_MODEL_DETAILS = "Error getting model details: {}"
ERROR_MODEL_NOT_FOUND = "Model {}:{} not found"
ERROR_VALIDATING_MODEL_DETAILS = "Error validating model details: {}"

MODEL_LICENSE_KEY = "license"
ERROR_GETTING_MODEL_LICENSE = "Error getting model license: {}"

MODEL_MODELFILE_KEY = "modelfile"
ERROR_GETTING_MODEL_FILE = "Error getting model Modelfile: {}"

MODEL_TEMPLATE_KEY = "template"
ERROR_GETTING_MODEL_TEMPLATE = "Error getting model template: {}"

MODEL_TENSORS_KEY = "tensors"
ERROR_GETTING_MODEL_TENSORS = "Error getting model tensors: {}"

ERROR_REQUESTING_MODEL = "An error occurred while requesting {}"
ERROR_MODEL_RESPONSE_STATUS = "Error response {} while requesting {}"
ERROR_GETTING_MODEL_ANSWER = "Error getting model answer: {}"
