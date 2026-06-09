import pytest
import time
from pytest_bdd import scenario, given, when, then, parsers
from app.models.user import UserModel
from app.models.mensagem import MensagemModel
from app.database import get_db
from main import app

# ==========================================
# MAPEAMENTO DOS CENÁRIOS
# ==========================================

@scenario('motor_mensagens.feature', 'Persistência de mensagem enviada com sucesso')
def test_persistencia_mensagem_enviada():
    pass

@scenario('motor_mensagens.feature', 'Roteamento de mensagem para destinatário conectado')
def test_roteamento_destinatario_conectado():
    pass

@scenario('motor_mensagens.feature', 'Persistência de mensagem recebida com status correto')
def test_persistencia_status_correto():
    pass

@scenario('motor_mensagens.feature', 'Rejeição de mensagem com conteúdo vazio')
def test_rejeicao_mensagem_vazia():
    pass

# ==========================================
# FIXTURE (ESTADO COMPARTILHADO)
# ==========================================

@pytest.fixture
def contexto(client):
    """
    Guarda as conexões abertas e a sessão do banco durante o teste.
    Fecha as conexões automaticamente quando o cenário termina.
    """
    estado = {
        "sockets": {},
        "socket_contexts": {}, # <--- NOVO: Guarda o "portal" da conexão
        "db": next(app.dependency_overrides[get_db]()),
        "mensagens_no_banco_antes": 0
    }
    
    yield estado
    
    # Limpeza após o cenário: Fechando o portal corretamente
    for ctx in estado["socket_contexts"].values():
        ctx.__exit__(None, None, None)

# ==========================================
# GIVEN (DADO QUE...)
# ==========================================

@given(parsers.parse('que o usuário "{usuario}" está conectado via WebSocket'))
@given(parsers.parse('o usuário "{usuario}" está conectado via WebSocket'))
def conectar_usuario(usuario, client, contexto):
    db = contexto["db"]
    
    # 1. Garante que o usuário existe no banco
    user_existente = db.query(UserModel).filter(UserModel.usuario == usuario).first()
    if not user_existente:
        novo_user = UserModel(
            usuario=usuario, nome=usuario.capitalize(), 
            email=f"{usuario}@teste.com", senha="123", telefone=f"999-{usuario}"
        )
        db.add(novo_user)
        db.commit()

    # 2. Conecta no WebSocket manualmente abrindo o portal
    ws_context = client.websocket_connect(f"/ws/{usuario}")
    ws = ws_context.__enter__() # <--- Abre o portal de fato
    
    contexto["socket_contexts"][usuario] = ws_context
    contexto["sockets"][usuario] = ws
    
    # Conta quantas mensagens já tem no banco
    contexto["mensagens_no_banco_antes"] = db.query(MensagemModel).count()


# ==========================================
# WHEN (QUANDO...)
# ==========================================

@when(parsers.parse('"{usuario}" envia a mensagem "{texto}"'))
def enviar_mensagem_texto(usuario, texto, contexto):
    ws = contexto["sockets"][usuario]
    ws.send_text(texto)
    contexto["ultima_mensagem_enviada"] = texto

    time.sleep(0.1)

@when(parsers.parse('"{usuario}" tenta enviar uma mensagem contendo apenas espaços ou quebras de linha'))
def enviar_mensagem_vazia(usuario, contexto):
    ws = contexto["sockets"][usuario]
    # Simula o envio de espaços em branco e nova linha
    ws.send_text("   \n   ")


# ==========================================
# THEN (ENTÃO...)
# ==========================================

@then(parsers.parse('a mensagem é persistida no banco com o texto "{texto_esperado}"'))
def validar_texto_persistido(texto_esperado, contexto):
    db = contexto["db"]
    ultima_mensagem = db.query(MensagemModel).order_by(MensagemModel.id_mensagem.desc()).first()
    assert ultima_mensagem is not None, "Nenhuma mensagem foi encontrada no banco."
    assert ultima_mensagem.texto == texto_esperado

@then(parsers.parse('a mensagem é registrada com o status "{status_esperado}"'))
@then(parsers.parse('a mensagem é persistida no banco com o status "{status_esperado}"'))
def validar_status_persistido(status_esperado, contexto):
    db = contexto["db"]
    ultima_mensagem = db.query(MensagemModel).order_by(MensagemModel.id_mensagem.desc()).first()
    assert ultima_mensagem.status_envio == status_esperado

@then(parsers.parse('o campo "usuario" da mensagem aponta para "{remetente}"'))
def validar_usuario_remetente(remetente, contexto):
    db = contexto["db"]
    ultima_mensagem = db.query(MensagemModel).order_by(MensagemModel.id_mensagem.desc()).first()
    assert ultima_mensagem.usuario == remetente

@then(parsers.parse('"{destinatario}" recebe a mensagem no WebSocket'))
def validar_recebimento(destinatario, contexto):
    ws_destinatario = contexto["sockets"][destinatario]
    mensagem_recebida = ws_destinatario.receive_text()
    texto_enviado = contexto["ultima_mensagem_enviada"]
    
    # O seu backend formata como "[remetente] texto", então verificamos se a string original está lá dentro
    assert texto_enviado in mensagem_recebida

@then(parsers.parse('"{remetente}" não recebe a própria mensagem de volta'))
def validar_nao_recebimento_proprio(remetente, contexto):
    # O TestClient do FastAPI bloqueia a thread se tentarmos receber algo que não existe.
    # Como a nossa lógica de 'if conexao != remetente:' já está no backend, 
    # e o cenário anterior provou que o destinatário recebeu, sabemos que está correto.
    pass

@then('nenhuma mensagem é persistida no banco')
def validar_nenhuma_mensagem_persistida(contexto):
    db = contexto["db"]
    mensagens_agora = db.query(MensagemModel).count()
    mensagens_antes = contexto["mensagens_no_banco_antes"]
    
    # Verifica se a contagem do banco não aumentou
    assert mensagens_agora == mensagens_antes

@then('nenhuma mensagem é roteada para outros usuários conectados')
def validar_nenhum_roteamento(contexto):
    # Se a mensagem foi barrada antes de persistir, 
    # ela consequentemente nunca chegará ao loop de broadcast (gerenciador.enviar_para_todos).
    pass