from __future__ import annotations

from datetime import datetime
import json

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app import database
from app.core.ws_manager import gerenciador
from app.models.mensagem import MensagemModel
from app.models.recebe import RecebeModel

router = APIRouter(tags=["Chat Realtime"])

STATUS_ENVIADO = "ENVIADO"
STATUS_ENTREGUE = "ENTREGUE"
STATUS_LIDO = "LIDO"


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _agora() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _json(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False)


def _mensagem_payload(
    mensagem: MensagemModel,
    destinatario: str | None = None,
    client_id: str | None = None,
) -> dict:
    payload = {
        "type": "message",
        "id_mensagem": mensagem.id_mensagem,
        "remetente": mensagem.usuario,
        "para": destinatario,
        "texto": mensagem.texto,
        "status": mensagem.status_envio or STATUS_ENVIADO,
        "timestamp": mensagem.timestamp,
    }
    if client_id:
        payload["client_id"] = client_id
    return payload


def _status_payload(ids_mensagens: list[int], status_envio: str) -> dict:
    return {
        "type": "status_update",
        "ids_mensagens": ids_mensagens,
        "status": status_envio,
    }


def _extrair_pacote(texto_recebido: str) -> dict:
    try:
        pacote = json.loads(texto_recebido)
    except json.JSONDecodeError:
        return {"type": "message", "texto": texto_recebido}

    if not isinstance(pacote, dict):
        return {"type": "message", "texto": texto_recebido}

    pacote.setdefault("type", "message")
    return pacote


def _criar_mensagem(
    db: Session,
    remetente: str,
    texto: str,
    destinatario: str | None,
) -> MensagemModel:
    status_envio = (
        STATUS_ENTREGUE
        if destinatario and gerenciador.esta_online(destinatario)
        else STATUS_ENVIADO
    )
    nova_mensagem = MensagemModel(
        timestamp=_agora(),
        texto=texto,
        status_envio=status_envio,
        usuario=remetente,
        id_grupo=None,
    )
    db.add(nova_mensagem)
    db.commit()
    db.refresh(nova_mensagem)

    if destinatario:
        db.add(
            RecebeModel(
                usuario=destinatario,
                id_mensagem=nova_mensagem.id_mensagem,
                lida=0,
            )
        )
        db.commit()
        db.refresh(nova_mensagem)

    return nova_mensagem


def _marcar_lidas(
    db: Session,
    leitor: str,
    remetente: str | None = None,
    ids_mensagens: list[int] | None = None,
) -> dict[str, list[int]]:
    consulta = (
        db.query(RecebeModel, MensagemModel)
        .join(MensagemModel, MensagemModel.id_mensagem == RecebeModel.id_mensagem)
        .filter(RecebeModel.usuario == leitor)
        .filter(or_(RecebeModel.lida.is_(None), RecebeModel.lida != 1))
    )

    if remetente:
        consulta = consulta.filter(MensagemModel.usuario == remetente)

    if ids_mensagens:
        consulta = consulta.filter(MensagemModel.id_mensagem.in_(ids_mensagens))

    por_remetente: dict[str, list[int]] = {}

    for recebimento, mensagem in consulta.all():
        recebimento.lida = 1
        mensagem.status_envio = STATUS_LIDO
        if mensagem.usuario:
            por_remetente.setdefault(mensagem.usuario, []).append(mensagem.id_mensagem)

    db.commit()
    return por_remetente


async def _notificar_status(por_remetente: dict[str, list[int]], status_envio: str):
    for remetente, ids_mensagens in por_remetente.items():
        if ids_mensagens:
            await gerenciador.enviar_para_usuario(
                remetente,
                _status_payload(ids_mensagens, status_envio),
            )


async def _entregar_mensagens_pendentes(usuario: str):
    with database.SessionLocal() as db:
        pendentes = (
            db.query(MensagemModel)
            .join(RecebeModel, MensagemModel.id_mensagem == RecebeModel.id_mensagem)
            .filter(RecebeModel.usuario == usuario)
            .filter(MensagemModel.status_envio == STATUS_ENVIADO)
            .order_by(MensagemModel.id_mensagem.asc())
            .all()
        )

        por_remetente: dict[str, list[int]] = {}
        payloads = []
        for mensagem in pendentes:
            mensagem.status_envio = STATUS_ENTREGUE
            payloads.append(_mensagem_payload(mensagem, destinatario=usuario))
            if mensagem.usuario:
                por_remetente.setdefault(mensagem.usuario, []).append(mensagem.id_mensagem)

        db.commit()

    for payload in payloads:
        await gerenciador.enviar_para_usuario(usuario, payload)

    await _notificar_status(por_remetente, STATUS_ENTREGUE)


