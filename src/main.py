from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.web.service import router as service_router
from src.web.dialog import router as dialog_router

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
    dialog_router,
    prefix="/api/v1/dialog"
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
