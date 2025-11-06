from pydantic import BaseModel
from typing import List

from src.constants import (
    Role, DEFAULT_TEMPERATURE, DEFAULT_STREAM_MODE
)


class LLMGenerationRequest(BaseModel):
    prompt: str


class LLMGenerationResponse(BaseModel):
    text: str


class LLMChatMessage(BaseModel):
    # 'user' is the default role for user chat messages
    role: str = Role.USER
    content: str


class LLMChatRequest(BaseModel):
    messages: List[LLMChatMessage]
    temperature: float = DEFAULT_TEMPERATURE
    stream: bool = DEFAULT_STREAM_MODE


class LLMChatResponse(BaseModel):
    message: LLMChatMessage
    created_at: str
    done: bool
