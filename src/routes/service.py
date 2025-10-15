import logging

from fastapi import HTTPException
from http import HTTPStatus
from httpx import AsyncClient
from pydantic import ValidationError as PydanticError

from src.constants import (
    LIST_ALL_MODELS_URL, LIST_ACTIVE_MODELS_URL,
    ERROR_GETTING_MODELS_LIST, ERROR_VALIDATING_MODELS_LIST,
    MODEL_DETAILS_URL, ERROR_MODEL_NOT_FOUND,
    ERROR_GETTING_MODEL_DETAILS, ERROR_VALIDATING_MODEL_DETAILS
)
from src.schema import LLModelsList, LLMFullDetails

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
        logger.error(
            ERROR_GETTING_MODELS_LIST.format(e)
        )
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    models_list = response.json()

    # Validate received data
    try:
        LLModelsList.model_validate(
            models_list
        )
    except PydanticError as e:
        logger.error(
            ERROR_VALIDATING_MODELS_LIST.format(e)
        )

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
            error = ERROR_MODEL_NOT_FOUND.format(model_name, version)
            logger.error(error)
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=error
            )
        # Any other error
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=ERROR_GETTING_MODEL_DETAILS.format(e)
        )

    # Extract and validate model description
    model_data = response.json()
    try:
        LLMFullDetails.model_validate(
            model_data
        )
    except PydanticError as e:
        logging.log(
            logging.ERROR,
            ERROR_VALIDATING_MODEL_DETAILS.format(e)
        )

    # Return results
    return LLMFullDetails(**model_data)
