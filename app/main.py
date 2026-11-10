import uvicorn
from fastapi import FastAPI

from app.config import settings
from app.routers.base import router as base_router

app = FastAPI(
    title="Python Template",
    version="1.0.0",
)
app.include_router(base_router)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        root_path=settings.root_path,
        reload=settings.reload,
    )
