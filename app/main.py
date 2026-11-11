import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.admin import admin
from app.routers.permission import permission
from app.routers.role import role
from app.routers.user import user

app = FastAPI(
    title="Python CRUD",
    version="1.0.0",
)

origins = ["http://127.0.0.1:5173", "http://127.0.0.1", "http://localhost:5173", "http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return {"message": "Welcome Fast API by Gadelha TI", "status": "success"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


app.include_router(permission)
app.include_router(role)
app.include_router(admin)
app.include_router(user)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        root_path=settings.root_path,
        reload=settings.reload,
    )
