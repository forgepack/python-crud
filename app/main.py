import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.config import settings
from app.routers.admin import admin
from app.routers.permission import permission
from app.routers.role import role
from app.routers.user import user

app = FastAPI(
    title="Python CRUD API",
    description="""
    # 🚀 Complete REST API for User, Role, and Permission Management
    
    This API provides comprehensive CRUD operations for managing users, roles, and permissions 
    with JWT-based authentication.
    
    ## Features
    - ✅ User management (CRUD)
    - ✅ Role management (CRUD)
    - ✅ Permission management with soft delete
    - ✅ JWT authentication
    - ✅ Bearer token authorization
    - ✅ Comprehensive API documentation
    
    ## Getting Started
    1. Create first user: POST `/admin/init/create-first-user` (no auth required)
    2. Login: POST `/user/login` to get JWT token
    3. Use token in Authorization header: `Bearer <your_token>`
    
    ## Documentation
    - **API Docs**: This page (Swagger UI)
    - **Alternative**: `/redoc` for ReDoc documentation
    - **Complete Guide**: See ENDPOINTS.md in the repository
    
    ## Authentication
    Most endpoints require JWT Bearer token authentication.
    Include token in header: `Authorization: Bearer eyJhbGciOiJIUzI1NiIs...`
    """,
    version="1.0.0",
    contact={
        "name": "Gadelha TI",
        "url": "https://github.com/gadelhati",
        "email": "gadelhati@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

origins = ["http://127.0.0.1:5173", "http://127.0.0.1", "http://localhost:5173", "http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def home():
    """
    Home endpoint - Returns welcome message
    """
    return {"message": "Welcome Fast API by Gadelha TI", "status": "success"}


@app.get("/health", tags=["Health"])
async def health():
    """
    Health check endpoint - Verifies API is running
    
    Returns:
        - status: "healthy" if API is running correctly
    """
    return {"status": "healthy"}


# Include routers with documentation tags
app.include_router(admin, prefix="/admin", tags=["Admin"])
app.include_router(permission, tags=["Permissions"])
app.include_router(role, tags=["Roles"])
app.include_router(user, tags=["Users"])


def custom_openapi():
    """
    Custom OpenAPI schema with security scheme configuration
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Python CRUD API",
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )

    # Add Bearer token security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token obtained from /user/login endpoint",
        }
    }

    # Apply security scheme to protected routes
    if "paths" in openapi_schema:
        for path_item in openapi_schema["paths"].values():
            for operation in path_item.values():
                if isinstance(operation, dict):
                    # Don't require auth for public endpoints
                    public_paths = [
                        "/health",
                        "/",
                        "/user/login",
                        "/user/swagger",
                        "/admin/init/create-first-user",
                    ]

                    # Check if this is a protected endpoint
                    if operation.get("summary") and not any(
                        pub in str(operation) for pub in public_paths
                    ):
                        operation["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        root_path=settings.root_path,
        reload=settings.reload,
    )
