from __future__ import annotations

from collections import defaultdict
from datetime import datetime
import json

from fastapi import WebSocket


class GerenciadorDeConexao:
    """Gerencia conexoes WebSocket por usuario e estado de presenca."""

    def __init__(self):
        self.conexoes_por_usuario: dict[str, set[WebSocket]] = defaultdict(set)
        self.usuario_por_conexao: dict[WebSocket, str] = {}
        self.ultimo_acesso: dict[str, str] = {}

    async def conectar(self, usuario: str, websocket: WebSocket):
        await websocket.accept()
        self.conexoes_por_usuario[usuario].add(websocket)
        self.usuario_por_conexao[websocket] = usuario
        await self.notificar_presenca(usuario, online=True, exceto_usuario=usuario)

    async def desconectar(self, websocket: WebSocket):
        usuario = self.usuario_por_conexao.pop(websocket, None)
        if not usuario:
            return

        conexoes = self.conexoes_por_usuario.get(usuario)
        if conexoes:
            conexoes.discard(websocket)
            if not conexoes:
                self.conexoes_por_usuario.pop(usuario, None)

        if not self.esta_online(usuario):
            self.ultimo_acesso[usuario] = self._agora_iso()
            await self.notificar_presenca(usuario, online=False, exceto_usuario=usuario)

    def esta_online(self, usuario: str | None) -> bool:
        if not usuario:
            return False
        return bool(self.conexoes_por_usuario.get(usuario))

    def obter_presenca(self, usuario: str) -> dict:
        online = self.esta_online(usuario)
        last_seen = None if online else self.ultimo_acesso.get(usuario)
        return {
            "type": "presence_update",
            "usuario": usuario,
            "online": online,
            "last_seen": last_seen,
            "status": "Online" if online else "Visto por ultimo",
        }

    async def enviar_para_usuario(self, usuario: str, payload: dict) -> int:
        conexoes = list(self.conexoes_por_usuario.get(usuario, set()))
        entregues = 0

        for conexao in conexoes:
            try:
                await conexao.send_text(json.dumps(payload, ensure_ascii=False))
                entregues += 1
            except RuntimeError:
                await self.desconectar(conexao)

        return entregues

    async def enviar_mensagem(self, mensagem: str, remetente: WebSocket):
        """Mantem compatibilidade com o broadcast usado pelos testes antigos."""
        for conexao in list(self.usuario_por_conexao.keys()):
            if conexao == remetente:
                continue
            try:
                await conexao.send_text(mensagem)
            except RuntimeError:
                await self.desconectar(conexao)

    async def notificar_presenca(
        self,
        usuario: str,
        online: bool,
        exceto_usuario: str | None = None,
    ):
        payload = self.obter_presenca(usuario)
        payload["online"] = online
        if online:
            payload["last_seen"] = None
            payload["status"] = "Online"

        for destinatario in list(self.conexoes_por_usuario.keys()):
            if destinatario == exceto_usuario:
                continue
            await self.enviar_para_usuario(destinatario, payload)

    def _agora_iso(self) -> str:
        return datetime.now().isoformat(timespec="seconds")


gerenciador = GerenciadorDeConexao()
