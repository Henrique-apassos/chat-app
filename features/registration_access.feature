Feature: Cadastro de Usuários
  As a visitante do sistema
  I want to criar uma nova conta
  So that eu possa acessar as funcionalidades do chat com segurança

  Scenario: Cadastro de novo usuário com sucesso
    Given estou na tela de cadastro
    And o sistema não possui usuário com e-mail "joao@email.com"
    When insiro e-mail "joao@email.com"
    And insiro telefone "(88) 988888888"
    And insiro nome de usuário "joaosilva"
    And insiro senha "Segura@123"
    And clico no botão "Cadastre-se"
    Then o sistema exibe mensagem "Cadastro realizado com sucesso"
    And me redireciona para tela de login
    And o sistema passa a ter usuário "joaosilva" com e-mail "joao@email.com"

  Scenario: Cadastro com e-mail já existente
    Given estou na tela de "Cadastro de Usuário"
    And o sistema já possui usuário com e-mail "existente@email.com", nome "UsuarioExistente" e senha "Senha@123"
    And o sistema NÃO possui usuário com e-mail "novo@email.com"
    When eu insiro e-mail "existente@email.com"
    And eu insiro nome de usuário "NovoUsuario"
    And eu insiro senha "NovaSenha@123"
    And eu clico no botão "Cadastre-se"
    Then o sistema exibe mensagem de alerta "E-mail já cadastrado"
    And eu continuo na tela "Cadastro de Usuário"
    And o sistema mantém o usuário "UsuarioExistente" com e-mail "existente@email.com" inalterado

    Scenario: Cadastro com senha menor que 6 caracteres
    Given estou na tela de cadastro
    And o sistema não possui usuário com e-mail "joao@email.com"
    When insiro e-mail "joao@email.com"
    And insiro telefone "(88) 988888888"
    And insiro nome de usuário "joaosilva"
    And insiro senha "abc"
    And clico no botão "Cadastre-se"
    Then o sistema rejeita o cadastro com erro de validação

    Scenario: Cadastro com nome de usuário já existente
    Given estou na tela de cadastro
    And o sistema já possui usuário com e-mail "existente@email.com", nome "UsuarioExistente" e senha "Senha@123"
    When eu insiro e-mail "novo@email.com"
    And eu insiro nome de usuário "UsuarioExistente"
    And eu insiro senha "Segura@123"
    And eu clico no botão "Cadastre-se"
    Then o sistema exibe mensagem de alerta "Nome de usuário já cadastrado"

  Scenario: Cadastro com senha de exatamente 6 caracteres
    Given estou na tela de cadastro
    And o sistema não possui usuário com e-mail "joao@email.com"
    When insiro e-mail "joao@email.com"
    And insiro telefone "(88) 988888888"
    And insiro nome de usuário "joaosilva"
    And insiro senha "Seis12"
    And clico no botão "Cadastre-se"
    Then o sistema exibe mensagem "Cadastro realizado com sucesso"