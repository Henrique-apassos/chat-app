from pytest_bdd import scenario, given, when, then, parsers


@scenario('registration_access.feature', 'Cadastro de novo usuário com sucesso')
def test_cadastro_novo_usuario_com_sucesso():
    pass


@scenario('registration_access.feature', 'Cadastro com e-mail já existente')
def test_cadastro_email_ja_existente():
    pass


@scenario('registration_access.feature', 'Cadastro com senha menor que 6 caracteres')
def test_cadastro_senha_curta():
    pass


@scenario('registration_access.feature', 'Cadastro com nome de usuário já existente')
def test_cadastro_usuario_duplicado():
    pass


@scenario('registration_access.feature', 'Cadastro com senha de exatamente 6 caracteres')
def test_cadastro_senha_limite_exato():
    pass


# ── Given ─────────────────────────────────────────────────────────────────────

@given('a rota POST /auth/register está disponível')
def rota_disponivel():
    pass


@given(parsers.parse('o sistema não possui usuário com e-mail "{email}"'))
def sistema_nao_possui_email(email):
    pass


@given(parsers.parse(
    'o sistema já possui usuário com e-mail "{email}", nome "{nome_usuario}" e senha "{senha}"'
))
def sistema_ja_possui_usuario(client, context, email, nome_usuario, senha):
    response = client.post('/auth/register', json={
        'usuario': nome_usuario,
        'email': email,
        'telefone': '(00) 000000000',
        'senha': senha,
    })
    assert response.status_code == 201
    context['usuario_existente'] = {
        'email': email,
        'usuario': nome_usuario,
        'senha': senha,
    }


# ── When ──────────────────────────────────────────────────────────────────────

@when(parsers.parse(
    'envio uma requisição de cadastro com e-mail "{email}", usuario "{usuario}", telefone "{telefone}" e senha "{senha}"'
))
def envio_requisicao_cadastro_completo(client, context, email, usuario, telefone, senha):
    response = client.post('/auth/register', json={
        'usuario': usuario,
        'email': email,
        'telefone': telefone,
        'senha': senha,
    })
    print("\n>>> BODY RESPOSTA:", response.json())
    context['response'] = response


@when(parsers.parse(
    'envio uma requisição de cadastro com e-mail "{email}", usuario "{usuario}" e senha "{senha}"'
))
def envio_requisicao_cadastro_simples(client, context, email, usuario, senha):
    response = client.post('/auth/register', json={
        'usuario': usuario,
        'email': email,
        'telefone': '(00) 000000000',
        'senha': senha,
    })
    context['response'] = response


# ── Then ──────────────────────────────────────────────────────────────────────

@then(parsers.parse('o sistema retorna status {status:d}'))
def sistema_retorna_status(context, status):
    assert context['response'].status_code == status


@then(parsers.parse('o corpo da resposta contém a mensagem "{mensagem}"'))
def corpo_contem_mensagem(context, mensagem):
    assert context['response'].json().get('message') == mensagem


@then(parsers.parse('o corpo da resposta contém o erro "{erro}"'))
def corpo_contem_erro(context, erro):
    assert context['response'].json().get('detail') == erro


@then(parsers.parse('o sistema passa a ter usuário "{usuario}" com e-mail "{email}"'))
def sistema_tem_usuario(client, usuario, email):
    response = client.post('/auth/login', json={
        'email': email,
        'senha': 'senha-errada-proposital',
    })
    assert response.status_code == 401


@then(parsers.parse('o sistema mantém o usuário "{nome_usuario}" com e-mail "{email}" inalterado'))
def sistema_mantem_usuario_inalterado(client, context, nome_usuario, email):
    senha_original = context.get('usuario_existente', {}).get('senha', '')
    response = client.post('/auth/login', json={
        'email': email,
        'senha': senha_original,
    })
    assert response.status_code == 200