import pytest


# ══════════════════════════════════════════════════════════════════════════════
# Feature: Cadastro de Usuários
# ══════════════════════════════════════════════════════════════════════════════

class TestCadastroDeUsuarios:

    PESSOA_VALIDA = {
        "email": "joao@email.com",
        "nome_de_usuario": "joaosilva",
        "telefone": "(88) 988888888",
        "senha": "Segura@123",
    }

    def test_cadastro_novo_usuario_com_sucesso(self, client):
        """
        Scenario: Cadastro de novo usuário com sucesso
        ─────────────────────────────────────────────────
        Given  estou na rota de cadastro e o sistema NÃO possui o e-mail "joao@email.com"
        When   insiro email, telefone, nome_de_usuario e senha com mínimo 6 caracteres
        Then   o sistema criptografa a senha, salva no banco,
               retorna Status 201 e mensagem "Cadastro realizado com sucesso"
        """
        response = client.post("/auth/register", json=self.PESSOA_VALIDA)

        assert response.status_code == 201
        assert response.json()["message"] == "Cadastro realizado com sucesso"

    def test_cadastro_email_duplicado_deve_ser_barrado(self, client):
        """
        Scenario: Cadastro com e-mail já existente
        ─────────────────────────────────────────────────
        Given  o sistema JÁ possui uma pessoa com e-mail "joao@email.com"
        When   tento registrar outra conta com esse mesmo e-mail
        Then   o sistema barra a criação, retorna Status 409
               e exibe "E-mail já cadastrado"
        """
        client.post("/auth/register", json=self.PESSOA_VALIDA)

        response = client.post("/auth/register", json=self.PESSOA_VALIDA)

        assert response.status_code == 409
        assert response.json()["detail"] == "E-mail já cadastrado"

    def test_cadastro_senha_curta_deve_retornar_erro_de_validacao(self, client):
        """
        Validação Extra: senha com menos de 6 caracteres é rejeitada (422).
        """
        pessoa_senha_curta = {**self.PESSOA_VALIDA, "senha": "abc"}
        response = client.post("/auth/register", json=pessoa_senha_curta)

        assert response.status_code == 422


# ══════════════════════════════════════════════════════════════════════════════
# Feature: Autenticação de Usuários (Login)
# ══════════════════════════════════════════════════════════════════════════════

class TestAutenticacaoDeUsuarios:

    PESSOA_REGISTRADA = {
        "email": "joao@email.com",
        "nome_de_usuario": "joaosilva",
        "telefone": "(88) 988888888",
        "senha": "Segura@123",
    }

    @pytest.fixture(autouse=True)
    def pre_cadastrar_pessoa(self, client):
        """
        Pré-condição que roda antes de cada teste:
        garante que a pessoa já existe no banco de teste.
        """
        client.post("/auth/register", json=self.PESSOA_REGISTRADA)

    def test_login_com_credenciais_validas(self, client):
        """
        Scenario: Login com credenciais válidas
        ─────────────────────────────────────────────────
        Given  a pessoa "joao@email.com" / "Segura@123" está registrada
        When   informo e-mail e senha corretos na rota de login
        Then   o sistema autentica, gera token JWT com expiração
               e retorna Status 200 com a lista de contatos
        """
        response = client.post("/auth/login", json={
            "email": "joao@email.com",
            "senha": "Segura@123",
        })

        assert response.status_code == 200

        body = response.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"
        assert "expires_in" in body
        assert body["expires_in"] > 0
        assert isinstance(body["contacts"], list)

    def test_login_com_senha_incorreta_deve_negar_acesso(self, client):
        """
        Scenario: Login com senha incorreta
        ─────────────────────────────────────────────────
        Given  a pessoa "joao@email.com" está cadastrada
        When   informo senha errada "Errada456"
        Then   o sistema impede o acesso, retorna Status 401
               e exibe mensagem genérica "Credenciais inválidas"
        """
        response = client.post("/auth/login", json={
            "email": "joao@email.com",
            "senha": "Errada456",
        })

        assert response.status_code == 401
        assert response.json()["detail"] == "Credenciais inválidas"

    def test_login_com_email_inexistente_deve_negar_acesso(self, client):
        """
        Validação Extra: e-mail não cadastrado retorna 401 com a MESMA mensagem genérica.
        """
        response = client.post("/auth/login", json={
            "email": "fantasma@email.com",
            "senha": "qualquer123",
        })

        assert response.status_code == 401
        assert response.json()["detail"] == "Credenciais inválidas"