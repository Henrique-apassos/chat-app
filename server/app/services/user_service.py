from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserProfileUpdateRequest


class UserService:
    """
    Serviço responsável pela edição de perfil.

    Contém as regras de negócio relacionadas aos dados
    pessoais do usuário, mantendo a separação de responsabilidades
    (SRP - Single Responsibility Principle).
    """

    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def update_profile(self, data: UserProfileUpdateRequest) -> dict:
        """
        Fluxo de atualização de perfil:

        1. Busca o usuário pelo nome de usuário.
        2. Verifica se o usuário existe.
        3. Caso um novo e-mail seja enviado, verifica se ele já pertence a outro usuário.
        4. Caso um novo telefone seja enviado, verifica se ele já pertence a outro usuário.
        5. Atualiza apenas os campos enviados na requisição.
        6. Persiste as alterações no banco.
        7. Retorna mensagem de sucesso.

        Retorna:
            dict: mensagem de confirmação.
        """

        pessoa_atual = self.repo.find_by_usuario(data.usuario)

        if not pessoa_atual:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )
        
        if data.novo_usuario is not None:
            pessoa_com_usuario = self.repo.find_by_usuario(data.novo_usuario)

            if pessoa_com_usuario and pessoa_com_usuario.usuario != data.usuario:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Nome de usuário já cadastrado",
                )

        if data.email is not None:
            pessoa_com_email = self.repo.find_by_email(data.email)

            if pessoa_com_email and pessoa_com_email.usuario != data.usuario:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="E-mail já cadastrado",
                )

        if data.telefone is not None:
            pessoa_com_telefone = self.repo.find_by_telefone(data.telefone)

            if pessoa_com_telefone and pessoa_com_telefone.usuario != data.usuario:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Telefone já cadastrado",
                )

        self.repo.update_profile(
            usuario=data.usuario,
            novo_usuario=data.novo_usuario,
            nome=data.nome,
            sobrenome=data.sobrenome,
            email=data.email,
            telefone=data.telefone,
            biografia=data.biografia,
            caminho_foto=data.caminho_foto,
        )

        return {
            "message": "Perfil atualizado com sucesso"
        }
    
    def get_profile(self, usuario: str) -> dict:
        """
        Fluxo de busca de perfil:

        1. Busca o usuário pelo nome de usuário.
        2. Verifica se o usuário existe.
        3. Retorna os dados públicos do perfil.

        Retorna:
            dict: dados do perfil do usuário.
        """

        pessoa = self.repo.find_by_usuario(usuario)

        if not pessoa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )

        return {
            "usuario": pessoa.usuario,
            "email": pessoa.email,
            "telefone": pessoa.telefone,
            "nome": pessoa.nome,
            "sobrenome": pessoa.sobrenome,
            "biografia": pessoa.biografia,
            "caminho_foto": pessoa.caminho_foto,
        }