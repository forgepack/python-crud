from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.base import ResponseError
from app.schemas.user import DTOUserCreate
from app.services.user import ServiceUser

admin = APIRouter(prefix="/admin", tags=["admin"])


@admin.post("/init/create-first-user", status_code=status.HTTP_201_CREATED, response_model=ResponseError, summary="Initialize database with first admin user")
async def create_first_user(
    request: DTOUserCreate,
    db: Session = Depends(get_db),
):
    """
    Create the first admin user (no authentication required).
    
    **⚠️ Important:** This endpoint only works if no users exist in the database.
    
    Use this endpoint to initialize the application on first run.
    After the first user is created, you must authenticate to create additional users.
    
    **Parameters:**
    - **username** (string): Admin username (e.g., "admin")
    - **email** (string): Admin email address
    - **password** (string): Secure password
    - **full_name** (string): Administrator's full name
    
    **Returns:**
    - Created user object with id and metadata
    
    **Status Codes:**
    - 201: First user created successfully
    - 403: Database already initialized (users exist)
    - 400: Invalid input data
    - 500: Server error
    
    **Example Request:**
    ```json
    {
      "username": "admin",
      "email": "admin@example.com",
      "password": "SecurePassword123!",
      "full_name": "Administrator"
    }
    ```
    
    **Next Steps:**
    1. After successful creation, use POST /user/login with these credentials
    2. Use the returned token in Authorization header for other endpoints
    """
    try:
        service = ServiceUser(db)
        
        # Check if any users exist
        existing_users = db.query(ServiceUser.model).count() if hasattr(service, 'model') else 0
        if existing_users > 0:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Database already initialized. Cannot create first user."
            )
        
        result = service.create(request)
        return ResponseError(
            code=201,
            status="Created",
            message="First user created successfully",
            validationErrors=result
        ).dict(exclude_none=True)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@admin.get(
    "/{user_id}/security-status", status_code=status.HTTP_200_OK, response_model=ResponseError
)
async def get_user_security_status(
    user_id: UUID, db: Session = Depends(get_db), current_user=Depends(ServiceUser.get_by_username)
):
    """
    Obter status de segurança de um usuário.
    APENAS para administradores - contém informações sensíveis.
    """
    service = ServiceUser(db)
    result = service.get_security_status(user_id)
    return ResponseError(
        code=200, status="Ok", message="Status de segurança obtido", validation_errors=result
    ).dict(exclude_none=True)


@admin.post("/{user_id}/unlock", status_code=status.HTTP_200_OK, response_model=ResponseError)
async def unlock_user_account(
    user_id: UUID, db: Session = Depends(get_db), current_user=Depends(ServiceUser.get_by_username)
):
    """
    Desbloquear conta de usuário manualmente.
    APENAS para administradores.
    """
    service = ServiceUser(db)
    current_user_id = getattr(current_user, "id", None) if current_user else None

    result = service.unlock_account(user_id, current_user_id)
    return ResponseError(
        code=200,
        status="Ok",
        message="Conta desbloqueada com sucesso",
        validation_errors={"unlocked": result},
    ).dict(exclude_none=True)
