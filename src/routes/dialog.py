from json import loads, dumps, JSONDecodeError

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from httpx import AsyncClient, RequestError, HTTPStatusError

from src.constants import (
    HTTPMethod,
    MODEL_GENERATE_URL, MODEL_CHAT_URL,
    SYSTEM_ROLE, SYSTEM_MESSAGE,
    ERROR_REQUESTING_MODEL,
    ERROR_MODEL_RESPONSE_STATUS,
    ERROR_GETTING_MODEL_ANSWER
)
from src.schemas import (
    GenerationRequest,
    GenerationResponse,
    ChatRequest
)
from src.utils import report_error


router = APIRouter()


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

        return GenerationResponse(text=full_text)

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


async def chat(
        model_name: str,
        version: str,
        request: ChatRequest
):
    """
    Enables stream chat support
    :param model_name
    :param version
    :param request:
    :return:
    """

    async def generate():
        """
        LLM response generator function
        :return:
        """
        try:
            async with AsyncClient() as client:
                # Define system message to begin the dialog
                system_message = {
                    "role": SYSTEM_ROLE,
                    "content": SYSTEM_MESSAGE,
                }

                # Build messages pool
                messages = [
                               system_message
                           ] + [
                    msg.dict() for msg in request.messages
                ]

                # Build request
                request_data = {
                    "model": "{}:{}".format(model_name, version),
                    "messages": messages,
                    "stream": True,
                    "temperature": request.temperature,
                }

                # Send message to LLM
                async with client.stream(
                    "POST",
                    MODEL_CHAT_URL,
                    json=request_data,
                    timeout=60.0
                ) as response:
                    # Something went wrong
                    if not response.is_success:
                        error_msg = await response.text()
                        yield f'data: {{"error": "{error_msg}"}}\n\n'
                        return

                    # Processing response line by line
                    async for line in response.aiter_lines():
                        # Check if line is not empty
                        if line.strip():
                            try:
                                data = loads(line)
                                if (
                                        "message" in data
                                ) and (
                                        "content" in data["message"]
                                ):
                                    yield f"data: {dumps(data)}\n\n"
                            except JSONDecodeError:
                                continue
                    yield "data: [DONE]\n\n"
        # except RequestError as exc:
        #     report_error(ERROR_REQUESTING_MODEL.format(exc.request.url))
        # except HTTPStatusError as exc:
        #     report_error(
        #         ERROR_MODEL_RESPONSE_STATUS.format(
        #             exc.response.status_code,
        #             exc.request.url
        #             )
        #         )
        except Exception as exc:
            yield f'data: {{"error": "{str(exc)}"}}\n\n'

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


router.add_api_route(
    "/models/{model_name}/{version}/generate",
    endpoint=generate_text,
    methods=[HTTPMethod.POST],
    summary="Processes single text generation request"
)

router.add_api_route(
    "/models/{model_name}/{version}/chat",
    endpoint=chat,
    methods=[HTTPMethod.POST],
    summary="Processes stream chat request"
)
