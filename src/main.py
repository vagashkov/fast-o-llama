from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.service import service_router
from src.routes.conversation import conversation_router

app = FastAPI(title="Ollama connector for RAG support")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    service_router,
    prefix="/api/v1/service"
)
app.include_router(
    conversation_router,
    prefix="/api/v1/conversation"
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
