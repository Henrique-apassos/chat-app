from pytest_bdd import scenario, given, when, then, parsers
import app.contacts_store as contacts_store


@scenario('autenticacao.feature', 'Login com credenciais válidas')
def test_login_com_credenciais_validas():
    pass


@scenario('autenticacao.feature', 'Login com senha incorreta')
def test_login_com_senha_incorreta():
    pass


@given(parsers.parse('o usuário "{email}" com senha "{senha}" está registrado no sistema'))
def usuario_registrado_no_sistema(client, email, senha):
    response = client.post('/auth/register', json={
        'nome_usuario': email.split('@')[0],
        'email': email,
        'telefone': '(88) 988888888',
        'senha': senha,
    })
    assert response.status_code == 201


@given(parsers.parse('o usuário "{email}" com senha "{senha}" está cadastrado'))
def usuario_cadastrado(client, email, senha):
    response = client.post('/auth/register', json={
        'nome_usuario': email.split('@')[0],
        'email': email,
        'telefone': '(88) 988888888',
        'senha': senha,
    })
    assert response.status_code == 201


@given(parsers.parse('o usuário "{email}" possui os contatos "{contato1}" e "{contato2}"'))
def usuario_possui_contatos(email, contato1, contato2):
    contacts_store.user_contacts[email] = [contato1, contato2]


@given(parsers.parse('estou na tela de "{tela}" do sistema'))
def estou_na_tela_do_sistema(tela):
    pass


@given('não estou logado no sistema')
def nao_estou_logado():
    pass


@when(parsers.parse('informo e-mail "{email}" e senha "{senha}"'))
def informo_email_e_senha(context, email, senha):
    context['email'] = email
    context['senha'] = senha


@when(parsers.parse('clico no botão "{botao}"'))
def clico_no_botao_entrar(client, context, botao):
    response = client.post('/auth/login', json={
        'email': context.get('email', ''),
        'senha': context.get('senha', ''),
    })
    context['response'] = response


@then(parsers.parse('o sistema exibe mensagem de boas-vindas "{mensagem}"'))
def sistema_exibe_boas_vindas(context, mensagem):
    response = context['response']
    assert response.status_code == 200
    assert response.json().get('welcome_message') == mensagem


@then(parsers.parse('eu vejo o contato "{contato}" na lista'))
def eu_vejo_contato_na_lista(context, contato):
    contacts = context['response'].json().get('contacts', [])
    assert contato in contacts


@then('o sistema me mantém logado por um tempo determinado')
def sistema_mantem_logado(context):
    body = context['response'].json()
    assert 'access_token' in body
    assert body.get('expires_in', 0) > 0


@then('o sistema deve impedir o acesso')
def sistema_impede_acesso(context):
    assert context['response'].status_code == 401


@then(parsers.parse('exibir mensagem "{mensagem}"'))
def exibir_mensagem(context, mensagem):
    assert context['response'].json().get('detail') == mensagem


@then(parsers.parse('o sistema NÃO me mantém logado como "{email}"'))
def sistema_nao_mantem_logado(context, email):
    assert 'access_token' not in context['response'].json()


@then(parsers.parse('o usuário "{email}" permanece com senha "{senha}" inalterada'))
def usuario_permanece_com_senha(client, email, senha):
    response = client.post('/auth/login', json={
        'email': email,
        'senha': senha,
    })
    assert response.status_code == 200

@scenario('autenticacao.feature', 'Login com e-mail inexistente')
def test_login_email_inexistente():
    pass


@given('o sistema não possui nenhum usuário cadastrado')
def sistema_sem_usuarios():
    """Garantido pelo fixture setup_database que limpa o banco antes de cada teste."""
    pass