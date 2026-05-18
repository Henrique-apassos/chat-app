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

    def create(
        self,
        email: str,
        nome_de_usuario: str,
        telefone: str,
        senha: str,  # recebe a senha JÁ hasheada — o hash é feito no Service
    ) -> UserModel:
        """Cria e persiste uma nova pessoa no banco."""
        pessoa = UserModel(
            email=email,
            nome_de_usuario=nome_de_usuario,
            telefone=telefone,
            senha=senha,
        )
        self.db.add(pessoa)
        self.db.commit()
        self.db.refresh(pessoa)
        return pessoa