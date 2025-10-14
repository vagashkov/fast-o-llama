import logging

from fastapi import HTTPException
from http import HTTPStatus
from httpx import get, post
from pydantic import ValidationError as PydanticError

from src.constants import BASE_URL
from src.validators import LLModel, LLMFullDetails


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
            {
                "name": model_data.get("name").split(":")[0],
                "version": model_data.get("name").split(":")[1]
            }
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
            {
                "name": model_data.get("name").split(":")[0],
                "version": model_data.get("name").split(":")[1]
            }
            for model_data
            in response.json().get("models")
        ]
    }


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

    response = post(
        "{}/api/show".format(BASE_URL),
        json={
            "model": "{}:{}".format(model_name, version),
            "verbose": verbose
        }
    )

    if not response.status_code == HTTPStatus.OK:
        # Process 'wrong model name/version' case
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="The model {}:{} is not found".format(
                    model_name, version
                )
            )
        # Escalate other cases
        response.raise_for_status()

    try:
        LLMFullDetails.model_validate(
            response.json()
        )
    except PydanticError as e:
        logging.log(
            logging.ERROR,
            e
        )

    return {
        "model_info": response.json().get("model_info"),
        "parameters": response.json().get("parameters")
    }
