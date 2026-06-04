"""
Testes Unitários — Validações do Schema UserRegisterRequest
Testam a lógica de validação isoladamente, sem banco de dados ou servidor.
"""
import pytest
from pydantic import ValidationError
from app.schemas.user import UserRegisterRequest


def test_senha_muito_curta_deve_falhar():
    """Senha com menos de 6 caracteres deve lançar ValidationError."""
    with pytest.raises(ValidationError):
        UserRegisterRequest(
            nome_usuario="joao",
            email="joao@email.com",
            telefone="(88) 98888-8888",
            senha="abc"
        )


def test_senha_valida_deve_passar():
    """Senha com 6 ou mais caracteres deve ser aceita."""
    user = UserRegisterRequest(
        nome_usuario="joao",
        email="joao@email.com",
        telefone="(88) 98888-8888",
        senha="Segura@123"
    )
    assert user.senha == "Segura@123"


def test_email_invalido_deve_falhar():
    """E-mail sem formato válido deve lançar ValidationError."""
    with pytest.raises(ValidationError):
        UserRegisterRequest(
            nome_usuario="joao",
            email="emailinvalido",
            telefone="(88) 98888-8888",
            senha="Segura@123"
        )


def test_email_valido_deve_passar():
    """E-mail com formato correto deve ser aceito."""
    user = UserRegisterRequest(
        nome_usuario="joao",
        email="joao@email.com",
        telefone="(88) 98888-8888",
        senha="Segura@123"
    )
    assert user.email == "joao@email.com"


def test_campos_obrigatorios_ausentes_devem_falhar():
    """Ausência de campo obrigatório deve lançar ValidationError."""
    with pytest.raises(ValidationError):
        UserRegisterRequest(
            email="joao@email.com",
            senha="Segura@123"
            # nome_usuario e telefone ausentes
        )