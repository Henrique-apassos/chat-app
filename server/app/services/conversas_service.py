"""
Serviço de busca de conversas.

Não existe tabela 'conversa' no banco — o conceito é *derivado*:

- Conversas 1:1  → das tabelas 'mensagem' (remetente) + 'recebe' (destinatário),
                   considerando apenas mensagens sem grupo (id_grupo nulo).
- Conversas de grupo → da tabela 'esta_em' (grupos que eu participo) + 'grupo'.

A busca é por PREFIXO e case-insensitive: "Pa" casa com "paulo", "paula", etc.
Retorna primeiro as conversas que já existem (ordenadas pela mais recente) e,
em seguida, os usuários encontrados com quem ainda não há conversa (status=False).

Segue o princípio da Responsabilidade Única (SRP): isola a regra de negócio da
camada de rota.
"""
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.esta_em import EstaModel
from app.models.grupo import GrupoModel
from app.models.mensagem import MensagemModel
from app.models.recebe import RecebeModel
from app.models.user import UserModel


class ConversasService:
    def __init__(self, db: Session):
        self.db = db

    # ── Auxiliares ─────────────────────────────────────────────────────────

    @staticmethod
    def _escapar_like(termo: str) -> str:
        """
        Neutraliza os curingas do LIKE ('%' e '_') para que o input seja tratado
        como texto literal. A proteção contra SQL Injection em si vem da
        parametrização do SQLAlchemy (bind parameters) — aspas e ';' já não têm
        efeito; aqui tratamos apenas os curingas do padrão de busca.
        """
        return (
            termo.replace("\\", "\\\\")
            .replace("%", "\\%")
            .replace("_", "\\_")
        )

    # ── Caso de uso principal ──────────────────────────────────────────────

    def buscar(self, usuario_atual: str, q: str = "") -> list[dict]:
        """
        Busca as conversas do usuário autenticado.

        Args:
            usuario_atual: nome de usuário extraído do JWT (nunca da URL).
            q: termo de busca (prefixo, case-insensitive). Vazio → todas as
               conversas existentes.

        Returns:
            Lista de itens no formato:
            {
                "tipo": "usuario" | "grupo",
                "id": <usuario:str | id_grupo:int>,
                "nome": <str>,
                "status": <bool>,           # True se a conversa já existe
                "last_message": {"remetente": str, "texto": str} | None
            }
        """
        prefixo = (q or "").strip().lower()

        existentes = self._conversas_existentes(usuario_atual, prefixo)

        # Ordena as existentes pela mensagem mais recente (id_mensagem maior).
        # Conversas sem mensagem (ex.: grupo recém-criado) vão para o fim do bloco.
        existentes.sort(key=lambda e: e["ordem"], reverse=True)
        resultado = [e["item"] for e in existentes]

        # Usuários ainda sem conversa só entram quando há termo de busca.
        if prefixo:
            ja_listados = {
                e["item"]["id"]
                for e in existentes
                if e["item"]["tipo"] == "usuario"
            }
            resultado.extend(
                self._usuarios_sem_conversa(usuario_atual, q.strip(), ja_listados)
            )

        return resultado

    # ── Conversas já existentes (1:1 + grupos) ─────────────────────────────

    def _conversas_existentes(self, usuario_atual: str, prefixo: str) -> list[dict]:
        itens: list[dict] = []
        itens.extend(self._conversas_1a1(usuario_atual, prefixo))
        itens.extend(self._conversas_de_grupo(usuario_atual, prefixo))
        return itens

    def _conversas_1a1(self, usuario_atual: str, prefixo: str) -> list[dict]:
        # Todas as mensagens 1:1 que me envolvem (como remetente OU destinatário),
        # da mais nova para a mais antiga.
        linhas = (
            self.db.query(
                MensagemModel.id_mensagem.label("id_mensagem"),
                MensagemModel.usuario.label("remetente"),
                MensagemModel.texto.label("texto"),
                RecebeModel.usuario.label("destinatario"),
            )
            .join(RecebeModel, MensagemModel.id_mensagem == RecebeModel.id_mensagem)
            .filter(MensagemModel.id_grupo.is_(None))
            .filter(
                or_(
                    MensagemModel.usuario == usuario_atual,
                    RecebeModel.usuario == usuario_atual,
                )
            )
            .order_by(MensagemModel.id_mensagem.desc())
            .all()
        )

        # Para cada parceiro, a primeira linha encontrada é a última mensagem
        # (porque a query veio ordenada de forma decrescente).
        ultimas: dict[str, object] = {}
        for linha in linhas:
            parceiro = (
                linha.destinatario
                if linha.remetente == usuario_atual
                else linha.remetente
            )
            if parceiro == usuario_atual:
                continue
            if parceiro not in ultimas:
                ultimas[parceiro] = linha

        if not ultimas:
            return []

        # Busca o 'nome' de exibição de cada parceiro.
        pessoas = {
            p.usuario: p
            for p in self.db.query(UserModel)
            .filter(UserModel.usuario.in_(list(ultimas.keys())))
            .all()
        }

        itens: list[dict] = []
        for parceiro, linha in ultimas.items():
            pessoa = pessoas.get(parceiro)
            nome = pessoa.nome if pessoa and pessoa.nome else parceiro

            if prefixo and not (
                parceiro.lower().startswith(prefixo)
                or nome.lower().startswith(prefixo)
            ):
                continue

            itens.append(
                {
                    "ordem": linha.id_mensagem,
                    "item": {
                        "tipo": "usuario",
                        "id": parceiro,
                        "nome": nome,
                        "status": True,
                        "last_message": {
                            "remetente": linha.remetente,
                            "texto": linha.texto,
                        },
                    },
                }
            )
        return itens

    def _conversas_de_grupo(self, usuario_atual: str, prefixo: str) -> list[dict]:
        grupos = (
            self.db.query(GrupoModel)
            .join(EstaModel, EstaModel.id_grupo == GrupoModel.id_grupo)
            .filter(EstaModel.usuario == usuario_atual)
            .all()
        )

        itens: list[dict] = []
        for grupo in grupos:
            nome = grupo.nome_grupo or ""
            if prefixo and not nome.lower().startswith(prefixo):
                continue

            # Última mensagem do grupo (pode não existir — envio de grupo ainda
            # não é implementado no motor de chat).
            ultima = (
                self.db.query(MensagemModel)
                .filter(MensagemModel.id_grupo == grupo.id_grupo)
                .order_by(MensagemModel.id_mensagem.desc())
                .first()
            )
            last_message = (
                {"remetente": ultima.usuario, "texto": ultima.texto}
                if ultima
                else None
            )

            itens.append(
                {
                    "ordem": ultima.id_mensagem if ultima else -1,
                    "item": {
                        "tipo": "grupo",
                        "id": grupo.id_grupo,
                        "nome": grupo.nome_grupo,
                        "status": True,
                        "last_message": last_message,
                    },
                }
            )
        return itens

    # ── Usuários ainda sem conversa (status=False) ─────────────────────────

    def _usuarios_sem_conversa(
        self,
        usuario_atual: str,
        termo: str,
        ja_listados: set[str],
    ) -> list[dict]:
        padrao = self._escapar_like(termo) + "%"

        consulta = (
            self.db.query(UserModel)
            .filter(UserModel.usuario != usuario_atual)
            .filter(
                or_(
                    UserModel.usuario.ilike(padrao, escape="\\"),
                    UserModel.nome.ilike(padrao, escape="\\"),
                )
            )
        )

        itens: list[dict] = []
        for pessoa in consulta.all():
            if pessoa.usuario in ja_listados:
                continue
            itens.append(
                {
                    "tipo": "usuario",
                    "id": pessoa.usuario,
                    "nome": pessoa.nome or pessoa.usuario,
                    "status": False,
                    "last_message": None,
                }
            )
        return itens
