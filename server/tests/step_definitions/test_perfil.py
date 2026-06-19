from pytest_bdd import scenario, given, when, then, parsers


@scenario('settings.feature', 'Atualizar perfil com sucesso')
def test_atualizar_perfil_com_sucesso():
    pass

@scenario('settings.feature', 'Buscar perfil com sucesso')
def test_buscar_perfil_com_sucesso():
    pass

@given(parsers.parse('existe uma pessoa cadastrada com usuário "{usuario}"'))
def existe_pessoa_cadastrada(client, context, usuario):
    response = client.post(
        '/auth/register',
        json={
            'usuario': usuario,
            'email': f'{usuario}@email.com',
            'telefone': f'81999{abs(hash(usuario)) % 100000:05d}',
            'senha': '123456',
        }
    )

    assert response.status_code == 201

    context['usuario'] = usuario

@when(
    parsers.parse(
        'atualizo o perfil com nome "{nome}", sobrenome "{sobrenome}" e biografia "{biografia}"'
    )
)
def atualizo_perfil(client, context, nome, sobrenome, biografia):
    response = client.put(
        '/user/profile',
        json={
            'usuario': context['usuario'],
            'nome': nome,
            'sobrenome': sobrenome,
            'biografia': biografia,
        }
    )

    context['response'] = response

@then(parsers.parse('o sistema deve retornar status {status:d}'))
def sistema_retorna_status(context, status):
    assert context['response'].status_code == status

@given(
    parsers.parse(
        'o perfil de "{usuario}" foi atualizado com nome "{nome}", sobrenome "{sobrenome}" e biografia "{biografia}"'
    )
)
def perfil_atualizado(client, context, usuario, nome, sobrenome, biografia):
    response = client.put(
        '/user/profile',
        json={
            'usuario': usuario,
            'nome': nome,
            'sobrenome': sobrenome,
            'biografia': biografia,
        }
    )

    assert response.status_code == 200

@when(parsers.parse('busco o perfil do usuário "{usuario}"'))
def busco_perfil(client, context, usuario):
    response = client.get(f'/user/profile/{usuario}')

    context['response'] = response

@then(parsers.parse('deve retornar o usuário "{usuario}"'))
def retorna_usuario(context, usuario):
    assert context['response'].json()['usuario'] == usuario


@then(parsers.parse('deve retornar o nome "{nome}"'))
def retorna_nome(context, nome):
    assert context['response'].json()['nome'] == nome


@then(parsers.parse('deve retornar o sobrenome "{sobrenome}"'))
def retorna_sobrenome(context, sobrenome):
    assert context['response'].json()['sobrenome'] == sobrenome


@then(parsers.parse('deve retornar a biografia "{biografia}"'))
def retorna_biografia(context, biografia):
    assert context['response'].json()['biografia'] == biografia



@scenario('settings.feature', 'Atualização parcial não deve apagar campos existentes')
def test_atualizacao_parcial_nao_deve_apagar_campos():
    pass

@given(
    parsers.parse(
        'o perfil de "{usuario}" possui nome "{nome}", sobrenome "{sobrenome}", biografia "{biografia}" e caminho da foto "{caminho_foto}"'
    )
)
def perfil_possui_dados(client, context, usuario, nome, sobrenome, biografia, caminho_foto):
    response = client.put(
        '/user/profile',
        json={
            'usuario': usuario,
            'nome': nome,
            'sobrenome': sobrenome,
            'biografia': biografia,
            'caminho_foto': caminho_foto,
        }
    )

    assert response.status_code == 200


@when(parsers.parse('atualizo apenas a biografia para "{biografia}"'))
def atualizo_apenas_biografia(client, context, biografia):
    usuario = context['usuario']

    response = client.put(
        '/user/profile',
        json={
            'usuario': usuario,
            'biografia': biografia,
        }
    )

    context['response'] = response

    response_busca = client.get(f'/user/profile/{usuario}')
    context['perfil'] = response_busca.json()


@then(parsers.parse('o nome deve continuar "{nome}"'))
def nome_deve_continuar(context, nome):
    assert context['perfil']['nome'] == nome


@then(parsers.parse('o sobrenome deve continuar "{sobrenome}"'))
def sobrenome_deve_continuar(context, sobrenome):
    assert context['perfil']['sobrenome'] == sobrenome


@then(parsers.parse('a biografia deve ser "{biografia}"'))
def biografia_deve_ser(context, biografia):
    assert context['perfil']['biografia'] == biografia


@then(parsers.parse('o caminho da foto deve continuar "{caminho_foto}"'))
def caminho_foto_deve_continuar(context, caminho_foto):
    assert context['perfil']['caminho_foto'] == caminho_foto



@scenario('settings.feature', 'Atualizar perfil de usuário inexistente')
def test_atualizar_perfil_usuario_inexistente():
    pass


@scenario('settings.feature', 'Buscar perfil de usuário inexistente')
def test_buscar_perfil_usuario_inexistente():
    pass

@given(parsers.parse('não existe pessoa cadastrada com usuário "{usuario}"'))
def nao_existe_pessoa_cadastrada(context, usuario):
    context['usuario'] = usuario


@when(parsers.parse('tento atualizar o perfil do usuário "{usuario}"'))
def tento_atualizar_perfil_usuario(client, context, usuario):
    response = client.put(
        '/user/profile',
        json={
            'usuario': usuario,
            'nome': 'Fantasma',
        }
    )

    context['response'] = response


@when(parsers.parse('tento buscar o perfil do usuário "{usuario}"'))
def tento_buscar_perfil_usuario(client, context, usuario):
    response = client.get(f'/user/profile/{usuario}')

    context['response'] = response

