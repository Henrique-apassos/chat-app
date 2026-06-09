# ══════════════════════════════════════════════════════════════════════════════
# Feature: Perfil de Usuário
# ══════════════════════════════════════════════════════════════════════════════

class TestPerfilDeUsuario:

    USUARIO_VALIDO = {
        "usuario": "bruna",
        "email": "bruna@email.com",
        "telefone": "81999999999",
        "senha": "123456",
    }

    def test_atualizar_perfil_com_sucesso(self, client):
        """
        Scenario: Atualização de perfil com sucesso
        ─────────────────────────────────────────────────
        Given existe uma pessoa cadastrada
        When atualizo os dados de perfil
        Then o sistema retorna sucesso
        """

        # Cria um usuário no banco de teste
        client.post("/auth/register", json=self.USUARIO_VALIDO)

        # Atualiza o perfil
        response = client.put(
            "/user/profile",
            json={
                "usuario": "bruna",
                "nome": "Bruna",
                "sobrenome": "Chalegre",
                "biografia": "Desenvolvedora mobile",
            },
        )

        assert response.status_code == 200

        assert response.json()["message"] == "Perfil atualizado com sucesso"

    def test_buscar_perfil_com_sucesso(self, client):
        """
        Scenario: Consulta de perfil com sucesso
        ─────────────────────────────────────────────────
        Given existe uma pessoa cadastrada com perfil atualizado
        When busco o perfil pelo nome de usuário
        Then o sistema retorna Status 200 e os dados do perfil
        """

        client.post("/auth/register", json=self.USUARIO_VALIDO)

        client.put(
            "/user/profile",
            json={
                "usuario": "bruna",
                "nome": "Bruna",
                "sobrenome": "Chalegre",
                "biografia": "Desenvolvedora mobile",
                "caminho_foto": None,
            },
        )

        response = client.get("/user/profile/bruna")

        assert response.status_code == 200

        body = response.json()
        assert body["usuario"] == "bruna"
        assert body["email"] == "bruna@email.com"
        assert body["telefone"] == "81999999999"
        assert body["nome"] == "Bruna"
        assert body["sobrenome"] == "Chalegre"
        assert body["biografia"] == "Desenvolvedora mobile"
        assert body["caminho_foto"] is None

    def test_atualizacao_parcial_nao_deve_apagar_campos_existentes(self, client):
        """
        Scenario: Atualização parcial de perfil
        ─────────────────────────────────────────────────
        Given existe uma pessoa cadastrada com perfil completo
        When atualizo apenas a biografia
        Then o sistema mantém os outros campos e altera somente a biografia
        """

        client.post("/auth/register", json=self.USUARIO_VALIDO)

        client.put(
            "/user/profile",
            json={
                "usuario": "bruna",
                "nome": "Bruna",
                "sobrenome": "Chalegre",
                "biografia": "Bio antiga",
                "caminho_foto": "/images/bruna.jpg",
            },
        )

        response = client.put(
            "/user/profile",
            json={
                "usuario": "bruna",
                "biografia": "Bio atualizada",
            },
        )

        assert response.status_code == 200

        perfil = client.get("/user/profile/bruna")

        assert perfil.status_code == 200

        body = perfil.json()
        assert body["nome"] == "Bruna"
        assert body["sobrenome"] == "Chalegre"
        assert body["biografia"] == "Bio atualizada"
        assert body["caminho_foto"] == "/images/bruna.jpg"

    def test_atualizar_perfil_de_usuario_inexistente_deve_retornar_404(self, client):
        """
        Scenario: Atualização de perfil de usuário inexistente
        ─────────────────────────────────────────────────
        Given não existe pessoa cadastrada com usuário "fantasma"
        When tento atualizar o perfil desse usuário
        Then o sistema retorna Status 404 e mensagem "Usuário não encontrado"
        """

        response = client.put(
            "/user/profile",
            json={
                "usuario": "fantasma",
                "nome": "Usuário Fantasma",
            },
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Usuário não encontrado"

    def test_buscar_perfil_de_usuario_inexistente_deve_retornar_404(self, client):
        """
        Scenario: Consulta de perfil de usuário inexistente
        ─────────────────────────────────────────────────
        Given não existe pessoa cadastrada com usuário "fantasma"
        When tento buscar o perfil desse usuário
        Then o sistema retorna Status 404 e mensagem "Usuário não encontrado"
        """

        response = client.get("/user/profile/fantasma")

        assert response.status_code == 404
        assert response.json()["detail"] == "Usuário não encontrado"

    def test_excluir_conta_com_sucesso(self, client):
        """
        Scenario: Exclusão de conta com sucesso
        ─────────────────────────────────────────────────
        Given existe uma pessoa cadastrada com usuário "bruna"
        When informo a senha correta para confirmar a exclusão
        Then o sistema remove a conta e retorna Status 200
        """

        # Cria um usuário no banco de teste
        client.post("/auth/register", json=self.USUARIO_VALIDO)

        # Solicita a exclusão informando a senha correta
        response = client.request(
            "DELETE",
            "/user/profile/bruna",
            json={
                "senha": "123456",
            },
        )

        assert response.status_code == 200

        assert response.json()["message"] == "Conta excluída com sucesso"

        # Verifica se o usuário realmente foi removido
        perfil = client.get("/user/profile/bruna")

        assert perfil.status_code == 404

        assert perfil.json()["detail"] == "Usuário não encontrado"

    def test_excluir_conta_com_senha_incorreta_deve_retornar_401(self, client):
        """
        Scenario: Exclusão de conta com senha incorreta
        ─────────────────────────────────────────────────
        Given existe uma pessoa cadastrada com usuário "bruna"
        When informo uma senha incorreta para confirmar a exclusão
        Then o sistema retorna Status 401
            e mantém a conta cadastrada
        """

        client.post("/auth/register", json=self.USUARIO_VALIDO)

        response = client.request(
            "DELETE",
            "/user/profile/bruna",
            json={
                "senha": "senhaerrada",
            },
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Senha incorreta"

        perfil = client.get("/user/profile/bruna")

        assert perfil.status_code == 200
        assert perfil.json()["usuario"] == "bruna"

    def test_excluir_conta_inexistente_deve_retornar_404(self, client):
        """
        Scenario: Exclusão de conta inexistente
        ─────────────────────────────────────────────────
        Given não existe uma pessoa com usuário "fantasma"
        When tento excluir essa conta
        Then o sistema retorna Status 404
            e informa que o usuário não foi encontrado
        """

        response = client.request(
            "DELETE",
            "/user/profile/fantasma",
            json={
                "senha": "123456",
            },
        )

        assert response.status_code == 404

        assert response.json()["detail"] == "Usuário não encontrado"

    def test_biografia_maior_que_300_caracteres_deve_retornar_422(self, client):
        """
        Scenario: Biografia maior que 300 caracteres
        ─────────────────────────────────────────────────
        Given existe uma pessoa cadastrada
        When tento atualizar a biografia com mais de 300 caracteres
        Then o sistema retorna Status 422
        """

        client.post("/auth/register", json=self.USUARIO_VALIDO)

        bio_grande = "a" * 301

        response = client.put(
            "/user/profile",
            json={
                "usuario": "bruna",
                "biografia": bio_grande,
            },
        )

        assert response.status_code == 422

    def test_atualizar_email_para_email_ja_cadastrado_deve_retornar_409(
    self,
    client,
    ):
        """
        Scenario: Atualização para e-mail já cadastrado
        ─────────────────────────────────────────────────
        Given existem duas pessoas cadastradas
        When tento alterar o e-mail de uma delas para o e-mail da outra
        Then o sistema retorna Status 409
            informando que o e-mail já está cadastrado
        """

        client.post(
            "/auth/register",
            json=self.USUARIO_VALIDO,
        )

        client.post(
            "/auth/register",
            json={
                "usuario": "joao",
                "email": "joao@email.com",
                "telefone": "81888888888",
                "senha": "123456",
            },
        )

        response = client.put(
            "/user/profile",
            json={
                "usuario": "bruna",
                "email": "joao@email.com",
            },
        )

        assert response.status_code == 409

        assert response.json()["detail"] == "E-mail já cadastrado"

    def test_atualizar_telefone_para_telefone_ja_cadastrado_deve_retornar_409(
    self,
    client,
    ):
        """
        Scenario: Atualização para telefone já cadastrado
        ─────────────────────────────────────────────────
        Given existem duas pessoas cadastradas
        When tento alterar o telefone de uma delas para o telefone da outra
        Then o sistema retorna Status 409
            informando que o telefone já está cadastrado
        """

        client.post(
            "/auth/register",
            json=self.USUARIO_VALIDO,
        )

        client.post(
            "/auth/register",
            json={
                "usuario": "joao",
                "email": "joao@email.com",
                "telefone": "81888888888",
                "senha": "123456",
            },
        )

        response = client.put(
            "/user/profile",
            json={
                "usuario": "bruna",
                "telefone": "81888888888",
            },
        )

        assert response.status_code == 409

        assert response.json()["detail"] == "Telefone já cadastrado"

    def test_trocar_nome_de_usuario_com_sucesso(self, client):
        """
        Scenario: Troca de nome de usuário com sucesso
        ─────────────────────────────────────────────────
        Given existe uma pessoa cadastrada com usuário "bruna"
        When atualizo o nome de usuário para "brunaveiga"
        Then o sistema retorna Status 200
            e o perfil passa a ser encontrado pelo novo usuário
        """

        client.post("/auth/register", json=self.USUARIO_VALIDO)

        response = client.put(
            "/user/profile",
            json={
                "usuario": "bruna",
                "novo_usuario": "brunaveiga",
            },
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Perfil atualizado com sucesso"

        perfil_novo = client.get("/user/profile/brunaveiga")

        assert perfil_novo.status_code == 200
        assert perfil_novo.json()["usuario"] == "brunaveiga"

        perfil_antigo = client.get("/user/profile/bruna")

        assert perfil_antigo.status_code == 404
        assert perfil_antigo.json()["detail"] == "Usuário não encontrado"

    def test_trocar_nome_de_usuario_para_usuario_ja_cadastrado_deve_retornar_409(
    self,
    client,
    ):
        """
        Scenario: Troca para nome de usuário já cadastrado
        ─────────────────────────────────────────────────
        Given existem duas pessoas cadastradas
        When tento alterar o usuário de uma delas para o usuário da outra
        Then o sistema retorna Status 409
            informando que o nome de usuário já está cadastrado
        """

        client.post("/auth/register", json=self.USUARIO_VALIDO)

        client.post(
            "/auth/register",
            json={
                "usuario": "joao",
                "email": "joao@email.com",
                "telefone": "81888888888",
                "senha": "123456",
            },
        )

        response = client.put(
            "/user/profile",
            json={
                "usuario": "bruna",
                "novo_usuario": "joao",
            },
        )

        assert response.status_code == 409
        assert response.json()["detail"] == "Nome de usuário já cadastrado"