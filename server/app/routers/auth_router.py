from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import TokenResponse, UserLoginRequest, UserRegisterRequest
from app.services.auth_service import AuthService
from app.core.security import get_usuario_atual
from app.models.user import UserModel

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"],
)

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastro de novo usuário",
    response_description="Usuário cadastrado com sucesso",
)
def cadastrar(
    data: UserRegisterRequest,
    db: Session = Depends(get_db),
) -> dict:
    """
    Cadastra um novo usuário no sistema.

    - **usuario**: nome de usuário único
    - **email**: e-mail único e válido
    - **telefone**: telefone no formato (XX) XXXXX-XXXX
    - **senha**: mínimo 6 caracteres
    """
    service = AuthService(db)
    return service.cadastrar(data)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
    summary="Login de usuário",
    response_description="Token JWT gerado com sucesso",
)
def login(
    data: UserLoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Autentica um usuário e retorna um token JWT.

    - **email**: e-mail cadastrado
    - **senha**: senha do usuário
    """
    service = AuthService(db)
    return service.login(data)


@router.delete(
    "/test/cleanup",
    status_code=status.HTTP_200_OK,
    summary="Limpa banco de dados de teste",
    include_in_schema=False,
)
def cleanup(db: Session = Depends(get_db)) -> dict:
    """Endpoint exclusivo para testes — remove todos os usuários do banco."""
    from app.models.user import UserModel
    from app.models.mensagem import MensagemModel
    from app.models.recebe import RecebeModel
    import os
    if os.getenv("ENVIRONMENT") != "production":
        db.query(RecebeModel).delete()
        db.query(MensagemModel).delete()
        db.query(UserModel).delete()
        db.commit()
        return {"message": "Banco limpo com sucesso"}
    
@router.get("/usuarios")
def listar_todos_os_usuarios(db: Session = Depends(get_db)):
    """
    Busca todos os usuários cadastrados no banco para preencher a barra lateral do chat.
    """
    usuarios_db = db.query(UserModel).all()
    
    lista_contatos = []
    for user in usuarios_db:
        lista_contatos.append({
            "usuario": user.usuario,
            "nome": user.nome
        })
        
    return lista_contatos

@router.get("/me", status_code=status.HTTP_200_OK, summary="Obter dados do usuário logado")
def get_me(
    usuario_no_token: str = Depends(get_usuario_atual), 
    db: Session = Depends(get_db)
):
    """
    Retorna os dados completos do usuário que é dono do token atual.
    Esta rota resolve a identidade real do frontend.
    """
    usuario_db = db.query(UserModel).filter(UserModel.usuario == usuario_no_token).first()
    
    if not usuario_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuário não encontrado no banco de dados."
        )
        
    return {
        "usuario": usuario_db.usuario,
        "nome": usuario_db.nome,
        "email": usuario_db.email
    }