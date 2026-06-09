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