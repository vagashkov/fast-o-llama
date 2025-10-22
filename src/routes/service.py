import logging

from http import HTTPStatus
from httpx import AsyncClient
from pydantic import ValidationError as PydanticError

from src.constants import (
    LIST_ALL_MODELS_URL, LIST_ACTIVE_MODELS_URL,
    ERROR_GETTING_MODELS_LIST, ERROR_VALIDATING_MODELS_LIST,
    MODEL_DETAILS_URL, ERROR_MODEL_NOT_FOUND,
    ERROR_GETTING_MODEL_DETAILS, ERROR_VALIDATING_MODEL_DETAILS,
    MODEL_LICENSE_KEY, ERROR_GETTING_MODEL_LICENSE,
    MODEL_MODELFILE_KEY, ERROR_GETTING_MODEL_FILE,
    MODEL_TEMPLATE_KEY, ERROR_GETTING_MODEL_TEMPLATE,
    MODEL_TENSORS_KEY, ERROR_GETTING_MODEL_TENSORS
)
from src.schemas import LLModelsList, LLMFullDetails
from src.utils import report_error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def list_models(active: bool = False) -> LLModelsList:
    """
    Returns LLMs list (all or active only)
    :return:
    """

    # Define necessary inference engine endpoint
    url = LIST_ACTIVE_MODELS_URL if active else LIST_ALL_MODELS_URL

    # Getting models list from inference engine
    try:
        async with AsyncClient() as client:
            response = await client.get(
                url
            )
    except Exception as e:
        report_error(ERROR_GETTING_MODELS_LIST.format(e))

    models_list = response.json()

    # Validate received data
    try:
        LLModelsList.model_validate(
            models_list
        )
    except PydanticError as e:
        report_error(ERROR_VALIDATING_MODELS_LIST.format(e))

    # Return result
    return LLModelsList(**models_list)


async def list_all_models() -> LLModelsList:
    """
    Returns all available LLMs (incl. aliases)
    :return:
    """

    return await list_models(active=False)


async def list_active_models() -> LLModelsList:
    """
    Returns active LLMs (incl. aliases)
    :return:
    """

    return await list_models(active=True)


async def get_model_data(
        model_name: str,
        version: str,
        verbose: bool = False
) -> dict:
    """
    Returns designated LLM details
    :param model_name:
    :param version
    :param verbose:
    :return dict
    """

    try:
        async with AsyncClient() as client:
            response = await client.post(
                MODEL_DETAILS_URL,
                json={
                    "model": "{}:{}".format(model_name, version),
                    "verbose": verbose
                }
            )
    except Exception as e:
        # Check if designated model is not found
        if response.status_code == HTTPStatus.NOT_FOUND:
            report_error(
                ERROR_MODEL_NOT_FOUND.format(
                    model_name, version
                )
            )

        # Any other error
        report_error(
            ERROR_GETTING_MODEL_DETAILS.format(e)
        )

    return response.json()


async def model_details(
        model_name: str,
        version: str,
        verbose: bool = False
):
    """
    Returns designated LLM details
    :param model_name:
    :param version
    :param verbose:
    :return:
    """

    # Extract and validate model description
    model_data = await get_model_data(model_name, version, verbose)

    try:
        LLMFullDetails.model_validate(
            model_data
        )
    except PydanticError as e:
        report_error(
            ERROR_VALIDATING_MODEL_DETAILS.format(e)
        )

    # Return results
    return LLMFullDetails(**model_data)


async def model_license(
        model_name: str,
        version: str
):
    """
    Returns designated LLM usage license
    :param model_name:
    :param version
    :return:
    """

    # Extract and validate model description
    model_data = await get_model_data(model_name, version, False)

    # Check if response contains license data
    if MODEL_LICENSE_KEY not in model_data:
        report_error(
            ERROR_GETTING_MODEL_LICENSE.format(
                "{}:{}".format(model_name, version)
            )
        )

    # Return results
    return {
        MODEL_LICENSE_KEY:
            model_data.get(MODEL_LICENSE_KEY)
    }


async def model_modelfile(
        model_name: str,
        version: str
):
    """
    Returns designated LLM modelfile content
    :param model_name:
    :param version
    :return:
    """

    # Extract and validate model description
    model_data = await get_model_data(model_name, version, False)

    # Check if response contains modelfile
    if MODEL_MODELFILE_KEY not in model_data:
        report_error(
            ERROR_GETTING_MODEL_FILE.format(
                "{}:{}".format(model_name, version)
            )
        )

    return {
        MODEL_MODELFILE_KEY:
        model_data.get(MODEL_MODELFILE_KEY)
    }


async def model_template(
        model_name: str,
        version: str
):
    """
    Returns designated LLM template
    :param model_name:
    :param version
    :return:
    """

    # Extract and validate model description
    model_data = await get_model_data(model_name, version, False)

    # Check if response contains template
    if MODEL_TEMPLATE_KEY not in model_data:
        report_error(
            ERROR_GETTING_MODEL_TEMPLATE.format(
                "{}:{}".format(model_name, version)
            )
        )

    return {
        MODEL_TEMPLATE_KEY:
        model_data.get(MODEL_TEMPLATE_KEY)
    }


async def model_tensors(
        model_name: str,
        version: str
):
    """
    Returns designated LLM tensors
    :param model_name:
    :param version
    :return:
    """

    # Extract and validate model description
    model_data = await get_model_data(model_name, version, False)

    # Check if response contains tensors
    if MODEL_TENSORS_KEY not in model_data:
        report_error(
            ERROR_GETTING_MODEL_TENSORS.format(
                "{}:{}".format(model_name, version)
            )
        )

    return {
        MODEL_TENSORS_KEY:
        model_data.get(MODEL_TENSORS_KEY)
    }
