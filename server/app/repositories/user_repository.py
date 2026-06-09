from sqlalchemy.orm import Session
from app.models.user import UserModel


class UserRepository:
    """
    Repositório de usuários — única camada responsável pelo acesso ao banco.
    Segue o princípio da Responsabilidade Única (SRP) e o padrão Repository,
    isolando a lógica de persistência do restante da aplicação.
    """

    def __init__(self, db: Session):
        self._db = db

    def find_by_email(self, email: str) -> UserModel | None:
        """Busca uma pessoa pelo e-mail. Retorna None se não existir."""
        return (
            self._db.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )

    def find_by_usuario(self, usuario: str) -> UserModel | None:
        """Busca uma pessoa pelo nome de usuário (PK). Retorna None se não existir."""
        return (
            self._db.query(UserModel)
            .filter(UserModel.usuario == usuario)
            .first()
        )

    def find_by_telefone(self, telefone: str) -> UserModel | None:
        """Busca uma pessoa pelo telefone. Retorna None se não existir."""
        return (
            self._db.query(UserModel)
            .filter(UserModel.telefone == telefone)
            .first()
        )

    def create(
        self,
        usuario: str,
        email: str,
        telefone: str,
        senha: str,
    ) -> UserModel:
        """
        Cria e persiste uma nova pessoa no banco.
        Recebe a senha JÁ hasheada — responsabilidade do Service.
        'nome' é preenchido automaticamente com o valor de 'usuario'.
        """
        pessoa = UserModel(
            usuario=usuario,
            email=email,
            telefone=telefone,
            senha=senha,
            nome=usuario,
        )
        self._db.add(pessoa)
        self._db.commit()
        self._db.refresh(pessoa)
        return pessoa