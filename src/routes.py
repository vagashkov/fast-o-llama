import logging

from http import HTTPStatus
from httpx import get, post
from pydantic import ValidationError as PydanticError

from src.constants import BASE_URL
from src.validators import LLModel


async def list_all_models():
    """
    Returns all available LLMs (incl. aliases)
    :return:
    """
    response = get(
        "{}/api/tags".format(BASE_URL)
    )

    if not response.status_code == HTTPStatus.OK:
        response.raise_for_status()

    # Validate LLM data received from ollama
    for model_data in response.json().get("models"):
        try:
            LLModel.model_validate(
                model_data
                )
        except PydanticError as e:
            logging.log(
                logging.ERROR,
                e
            )

    # Return LLM aliases list
    return {
        "models": [
            model_data.get("name")
            for model_data
            in response.json().get("models")
            ]
        }


async def list_active_models():
    """
    Returns only active LLMs list
    :return:
    """
    response = get(
        "{}/api/ps".format(BASE_URL)
    )

    if not response.status_code == HTTPStatus.OK:
        response.raise_for_status()

    # Validate LLM data received from ollama
    for model_data in response.json().get("models"):
        try:
            LLModel.model_validate(
                model_data
                )
        except PydanticError as e:
            logging.log(
                logging.ERROR,
                e
            )

    # Return LLM aliases list
    return {
        "models": [
            model_data.get("name")
            for model_data
            in response.json().get("models")
            ]
        }


async def model_details(
        model_name: str,
        version: str = "latest",
        verbose: bool = False
):
    """
    Returns designated LLM details
    :param model_name:
    :param version
    :param verbose:
    :return:
    """

    response = post(
        "{}/api/show".format(BASE_URL),
        data={
            "model": "{}:{}".format(model_name, version),
            "verbose": verbose
        }
    )

    if not response.status_code == HTTPStatus.OK:
        response.raise_for_status()

    return {
        "model_details": response.json()
    }
