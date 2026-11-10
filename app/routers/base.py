from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def hello() -> dict[str, str]:
    return {"message": "Hello, World!"}


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}
