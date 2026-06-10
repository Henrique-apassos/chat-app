"""
Verificação de token JWT para rotas protegidas.

O login (auth_service) já *gera* o token com `jwt.encode`, colocando o nome de
usuário no campo `sub`. Este módulo faz o caminho inverso: *valida* o token que
chega no header `Authorization: Bearer <token>` e devolve o usuário autenticado.

Reutiliza as MESMAS configurações do auth_service (SECRET_KEY e algoritmo), lidas
do ambiente — caso contrário a assinatura não bateria e nenhum token validaria.
"""
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "chave-padrao-insegura-mude-no-env")
ALGORITHM = "HS256"

# auto_error=False: nós mesmos lançamos o 401 quando o header faltar,
# garantindo uma resposta de erro consistente.
_esquema_bearer = HTTPBearer(auto_error=False)


def get_usuario_atual(
    credenciais: HTTPAuthorizationCredentials | None = Depends(_esquema_bearer),
) -> str:
    """
    Dependência do FastAPI que identifica o usuário a partir do JWT.

    - Lê o token do header `Authorization: Bearer <token>`.
    - Valida assinatura e expiração.
    - Retorna o `sub` (nome de usuário) embutido no token.

    Qualquer falha (header ausente, token inválido, expirado ou sem `sub`)
    resulta em 401 — impedindo que um usuário acesse conversas de outro (IDOR).
    """
    erro_401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token de autenticação ausente ou inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credenciais is None or not credenciais.credentials:
        raise erro_401

    try:
        payload = jwt.decode(
            credenciais.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except JWTError:
        raise erro_401

    usuario = payload.get("sub")
    if not usuario:
        raise erro_401

    return usuario
