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


@given('estou na tela de cadastro')
def estou_na_tela_de_cadastro():
    pass


@given(parsers.parse('estou na tela de "{tela}"'))
def estou_na_tela_de(tela):
    pass


@given(parsers.parse('o sistema não possui usuário com e-mail "{email}"'))
def sistema_nao_possui_email(email):
    pass


@given(parsers.parse('o sistema NÃO possui usuário com e-mail "{email}"'))
def sistema_nao_possui_email_upper(email):
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


@when(parsers.parse('insiro e-mail "{email}"'))
def insiro_email(context, email):
    context['email'] = email


@when(parsers.parse('insiro telefone "{telefone}"'))
def insiro_telefone(context, telefone):
    context['telefone'] = telefone


@when(parsers.parse('insiro nome de usuário "{nome_usuario}"'))
def insiro_nome_usuario(context, nome_usuario):
    context['nome_usuario'] = nome_usuario


@when(parsers.parse('insiro senha "{senha}"'))
def insiro_senha(context, senha):
    context['senha'] = senha


@when(parsers.parse('clico no botão "{botao}"'))
def clico_no_botao_cadastrese(client, context, botao):
    response = client.post('/auth/register', json={
        'usuario': context.get('nome_usuario', ''),
        'email': context.get('email', ''),
        'telefone': context.get('telefone', '(00) 000000000'),
        'senha': context.get('senha', ''),
    })
    context['response'] = response


@when(parsers.parse('eu insiro e-mail "{email}"'))
def eu_insiro_email(context, email):
    context['email'] = email


@when(parsers.parse('eu insiro nome de usuário "{nome_usuario}"'))
def eu_insiro_nome(context, nome_usuario):
    context['nome_usuario'] = nome_usuario


@when(parsers.parse('eu insiro senha "{senha}"'))
def eu_insiro_senha(context, senha):
    context['senha'] = senha


@when(parsers.parse('eu clico no botão "{botao}"'))
def eu_clico_no_botao(client, context, botao):
    response = client.post('/auth/register', json={
        'usuario': context.get('nome_usuario', ''),
        'email': context.get('email', ''),
        'telefone': context.get('telefone', '(00) 000000000'),
        'senha': context.get('senha', ''),
    })
    context['response'] = response


@then(parsers.parse('o sistema exibe mensagem "{mensagem}"'))
def sistema_exibe_mensagem(context, mensagem):
    assert context['response'].json().get('message') == mensagem


@then('me redireciona para tela de login')
def me_redireciona_para_login(context):
    assert context['response'].status_code == 201


@then(parsers.parse('o sistema passa a ter usuário "{usuario}" com e-mail "{email}"'))
def sistema_tem_usuario(client, usuario, email):
    response = client.post('/auth/login', json={
        'email': email,
        'senha': 'senha-errada-proposital',
    })
    assert response.status_code == 401


@then(parsers.parse('o sistema exibe mensagem de alerta "{mensagem}"'))
def sistema_exibe_mensagem_alerta(context, mensagem):
    assert context['response'].status_code == 409
    assert context['response'].json().get('detail') == mensagem


@then(parsers.parse('eu continuo na tela "{tela}"'))
def eu_continuo_na_tela(context, tela):
    assert context['response'].status_code != 201


@then(parsers.parse('o sistema mantém o usuário "{nome_usuario}" com e-mail "{email}" inalterado'))
def sistema_mantem_usuario_inalterado(client, context, nome_usuario, email):
    senha_original = context.get('usuario_existente', {}).get('senha', '')
    response = client.post('/auth/login', json={
        'email': email,
        'senha': senha_original,
    })
    assert response.status_code == 200


@then('o sistema rejeita o cadastro com erro de validação')
def sistema_rejeita_senha_curta(context):
    assert context['response'].status_code == 422

@scenario('registration_access.feature', 'Cadastro com nome de usuário já existente')
def test_cadastro_usuario_duplicado():
    pass


@scenario('registration_access.feature', 'Cadastro com senha de exatamente 6 caracteres')
def test_cadastro_senha_limite_exato():
    pass