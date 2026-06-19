# ══════════════════════════════════════════════════════════════════════════════
# Feature: Lista de Conversas e Busca
# ══════════════════════════════════════════════════════════════════════════════
"""
Testes do serviço/rota de busca de conversas (GET /conversas/buscar).

O usuário é sempre identificado pelo JWT (header Authorization: Bearer),
nunca por parâmetro — por isso cada teste registra e faz login para obter
um token real.

As mensagens são semeadas direto no banco de teste (mensagem + recebe),
reproduzindo o que o motor de WebSocket grava, sem depender dele.
"""
from app import database
from app.models.esta_em import EstaModel
from app.models.grupo import GrupoModel
from app.models.mensagem import MensagemModel
from app.models.recebe import RecebeModel


# ── Helpers ───────────────────────────────────────────────────────────────────

def _registrar(client, usuario, email, telefone):
    return client.post(
        "/auth/register",
        json={"usuario": usuario, "email": email, "telefone": telefone, "senha": "123456"},
    )


def _logar(client, email):
    resposta = client.post("/auth/login", json={"email": email, "senha": "123456"})
    token = resposta.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _enviar_mensagem(remetente, destinatario, texto):
    """Grava uma mensagem 1:1 (tabelas 'mensagem' + 'recebe') no banco de teste."""
    db = database.SessionLocal()
    try:
        msg = MensagemModel(
            timestamp="2026-01-01 00:00:00",
            texto=texto,
            status_envio="ENVIADO",
            usuario=remetente,
            id_grupo=None,
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)
        db.add(RecebeModel(usuario=destinatario, id_mensagem=msg.id_mensagem, lida=0))
        db.commit()
        return msg.id_mensagem
    finally:
        db.close()


def _criar_grupo(nome, membro):
    """Cria um grupo e adiciona um membro (tabelas 'grupo' + 'esta_em')."""
    db = database.SessionLocal()
    try:
        grupo = GrupoModel(nome_grupo=nome, data_criacao="2026-01-01", descricao=None)
        db.add(grupo)
        db.commit()
        db.refresh(grupo)
        db.add(EstaModel(usuario=membro, id_grupo=grupo.id_grupo, papel="membro", data_entrada="2026-01-01"))
        db.commit()
        return grupo.id_grupo
    finally:
        db.close()


# ── Testes ────────────────────────────────────────────────────────────────────

