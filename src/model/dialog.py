from pydantic import BaseModel
from typing import List

from src.constants import USER_ROLE


class GenerationRequest(BaseModel):
    prompt: str


class GenerationResponse(BaseModel):
    text: str


class ChatMessage(BaseModel):
    role: str = USER_ROLE
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    temperature: float = 0.7
    stream: bool = True


class ChatResponse(BaseModel):
    message: ChatMessage
    created_at: str
    done: bool = True
