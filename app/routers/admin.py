from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.base import ResponseError
from app.services.user import ServiceUser

admin = APIRouter(prefix="/admin", tags=["admin"])


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
