from pytest_bdd import scenario, given, when, then, parsers
import app.contacts_store as contacts_store


@scenario('autenticacao.feature', 'Login com credenciais válidas')
def test_login_com_credenciais_validas():
    pass


@scenario('autenticacao.feature', 'Login com senha incorreta')
def test_login_com_senha_incorreta():
    pass


@scenario('autenticacao.feature', 'Login com e-mail inexistente')
def test_login_email_inexistente():
    pass


# ── Given ─────────────────────────────────────────────────────────────────────

@given(parsers.parse('o usuário "{email}" com senha "{senha}" está registrado no sistema'))
def usuario_registrado_no_sistema(client, email, senha):
    response = client.post('/auth/register', json={
        'usuario': email.split('@')[0],
        'email': email,
        'telefone': '(88) 988888888',
        'senha': senha,
    })
    assert response.status_code == 201


@given(parsers.parse('o usuário "{email}" com senha "{senha}" está cadastrado'))
def usuario_cadastrado(client, email, senha):
    response = client.post('/auth/register', json={
        'usuario': email.split('@')[0],
        'email': email,
        'telefone': '(88) 988888888',
        'senha': senha,
    })
    assert response.status_code == 201


@given(parsers.parse('o usuário "{email}" possui os contatos "{contato1}" e "{contato2}"'))
def usuario_possui_contatos(email, contato1, contato2):
    contacts_store.user_contacts[email] = [contato1, contato2]


@given('o sistema não possui nenhum usuário cadastrado')
def sistema_sem_usuarios():
    """Garantido pelo fixture setup_database que limpa o banco antes de cada teste."""
    pass


# ── When ──────────────────────────────────────────────────────────────────────

@when(parsers.parse('envio uma requisição de login com e-mail "{email}" e senha "{senha}"'))
def envio_requisicao_login(client, context, email, senha):
    response = client.post('/auth/login', json={
        'email': email,
        'senha': senha,
    })
    context['response'] = response


# ── Then ──────────────────────────────────────────────────────────────────────

@then(parsers.parse('o sistema retorna status {status:d}'))
def sistema_retorna_status(context, status):
    assert context['response'].status_code == status


@then(parsers.parse('o corpo da resposta contém o erro "{erro}"'))
def corpo_contem_erro(context, erro):
    assert context['response'].json().get('detail') == erro


@then('o corpo da resposta contém um token de acesso')
def corpo_contem_token(context):
    assert 'access_token' in context['response'].json()


@then('o corpo da resposta contém expires_in positivo')
def corpo_contem_expires_in(context):
    assert context['response'].json().get('expires_in', 0) > 0


@then(parsers.parse('o corpo da resposta contém a mensagem de boas-vindas "{mensagem}"'))
def corpo_contem_boas_vindas(context, mensagem):
    assert context['response'].json().get('welcome_message') == mensagem


@then(parsers.parse('o corpo da resposta contém o contato "{contato}" na lista'))
def corpo_contem_contato(context, contato):
    assert contato in context['response'].json().get('contacts', [])


@then('o corpo da resposta não contém token de acesso')
def corpo_nao_contem_token(context):
    assert 'access_token' not in context['response'].json()


@then(parsers.parse('o usuário "{email}" ainda consegue autenticar com a senha "{senha}"'))
def usuario_ainda_autentica(client, email, senha):
    response = client.post('/auth/login', json={
        'email': email,
        'senha': senha,
    })
    assert response.status_code == 200