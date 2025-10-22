from httpx import AsyncClient, RequestError, HTTPStatusError
from json import loads, JSONDecodeError

from src.constants import (
    MODEL_GENERATE_URL,
    ERROR_REQUESTING_MODEL,
    ERROR_MODEL_RESPONSE_STATUS,
    ERROR_GETTING_MODEL_ANSWER
)
from src.schemas import (
    GenerationRequest, GenerationResponse
)
from src.utils import report_error


async def generate_text(
        model_name: str,
        version: str,
        request: GenerationRequest
):
    """
    Processes single text generation request
    :param model_name:
    :param version
    :param request:
    :return:
    """

    try:
        async with AsyncClient() as client:
            response = await client.post(
                MODEL_GENERATE_URL,
                # timeout is big enough to load LLM into memory
                timeout=10.0,
                json={
                    "model": "{}:{}".format(model_name, version),
                    "prompt": request.prompt,
                    "stream": True
                },
            )
            response.raise_for_status()

        full_text = ""

        # Split the response text into lines and process each one
        for line in response.text.split("\n"):
            # Empty line
            if not line.strip():
                continue

            # Got some answer chunk - let's analyze it
            try:
                # Concise answer part
                data = loads(line)
                if "response" in data:
                    full_text += data["response"]
            except JSONDecodeError:
                # Some gibberish - skip it
                continue
    except RequestError as exc:
        report_error(ERROR_REQUESTING_MODEL.format(exc.request.url))
    except HTTPStatusError as exc:
        report_error(ERROR_MODEL_RESPONSE_STATUS.format(
            exc.response.status_code,
            exc.request.url
            )
        )
    except Exception as e:
        report_error(ERROR_GETTING_MODEL_ANSWER.format(e))

    return GenerationResponse(text=full_text)
