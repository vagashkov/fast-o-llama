from fastapi import FastAPI, APIRouter

from src.constants import HTTPMethod
from src.routes.service import (
    list_all_models,
    list_active_models,
    model_details
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
