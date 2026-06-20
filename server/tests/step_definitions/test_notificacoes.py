import pytest
from pytest_bdd import scenario, given, when, then, parsers
from app.models.mensagem import MensagemModel
from app.models.recebe import RecebeModel
from app.models.user import UserModel
from app.database import get_db
from main import app


@scenario('../../features/Notificacoes_Alertas.feature', 'Badge zerado ao abrir conversa')
def test_badge_zerado_ao_abrir_conversa():
    pass


@scenario('../../features/Notificacoes_Alertas.feature', 'Feedback de falha de conexão ao tentar atualizar notificações')
def test_feedback_falha_conexao():
    pass


@scenario('../../features/Notificacoes_Alertas.feature', 'Erro interno do servidor ao consultar badges')
def test_erro_interno_servidor_badges():
    pass


@pytest.fixture
def contexto(client):
    estado = {
        "db": next(app.dependency_overrides[get_db]()),
        "usuario_atual": None,
        "contato": None,
        "response": None,
    }
    yield estado


@given(parsers.parse('que o usuário "{usuario}" está autenticado no sistema'))
def usuario_autenticado(client, contexto, usuario):
    # Registrar usuário
    client.post('/auth/register', json={
        'usuario': usuario,
        'email': f'{usuario}@email.com',
        'telefone': f'81999{abs(hash(usuario)) % 100000:05d}',
        'senha': '123456',
    })
    
    # Fazer login para obter token
    response = client.post('/auth/login', json={
        'email': f'{usuario}@email.com',
        'senha': '123456',
    })
    
    contexto['usuario_atual'] = usuario
    contexto['token'] = response.json()['access_token']


@given(parsers.parse('o usuário "{usuario}" possui {quantidade:d} mensagens não lidas de "{contato}"'))
def mensagens_nao_lidas(client, contexto, usuario, quantidade, contato):
    # Registrar contato
    client.post('/auth/register', json={
        'usuario': contato,
        'email': f'{contato}@email.com',
        'telefone': f'81999{abs(hash(contato)) % 100000:05d}',
        'senha': '123456',
    })
    
    db = contexto['db']
    contexto['contato'] = contato
    
    # Criar mensagens não lidas
    for i in range(quantidade):
        mensagem = MensagemModel(
            timestamp=f"2026-06-10 10:0{i}:00",
            texto=f"Mensagem {i+1}",
            status_envio="ENVIADO",
            usuario=contato,
            id_grupo=None
        )
        db.add(mensagem)
        db.commit()
        db.refresh(mensagem)
        
        recebimento = RecebeModel(
            usuario=usuario,
            id_mensagem=mensagem.id_mensagem,
            lida=0
        )
        db.add(recebimento)
        db.commit()


@when(parsers.parse('"{usuario}" consulta os badges de notificação'))
def consultar_badges(client, contexto, usuario):
    response = client.get(
        '/api/v1/notifications/badges',
        headers={'Authorization': f"Bearer {contexto['token']}"}
    )
    contexto['response'] = response


@when(parsers.parse('"{usuario}" abre a conversa com "{contato}"'))
def abrir_conversa(client, contexto, usuario, contato):
    response = client.post(
        f'/mensagens/{usuario}/{contato}/lidas',
        headers={'Authorization': f"Bearer {contexto['token']}"}
    )
    contexto['response'] = response


@then(parsers.parse('o sistema retorna os badges com {quantidade:d} mensagens não lidas de "{contato}"'))
def verificar_badges(contexto, quantidade, contato):
    dados = contexto['response'].json()
    assert dados.get(contato) == quantidade


@then(parsers.parse('o badge de "{contato}" é zerado'))
def verificar_badge_zerado(client, contexto, contato):
    # Consultar badges novamente
    response = client.get(
        '/api/v1/notifications/badges',
        headers={'Authorization': f"Bearer {contexto['token']}"}
    )
    dados = response.json()
    assert dados.get(contato) is None or dados.get(contato) == 0


@then(parsers.parse('todas as mensagens de "{contato}" ficam marcadas como lidas'))
def verificar_mensagens_lidas(contexto, contato):
    db = contexto['db']
    mensagens_nao_lidas = (
        db.query(RecebeModel)
        .join(MensagemModel, RecebeModel.id_mensagem == MensagemModel.id_mensagem)
        .filter(RecebeModel.usuario == contexto['usuario_atual'])
        .filter(MensagemModel.usuario == contato)
        .filter(RecebeModel.lida == 0)
        .all()
    )
    assert len(mensagens_nao_lidas) == 0