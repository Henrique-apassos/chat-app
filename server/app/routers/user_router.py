from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserProfileUpdateRequest
from app.services.user_service import UserService


router = APIRouter(
    prefix="/user",
    tags=["Perfil"],
)


@router.put(
    "/profile",
    status_code=status.HTTP_200_OK,
    summary="Atualizar perfil do usuário",
    response_description="Perfil atualizado com sucesso",
)
def update_profile(
    data: UserProfileUpdateRequest,
    db: Session = Depends(get_db),
) -> dict:
    """
    Atualiza os dados de perfil de um usuário.

    Campos editáveis:

    - **nome**
    - **novo_usuario**
    - **sobrenome**
    - **email**
    - **telefone**
    - **biografia**
    - **caminho_foto**

    O usuário é identificado pelo campo **usuario** enviado na requisição.
    """

    service = UserService(db)

    return service.update_profile(data)


@router.get(
    "/profile/{usuario}",
    status_code=status.HTTP_200_OK,
    summary="Buscar perfil do usuário",
    response_description="Perfil encontrado com sucesso",
)
def get_profile(
    usuario: str,
    db: Session = Depends(get_db),
) -> dict:
    """
    Busca os dados completos de perfil de um usuário.

    O usuário é identificado pelo campo **usuario** enviado na URL.
    """

    service = UserService(db)

    return service.get_profile(usuario)