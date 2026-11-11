from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.base import ResponseError, SchemaSwagger
from app.schemas.user import DTOUserCreate, DTOUserRetrieve, DTOUserUpdate
from app.services.user import ServiceUser

user = APIRouter(prefix="/user", tags=["user"])


@user.post("/swagger", status_code=200)
async def create_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    try:
        print(form_data)
        return ResponseError(code=200, status="Ok", message="Ok", validationErrors="_result").dict(
            exclude_none=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@user.post("/login", status_code=200, summary="Authenticate user and get JWT token")
async def login(request: SchemaSwagger, db: Session = Depends(get_db)):
    """
    Authenticate user with username and password.

    Returns a JWT token that must be included in the Authorization header for protected endpoints.

    **Parameters:**
    - **username** (string): User's username
    - **password** (string): User's password

    **Returns:**
    - **access_token**: JWT token to use in Authorization header
    - **token_type**: "bearer"

    **Example:**
    ```json
    {
      "code": 200,
      "status": "Ok",
      "validationErrors": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
      }
    }
    ```
    """
    try:
        _result = ServiceUser.authenticate_user(db, request.username, request.password)
        return ResponseError(code=200, status="Ok", message="Ok", validationErrors=_result).dict(
            exclude_none=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@user.post("/", status_code=201, summary="Create a new user")
async def create_user(
    request: DTOUserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(ServiceUser.get_current_user),
):
    """
    Create a new user in the system.

    **Requires authentication:** Bearer token from /user/login endpoint

    **Parameters:**
    - **username** (string): Unique username
    - **email** (string): User's email address
    - **password** (string): Secure password
    - **full_name** (string): User's full name

    **Returns:**
    - Created user object with id, username, email, and full_name

    **Status Codes:**
    - 201: User created successfully
    - 400: Invalid input data
    - 401: Authentication required
    - 500: Server error
    """
    try:
        _result = ServiceUser.create(db, created=request)
        return ResponseError(
            code=201, status="Created", message="Created", validationErrors=_result
        ).dict(exclude_none=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@user.patch("/", status_code=202)
async def cancel(request: DTOUserRetrieve, db: Session = Depends(get_db)):
    try:
        _result = DTOUserRetrieve.cancel(db, cancelled=request)
        return ResponseError(
            code=202, status="Accepted", message="Cancelled", validationErrors=_result
        ).dict(exclude_none=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@user.get("/", status_code=200, summary="List all users")
async def get(
    db: Session = Depends(get_db), current_user: dict = Depends(ServiceUser.get_current_user)
):
    """
    Retrieve all users from the system.

    **Requires authentication:** Bearer token from /user/login endpoint

    **Query Parameters:**
    - **page** (int, optional): Page number (default: 1)
    - **limit** (int, optional): Items per page (default: 20, max: 100)

    **Returns:**
    - List of user objects with pagination info

    **Status Codes:**
    - 200: Users retrieved successfully
    - 401: Authentication required
    - 500: Server error
    """
    try:
        _result = ServiceUser.get(db, 0, 100)
        return ResponseError(
            code=200, status="Ok", message="Finded all", validationErrors=_result
        ).dict(exclude_none=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@user.get("/{id}", status_code=200, summary="Get user by ID")
async def get_by_id(id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve a specific user by their ID.

    **Path Parameters:**
    - **id** (UUID): User's unique identifier

    **Returns:**
    - User object with id, username, email, full_name, and metadata

    **Status Codes:**
    - 200: User found
    - 404: User not found
    - 500: Server error
    """
    try:
        _result = ServiceUser.get_by_id(db, id)
        if not _result:
            raise HTTPException(status_code=404, detail=f"Object {id} not found")
        return ResponseError(
            code=200, status="Ok", message="Finded one", validationErrors=_result
        ).dict(exclude_none=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@user.put("/", status_code=202, summary="Update user")
async def update(
    request: DTOUserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(ServiceUser.get_current_user),
):
    """
    Update an existing user's information.

    **Requires authentication:** Bearer token from /user/login endpoint

    **Parameters:**
    - **id** (UUID): User's unique identifier
    - **email** (string, optional): New email address
    - **full_name** (string, optional): New full name
    - Other optional fields to update

    **Returns:**
    - Updated user object

    **Status Codes:**
    - 202: User updated successfully
    - 404: User not found
    - 401: Authentication required
    - 500: Server error
    """
    try:
        _result = ServiceUser.update(db, updated=request)
        if not _result:
            raise HTTPException(status_code=404, detail=f"Object {id} not found")
        return ResponseError(
            code=202, status="Accepted", message="Updated", validationErrors=_result
        ).dict(exclude_none=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@user.delete("/{id}", status_code=204, summary="Delete user")
async def delete(
    id: UUID, db: Session = Depends(get_db), current_user=Depends(ServiceUser.get_current_user)
):
    """
    Delete a user from the system.

    **Requires authentication:** Bearer token from /user/login endpoint

    **Path Parameters:**
    - **id** (UUID): User's unique identifier

    **Returns:**
    - No content (HTTP 204 status)

    **Status Codes:**
    - 204: User deleted successfully
    - 404: User not found
    - 401: Authentication required
    - 500: Server error
    """
    try:
        _result = ServiceUser.remove(db, id=id)
        if not _result:
            raise HTTPException(status_code=404, detail=f"Object {id} not found")
        return ResponseError(
            code=204, status="No Content", message="Delete one", validationErrors=_result
        ).dict(exclude_none=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