@then(parsers.parse('o sistema deve exibir a mensagem "{mensagem}"'))
def sistema_exibe_mensagem(context, mensagem):
    body = context['response'].json()
    assert body.get('message') == mensagem or body.get('detail') == mensagem


@scenario('settings.feature', 'Validar biografia com no máximo 300 caracteres')
def test_validar_biografia_com_no_maximo_300_caracteres():
    pass

@when('tento atualizar a biografia com mais de 300 caracteres')
def tento_atualizar_biografia_grande(client, context):
    usuario = context['usuario']
    bio_grande = 'a' * 301

    response = client.put(
        '/user/profile',
        json={
            'usuario': usuario,
            'biografia': bio_grande,
        }
    )

    context['response'] = response


@then('o sistema deve informar erro de validação na biografia')
def sistema_informa_erro_validacao_biografia(context):
    body = context['response'].json()

    assert 'detail' in body
    assert 'biografia' in str(body['detail'])


@scenario('settings.feature', 'Impedir atualização para email já cadastrado')
def test_impedir_atualizacao_para_email_ja_cadastrado():
    pass


@given(parsers.parse('existe uma pessoa cadastrada com usuário "{usuario}" e email "{email}"'))
def existe_pessoa_com_email(client, usuario, email):
    response = client.post(
        '/auth/register',
        json={
            'usuario': usuario,
            'email': email,
            'telefone': f'81999{len(usuario)}9999',
            'senha': '123456',
        }
    )

    assert response.status_code == 201


@when(parsers.parse('tento atualizar o email de "{usuario}" para "{email}"'))
def tento_atualizar_email(client, context, usuario, email):
    response = client.put(
        '/user/profile',
        json={
            'usuario': usuario,
            'email': email,
        }
    )

    context['response'] = response


@scenario('settings.feature', 'Impedir atualização para telefone já cadastrado')
def test_impedir_atualizacao_para_telefone_ja_cadastrado():
    pass


@given(parsers.parse('existe uma pessoa cadastrada com usuário "{usuario}" e telefone "{telefone}"'))
def existe_pessoa_com_telefone(client, usuario, telefone):
    response = client.post(
        '/auth/register',
        json={
            'usuario': usuario,
            'email': f'{usuario}@email.com',
            'telefone': telefone,
            'senha': '123456',
        }
    )

    assert response.status_code == 201


@when(parsers.parse('tento atualizar o telefone de "{usuario}" para "{telefone}"'))
def tento_atualizar_telefone(client, context, usuario, telefone):
    response = client.put(
        '/user/profile',
        json={
            'usuario': usuario,
            'telefone': telefone,
        }
    )

    context['response'] = response


@scenario('settings.feature', 'Trocar nome de usuário com sucesso')
def test_trocar_nome_de_usuario_com_sucesso():
    pass


@when(parsers.parse('atualizo o nome de usuário de "{usuario}" para "{novo_usuario}"'))
def atualizo_nome_usuario(client, context, usuario, novo_usuario):
    response = client.put(
        '/user/profile',
        json={
            'usuario': usuario,
            'novo_usuario': novo_usuario,
        }
    )

    context['response'] = response
    context['novo_usuario'] = novo_usuario


@then(parsers.parse('ao buscar o perfil do usuário "{usuario}" o sistema deve retornar status {status:d}'))
def buscar_perfil_deve_retornar_status(client, usuario, status):
    response = client.get(f'/user/profile/{usuario}')

    assert response.status_code == status


@scenario('settings.feature', 'Impedir troca para nome de usuário já cadastrado')
def test_impedir_troca_para_nome_usuario_ja_cadastrado():
    pass


@scenario('settings.feature', 'Excluir conta com sucesso')
def test_excluir_conta_com_sucesso():
    pass


@scenario('settings.feature', 'Impedir exclusão de conta com senha incorreta')
def test_impedir_exclusao_com_senha_incorreta():
    pass


@scenario('settings.feature', 'Impedir exclusão de conta inexistente')
def test_impedir_exclusao_conta_inexistente():
    pass


@when(parsers.parse(
    'tento atualizar o nome de usuário de "{usuario}" para "{novo_usuario}"'
))
def tento_atualizar_nome_usuario(client, context, usuario, novo_usuario):
    response = client.put(
        '/user/profile',
        json={
            'usuario': usuario,
            'novo_usuario': novo_usuario,
        }
    )

    context['response'] = response


@given(parsers.parse(
    'existe uma pessoa cadastrada com usuário "{usuario}" e senha "{senha}"'
))
def existe_pessoa_com_senha(client, usuario, senha):
    response = client.post(
        '/auth/register',
        json={
            'usuario': usuario,
            'email': f'{usuario}@email.com',
            'telefone': f'81999{len(usuario)}7777',
            'senha': senha,
        }
    )

    assert response.status_code == 201


@when(parsers.parse(
    'excluo a conta do usuário "{usuario}" informando a senha correta "{senha}"'
))
def excluo_conta(client, context, usuario, senha):
    response = client.request(
    'DELETE',
    f'/user/profile/{usuario}',
    json={
        'senha': senha
    }
)

    context['response'] = response


@when(parsers.parse(
    'tento excluir a conta do usuário "{usuario}" informando a senha incorreta "{senha}"'
))
def excluo_conta_senha_errada(client, context, usuario, senha):
    response = client.request(
    'DELETE',
    f'/user/profile/{usuario}',
    json={
        'senha': senha
    }
)

    context['response'] = response


@when(parsers.parse(
    'tento excluir a conta do usuário "{usuario}" informando a senha "{senha}"'
))
def excluo_conta_inexistente(client, context, usuario, senha):
    response = client.request(
    'DELETE',
    f'/user/profile/{usuario}',
    json={
        'senha': senha
    }
)

    context['response'] = response