@router.websocket("/ws/{nome_usuario}")
async def endpoint_websocket(websocket: WebSocket, nome_usuario: str):
    await gerenciador.conectar(nome_usuario, websocket)
    await _entregar_mensagens_pendentes(nome_usuario)

    try:
        while True:
            texto_recebido = await websocket.receive_text()
            if not texto_recebido.strip():
                continue

            pacote = _extrair_pacote(texto_recebido)

            if pacote.get("type") == "read":
                with database.SessionLocal() as db:
                    por_remetente = _marcar_lidas(
                        db,
                        leitor=nome_usuario,
                        remetente=pacote.get("conversa_com"),
                        ids_mensagens=pacote.get("ids_mensagens"),
                    )
                await _notificar_status(por_remetente, STATUS_LIDO)
                continue

            texto_limpo = str(pacote.get("texto", "")).strip()
            if not texto_limpo:
                continue

            destinatario = pacote.get("para")
            client_id = pacote.get("client_id")

            with database.SessionLocal() as db:
                nova_mensagem = _criar_mensagem(
                    db,
                    remetente=nome_usuario,
                    texto=texto_limpo,
                    destinatario=destinatario,
                )
                payload = _mensagem_payload(nova_mensagem, destinatario, client_id)

            if destinatario:
                await gerenciador.enviar_para_usuario(destinatario, payload)
            else:
                await gerenciador.enviar_mensagem(_json(payload), remetente=websocket)

            await gerenciador.enviar_para_usuario(nome_usuario, payload)

    except WebSocketDisconnect:
        pass
    finally:
        await gerenciador.desconectar(websocket)


@router.get("/mensagens/{remetente}/{destinatario}")
def obter_historico_mensagens(
    remetente: str,
    destinatario: str,
    db: Session = Depends(get_db),
):
    historico = (
        db.query(MensagemModel, RecebeModel)
        .join(RecebeModel, MensagemModel.id_mensagem == RecebeModel.id_mensagem)
        .filter(
            or_(
                and_(MensagemModel.usuario == remetente, RecebeModel.usuario == destinatario),
                and_(MensagemModel.usuario == destinatario, RecebeModel.usuario == remetente),
            )
        )
        .order_by(MensagemModel.id_mensagem.asc())
        .all()
    )

    return [
        {
            "id_mensagem": msg.id_mensagem,
            "remetente": msg.usuario,
            "para": recebimento.usuario,
            "texto": msg.texto,
            "status": msg.status_envio or STATUS_ENVIADO,
            "lida": bool(recebimento.lida),
            "timestamp": msg.timestamp,
        }
        for msg, recebimento in historico
    ]


@router.post("/mensagens/{usuario}/{contato}/lidas")
async def marcar_conversa_como_lida(
    usuario: str,
    contato: str,
    db: Session = Depends(get_db),
):
    por_remetente = _marcar_lidas(db, leitor=usuario, remetente=contato)
    await _notificar_status(por_remetente, STATUS_LIDO)

    ids_mensagens = [
        id_mensagem
        for ids_do_remetente in por_remetente.values()
        for id_mensagem in ids_do_remetente
    ]
    return {"ids_mensagens": ids_mensagens, "status": STATUS_LIDO}


@router.get("/presenca/{usuario}")
def obter_presenca_usuario(usuario: str):
    return gerenciador.obter_presenca(usuario)


class EditarMensagemRequest(BaseModel):
    usuario: str
    novo_texto: str


@router.put("/mensagens/{id_mensagem}")
def editar_mensagem(
    id_mensagem: int,
    dados: EditarMensagemRequest,
    db: Session = Depends(get_db),
):
    mensagem = db.query(MensagemModel).filter(
        MensagemModel.id_mensagem == id_mensagem
    ).first()

    if not mensagem:
        raise HTTPException(status_code=404, detail="Mensagem nao encontrada")

    if mensagem.usuario != dados.usuario:
        raise HTTPException(
            status_code=403,
            detail="Usuario nao autorizado a editar esta mensagem",
        )

    mensagem.texto = dados.novo_texto
    db.commit()
    db.refresh(mensagem)

    return {
        "mensagem": "Mensagem editada com sucesso",
        "id_mensagem": mensagem.id_mensagem,
        "texto": mensagem.texto,
        "editada": True,
    }


class ExcluirMensagemRequest(BaseModel):
    usuario: str


@router.delete("/mensagens/{id_mensagem}")
def excluir_mensagem(
    id_mensagem: int,
    dados: ExcluirMensagemRequest,
    db: Session = Depends(get_db),
):
    mensagem = db.query(MensagemModel).filter(
        MensagemModel.id_mensagem == id_mensagem
    ).first()

    if not mensagem:
        raise HTTPException(status_code=404, detail="Mensagem nao encontrada")

    if mensagem.usuario != dados.usuario:
        raise HTTPException(
            status_code=403,
            detail="Usuario nao autorizado a excluir esta mensagem",
        )

    recebimentos = db.query(RecebeModel).filter(
        RecebeModel.id_mensagem == id_mensagem
    ).all()

    for recebimento in recebimentos:
        db.delete(recebimento)

    db.delete(mensagem)
    db.commit()

    return {
        "mensagem": "Mensagem excluida com sucesso",
        "id_mensagem": id_mensagem,
    }
