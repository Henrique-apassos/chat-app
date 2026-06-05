from sqlalchemy.orm import Session
from app.models.user import UserModel


class UserRepository:
    """
    Única camada que fala diretamente com o banco de dados.
    Nenhuma outra camada acessa o banco fora daqui.
    """

    def __init__(self, db: Session):
        self.db = db

    def find_by_email(self, email: str) -> UserModel | None:
        """Busca uma pessoa pelo e-mail. Retorna None se não existir."""
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def find_by_usuario(self, usuario: str) -> UserModel | None:
        return self.db.query(UserModel).filter(
            UserModel.usuario == usuario
        ).first()

    def create(
        self,
        usuario: str,
        email: str,
        telefone: str,
        senha: str,
    ) -> UserModel:
        """Cria e persiste uma nova pessoa no banco.
        'nome' é preenchido automaticamente com o valor de 'usuario'.
        """
        pessoa = UserModel(
            usuario=usuario,
            email=email,
            telefone=telefone,
            senha=senha,
            nome=usuario,
        )
        self.db.add(pessoa)
        self.db.commit()
        self.db.refresh(pessoa)
        return pessoa