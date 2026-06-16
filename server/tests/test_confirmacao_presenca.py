import json
from uuid import uuid4

from app import database
from app.models.mensagem import MensagemModel
from app.models.recebe import RecebeModel


def _usuario(prefixo):
    return f"{prefixo}_{uuid4().hex[:8]}"


def _registrar(client, usuario):
    return client.post(
        "/auth/register",
        json={
            "usuario": usuario,
            "email": f"{usuario}@email.com",
            "telefone": f"119{uuid4().hex[:8]}",
            "senha": "senha123",
        },
    )


def _receber_evento(ws, tipo, tentativas=4):
    for _ in range(tentativas):
        evento = json.loads(ws.receive_text())
        if evento.get("type") == tipo:
            return evento
    raise AssertionError(f"Evento {tipo} nao recebido")


def test_presenca_online_e_visto_por_ultimo(client):
    usuario = _usuario("joao")
    _registrar(client, usuario)

    resposta_offline = client.get(f"/presenca/{usuario}")
    assert resposta_offline.status_code == 200
    assert resposta_offline.json()["online"] is False

    with client.websocket_connect(f"/ws/{usuario}"):
        resposta_online = client.get(f"/presenca/{usuario}")
        assert resposta_online.json()["online"] is True
        assert resposta_online.json()["status"] == "Online"

    resposta_visto = client.get(f"/presenca/{usuario}")
    corpo = resposta_visto.json()
    assert corpo["online"] is False
    assert corpo["last_seen"] is not None


def test_mensagem_para_destinatario_conectado_fica_entregue(client):
    remetente = _usuario("ana")
    destinatario = _usuario("joao")
    _registrar(client, remetente)
    _registrar(client, destinatario)

    with client.websocket_connect(f"/ws/{remetente}") as ws_remetente:
        with client.websocket_connect(f"/ws/{destinatario}") as ws_destinatario:
            ws_remetente.send_text(json.dumps({
                "para": destinatario,
                "texto": "Ola, Joao!",
                "client_id": "teste-entrega",
            }))

            recebido = _receber_evento(ws_destinatario, "message")
            confirmado = _receber_evento(ws_remetente, "message")

    assert recebido["texto"] == "Ola, Joao!"
    assert recebido["status"] == "ENTREGUE"
    assert confirmado["client_id"] == "teste-entrega"
    assert confirmado["status"] == "ENTREGUE"

    db = database.SessionLocal()
    try:
        mensagem = db.query(MensagemModel).filter(
            MensagemModel.texto == "Ola, Joao!"
        ).one()
        recebimento = db.query(RecebeModel).filter(
            RecebeModel.id_mensagem == mensagem.id_mensagem,
            RecebeModel.usuario == destinatario,
        ).one()

        assert mensagem.status_envio == "ENTREGUE"
        assert recebimento.lida == 0
    finally:
        db.close()


def test_abrir_conversa_marca_mensagem_como_lida(client):
    remetente = _usuario("ana")
    destinatario = _usuario("joao")
    _registrar(client, remetente)
    _registrar(client, destinatario)

    with client.websocket_connect(f"/ws/{remetente}") as ws_remetente:
        ws_remetente.send_text(json.dumps({
            "para": destinatario,
            "texto": "Leia quando puder",
            "client_id": "teste-leitura",
        }))
        _receber_evento(ws_remetente, "message")

        resposta = client.post(f"/mensagens/{destinatario}/{remetente}/lidas")
        assert resposta.status_code == 200

        atualizacao = _receber_evento(ws_remetente, "status_update")
        assert atualizacao["status"] == "LIDO"

    db = database.SessionLocal()
    try:
        mensagem = db.query(MensagemModel).filter(
            MensagemModel.texto == "Leia quando puder"
        ).one()
        recebimento = db.query(RecebeModel).filter(
            RecebeModel.id_mensagem == mensagem.id_mensagem,
            RecebeModel.usuario == destinatario,
        ).one()

        assert mensagem.status_envio == "LIDO"
        assert recebimento.lida == 1
    finally:
        db.close()
