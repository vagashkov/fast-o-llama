from fastapi import FastAPI, APIRouter

from src.constants import HTTPMethod
from src.routes.service import (
    list_all_models,
    list_active_models,
    model_details, model_license,
    model_modelfile, model_template, model_tensors
)
from src.routes.conversation import (
    generate_text
)

app = FastAPI()
router = APIRouter

app.add_api_route(
    "/models",
    endpoint=list_all_models,
    methods=[HTTPMethod.GET],
    summary="Returns all available LLMs (incl. aliases)"
)

app.add_api_route(
    "/models/active",
    endpoint=list_active_models,
    methods=[HTTPMethod.GET],
    summary="Returns active LLMs only (incl. aliases)"
)

app.add_api_route(
    "/models/{model_name}/{version}",
    endpoint=model_details,
    methods=[HTTPMethod.GET],
    summary="Returns designated LLM details"
)

app.add_api_route(
    "/models/{model_name}/{version}/license",
    endpoint=model_license,
    methods=[HTTPMethod.GET],
    summary="Returns designated LLM license information"
)

app.add_api_route(
    "/models/{model_name}/{version}/modelfile",
    endpoint=model_modelfile,
    methods=[HTTPMethod.GET],
    summary="Returns designated LLM modelfile content"
)

app.add_api_route(
    "/models/{model_name}/{version}/template",
    endpoint=model_template,
    methods=[HTTPMethod.GET],
    summary="Returns designated LLM template"
)

app.add_api_route(
    "/models/{model_name}/{version}/tensors",
    endpoint=model_tensors,
    methods=[HTTPMethod.GET],
    summary="Returns designated LLM tensors"
)

app.add_api_route(
    "/models/{model_name}/{version}/generate",
    endpoint=generate_text,
    methods=[HTTPMethod.POST],
    summary="Processes single text generation request"
)
