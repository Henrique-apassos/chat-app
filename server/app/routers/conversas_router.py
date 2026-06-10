from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.security import get_usuario_atual
from app.database import get_db
from app.services.conversas_service import ConversasService

router = APIRouter(
    prefix="/conversas",
    tags=["Conversas"],
)


@router.get(
    "/buscar",
    summary="Buscar conversas do usuário autenticado",
    response_description="Lista de conversas (existentes primeiro) e usuários encontrados",
)
def buscar_conversas(
    q: str = Query(
        default="",
        max_length=100,
        description="Termo de busca por prefixo (nome de usuário ou nome de grupo). "
        "Case-insensitive. Vazio retorna todas as conversas existentes.",
    ),
    usuario_atual: str = Depends(get_usuario_atual),
    db: Session = Depends(get_db),
) -> list[dict]:
    """
    Busca as conversas do usuário autenticado.

    O usuário é identificado pelo **JWT** (header `Authorization: Bearer <token>`),
    nunca por parâmetro — garantindo que ninguém acesse as conversas de outro.

    Regras:
    - Busca por **prefixo**, case-insensitive (ex.: `Pa` → `paulo`, `paula`).
    - `q` vazio → todas as conversas existentes, mais recentes primeiro.
    - Conversas já existentes (`status: true`) vêm antes dos usuários ainda sem
      conversa (`status: false`).
    - Grupos retornados são apenas aqueles dos quais o usuário participa.

    Cada item:
    ```
    {
      "tipo": "usuario" | "grupo",
      "id": "<usuario>" | <id_grupo>,
      "nome": "<nome>",
      "status": true | false,
      "last_message": {"remetente": "<usuario>", "texto": "<texto>"} | null
    }
    ```
    """
    service = ConversasService(db)
    return service.buscar(usuario_atual, q)
