Feature: Cadastro de Usuários
  As a visitante do sistema
  I want to criar uma nova conta
  So that eu possa acessar as funcionalidades do chat com segurança

  Scenario: Cadastro de novo usuário com sucesso
    Given a rota POST /auth/register está disponível
    And o sistema não possui usuário com e-mail "joao@email.com"
    When envio uma requisição de cadastro com e-mail "joao@email.com", usuario "joaosilva", telefone "(88) 988888888" e senha "Segura@123"
    Then o sistema retorna status 201
    And o corpo da resposta contém a mensagem "Cadastro realizado com sucesso"
    And o sistema passa a ter usuário "joaosilva" com e-mail "joao@email.com"

  Scenario: Cadastro com e-mail já existente
    Given o sistema já possui usuário com e-mail "existente@email.com", nome "UsuarioExistente" e senha "Senha@123"
    When envio uma requisição de cadastro com e-mail "existente@email.com", usuario "NovoUsuario" e senha "NovaSenha@123"
    Then o sistema retorna status 409
    And o corpo da resposta contém o erro "E-mail já cadastrado"
    And o sistema mantém o usuário "UsuarioExistente" com e-mail "existente@email.com" inalterado

  Scenario: Cadastro com senha menor que 6 caracteres
    Given a rota POST /auth/register está disponível
    And o sistema não possui usuário com e-mail "joao@email.com"
    When envio uma requisição de cadastro com e-mail "joao@email.com", usuario "joaosilva", telefone "(88) 988888888" e senha "abc"
    Then o sistema retorna status 422

  Scenario: Cadastro com nome de usuário já existente
    Given o sistema já possui usuário com e-mail "existente@email.com", nome "UsuarioExistente" e senha "Senha@123"
    When envio uma requisição de cadastro com e-mail "novo@email.com", usuario "UsuarioExistente" e senha "Segura@123"
    Then o sistema retorna status 409
    And o corpo da resposta contém o erro "Nome de usuário já cadastrado"

  Scenario: Cadastro com senha de exatamente 6 caracteres
    Given a rota POST /auth/register está disponível
    And o sistema não possui usuário com e-mail "joao@email.com"
    When envio uma requisição de cadastro com e-mail "joao@email.com", usuario "joaosilva", telefone "(88) 988888888" e senha "Seis12"
    Then o sistema retorna status 201
    And o corpo da resposta contém a mensagem "Cadastro realizado com sucesso"