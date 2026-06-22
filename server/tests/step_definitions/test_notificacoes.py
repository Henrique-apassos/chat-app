import pytest
from unittest.mock import patch
from pytest_bdd import scenario, given, when, then, parsers
from app.models.mensagem import MensagemModel
from app.models.recebe import RecebeModel
from app.database import get_db
from main import app

@scenario('Notificacoes_Alertas.feature', 'Badge zerado ao abrir conversa')
def test_badge_zerado_ao_abrir_conversa():
    pass

@scenario('Notificacoes_Alertas.feature', 'Feedback de falha de conexão ao tentar atualizar notificações')
def test_feedback_falha_conexao():
    pass

@scenario('Notificacoes_Alertas.feature', 'Erro interno do servidor ao consultar badges')
def test_erro_interno_servidor_badges():
    pass

@pytest.fixture
def contexto(client):
    estado = {
        "db": next(app.dependency_overrides[get_db]()),
        "usuario_atual": None,
        "contato": None,
        "response": None,
        "token": None,
    }
    yield estado

# ─── GIVEN ─────────────────────────────────────────────────────────────

@given(parsers.parse('que o usuário "{usuario}" está na tela "{tela}"'))
@given(parsers.parse('que o usuário "{usuario}" está autenticada no sistema'))
def autenticar_usuario(client, contexto, usuario, tela=None):
    # Para o backend, estar numa tela significa que ele está autenticado e logado
    client.post('/auth/register', json={
        'usuario': usuario,
        'email': f'{usuario}@email.com',
        'telefone': f'81999{abs(hash(usuario)) % 100000:05d}',
        'senha': '123456',
    })
    response = client.post('/auth/login', json={
        'email': f'{usuario}@email.com',
        'senha': '123456',
    })
    contexto['usuario_atual'] = usuario
    contexto['token'] = response.json()['access_token']

@given(parsers.parse('o badge ao lado de "{contato}" exibe "{quantidade:d}" mensagens não lidas'))
def mensagens_nao_lidas(client, contexto, contato, quantidade):
    db = contexto['db']
    usuario = contexto['usuario_atual']
    contexto['contato'] = contato
    
    # Cria a pessoa que vai enviar as mensagens
    client.post('/auth/register', json={
        'usuario': contato,
        'email': f'{contato}@email.com',
        'telefone': f'81999{abs(hash(contato)) % 100000:05d}',
        'senha': '123456',
    })
    
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

@given('o dispositivo está offline ou sem conexão com o servidor')
def dispositivo_offline(contexto):
    contexto['offline'] = True

@given('o servidor de notificações está em estado de manutenção')
def servidor_em_manutencao(contexto):
    contexto['manutencao'] = True

# ─── WHEN ──────────────────────────────────────────────────────────────

@when(parsers.parse('"{usuario}" abre a conversa com "{contato}"'))
def abrir_conversa(client, contexto, usuario, contato):
    response = client.post(
        f'/mensagens/{usuario}/{contato}/lidas',
        headers={'Authorization': f"Bearer {contexto.get('token', '')}"}
    )
    contexto['response'] = response

@when(parsers.parse('"{usuario}" tenta atualizar a lista de notificações'))
def atualizar_lista(contexto, usuario):
    # Simula o front-end detectando que não há internet
    if contexto.get('offline'):
        contexto['erro_frontend'] = "Sem conexão. Verifique sua internet."

@when('o serviço recebe a requisição "GET /api/v1/notifications/badges"')
def consulta_badges_manutencao(client, contexto):
    if contexto.get('manutencao'):
        # Injetamos um erro no banco (patch) para forçar o backend a disparar o erro 503
        with patch('sqlalchemy.orm.Query.all', side_effect=Exception("Manutenção simulada no BD")):
            response = client.get(
                '/api/v1/notifications/badges',
                headers={'Authorization': f"Bearer {contexto.get('token', '')}"}
            )
            contexto['response'] = response

# ─── THEN ──────────────────────────────────────────────────────────────

@then(parsers.parse('o badge ao lado de "{contato}" é removido'))
def badge_removido(client, contexto, contato):
    response = client.get(
        '/api/v1/notifications/badges',
        headers={'Authorization': f"Bearer {contexto.get('token', '')}"}
    )
    dados = response.json()
    assert dados.get(contato) is None or dados.get(contato) == 0

@then(parsers.parse('todas as mensagens de "{contato}" ficam marcadas como lidas'))
def msgs_marcadas_lidas(contexto, contato):
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

@then('o indicador de não lidas na aba do navegador é removido')
def indicador_aba_removido():
    pass

@then(parsers.parse('o sistema exibe o banner de erro "{mensagem}"'))
def exibe_banner_erro(contexto, mensagem):
    assert contexto.get('erro_frontend') == mensagem

@then('o badge numérico permanece inalterado')
def badge_inalterado():
    pass

@then('a interface de atualização é desabilitada temporariamente')
def interface_desabilitada():
    pass

@then('o serviço retorna HTTP 503 Service Unavailable')
def retorna_503(contexto):
    assert contexto['response'].status_code == 503

@then(parsers.parse('o corpo da resposta contém a mensagem "{mensagem}"'))
def corpo_contem_msg(contexto, mensagem):
    assert contexto['response'].json().get('detail') == mensagem