class TestBuscaDeConversas:

    def test_busca_sem_token_retorna_401(self, client):
        """
        Scenario: Acesso sem autenticação é negado
        ─────────────────────────────────────────────────
        Given um cliente sem token JWT
        When ele chama GET /conversas/buscar
        Then o sistema retorna 401 (protege contra IDOR)
        """
        resposta = client.get("/conversas/buscar")

        assert resposta.status_code == 401

    def test_q_vazio_retorna_conversas_existentes_ordenadas(self, client):
        """
        Scenario: q vazio lista as conversas existentes, mais recentes primeiro
        ─────────────────────────────────────────────────
        Given "paulo" conversou com "joao" e depois com "paula"
        When ele busca com q vazio
        Then retorna as duas conversas, com "paula" (mais recente) primeiro
        And cada item tem status True e a última mensagem
        """
        _registrar(client, "paulo", "paulo@email.com", "81900000001")
        _registrar(client, "joao", "joao@email.com", "81900000002")
        _registrar(client, "paula", "paula@email.com", "81900000003")

        _enviar_mensagem("paulo", "joao", "fala joao")       # mais antiga
        _enviar_mensagem("paula", "paulo", "oi paulo")       # mais recente

        cabecalho = _logar(client, "paulo@email.com")
        resposta = client.get("/conversas/buscar", headers=cabecalho)

        assert resposta.status_code == 200
        dados = resposta.json()

        assert [d["id"] for d in dados] == ["paula", "joao"]   # ordenado por recência
        assert all(d["status"] is True for d in dados)
        assert dados[0]["tipo"] == "usuario"
        assert dados[0]["last_message"] == {"remetente": "paula", "texto": "oi paulo"}

    def test_busca_por_prefixo_case_insensitive(self, client):
        """
        Scenario: Busca por prefixo, ignorando maiúsculas/minúsculas
        ─────────────────────────────────────────────────
        Given existem os usuários "paula" e "joao"
        When "paulo" busca por "PA"
        Then apenas nomes que começam com "pa" são retornados (paula), não "joao"
        """
        _registrar(client, "paulo", "paulo@email.com", "81900000001")
        _registrar(client, "paula", "paula@email.com", "81900000003")
        _registrar(client, "joao", "joao@email.com", "81900000002")

        cabecalho = _logar(client, "paulo@email.com")
        resposta = client.get("/conversas/buscar?q=PA", headers=cabecalho)

        assert resposta.status_code == 200
        ids = [d["id"] for d in resposta.json()]

        assert "paula" in ids
        assert "joao" not in ids
        assert "paulo" not in ids  # nunca retorna o próprio usuário

    def test_usuario_sem_conversa_aparece_com_status_false(self, client):
        """
        Scenario: Usuário encontrado sem conversa iniciada vem como "conversa vazia"
        ─────────────────────────────────────────────────
        Given existe "carla", com quem "paulo" nunca conversou
        When "paulo" busca por "ca"
        Then "carla" é retornada com status False e sem última mensagem
        """
        _registrar(client, "paulo", "paulo@email.com", "81900000001")
        _registrar(client, "carla", "carla@email.com", "81900000004")

        cabecalho = _logar(client, "paulo@email.com")
        resposta = client.get("/conversas/buscar?q=ca", headers=cabecalho)

        assert resposta.status_code == 200
        dados = resposta.json()

        carla = next(d for d in dados if d["id"] == "carla")
        assert carla["status"] is False
        assert carla["last_message"] is None

    def test_conversa_existente_vem_antes_de_usuario_novo(self, client):
        """
        Scenario: Conversas existentes têm prioridade sobre usuários novos
        ─────────────────────────────────────────────────
        Given "paulo" já conversou com "paula", mas nunca com "pamela"
        When "paulo" busca por "pa"
        Then "paula" (existente) aparece antes de "pamela" (status False)
        """
        _registrar(client, "paulo", "paulo@email.com", "81900000001")
        _registrar(client, "paula", "paula@email.com", "81900000003")
        _registrar(client, "pamela", "pamela@email.com", "81900000005")

        _enviar_mensagem("paulo", "paula", "oi paula")

        cabecalho = _logar(client, "paulo@email.com")
        resposta = client.get("/conversas/buscar?q=pa", headers=cabecalho)

        dados = resposta.json()
        por_id = {d["id"]: d for d in dados}

        assert por_id["paula"]["status"] is True
        assert por_id["pamela"]["status"] is False
        assert dados.index(por_id["paula"]) < dados.index(por_id["pamela"])

    def test_isolamento_entre_usuarios_previne_idor(self, client):
        """
        Scenario: Um usuário não enxerga as conversas de outro
        ─────────────────────────────────────────────────
        Given "paulo" e "paula" trocaram mensagens
        And "joao" não tem nenhuma conversa
        When "joao" (autenticado) busca com q vazio
        Then ele recebe uma lista vazia — não vê a conversa de "paulo"
        """
        _registrar(client, "paulo", "paulo@email.com", "81900000001")
        _registrar(client, "paula", "paula@email.com", "81900000003")
        _registrar(client, "joao", "joao@email.com", "81900000002")

        _enviar_mensagem("paulo", "paula", "segredo")

        cabecalho = _logar(client, "joao@email.com")
        resposta = client.get("/conversas/buscar", headers=cabecalho)

        assert resposta.status_code == 200
        assert resposta.json() == []

    def test_grupo_que_participo_aparece_na_lista(self, client):
        """
        Scenario: Grupos dos quais o usuário participa entram na lista
        ─────────────────────────────────────────────────
        Given "paulo" participa do grupo "Paladinos"
        When ele busca com q vazio
        Then o grupo aparece com tipo "grupo", status True e sem última mensagem
        """
        _registrar(client, "paulo", "paulo@email.com", "81900000001")
        id_grupo = _criar_grupo("Paladinos", "paulo")

        cabecalho = _logar(client, "paulo@email.com")
        resposta = client.get("/conversas/buscar", headers=cabecalho)

        dados = resposta.json()
        grupo = next(d for d in dados if d["tipo"] == "grupo")

        assert grupo["id"] == id_grupo
        assert grupo["nome"] == "Paladinos"
        assert grupo["status"] is True
        assert grupo["last_message"] is None
