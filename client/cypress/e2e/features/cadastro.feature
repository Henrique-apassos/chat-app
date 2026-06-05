Feature: Cadastro de Usuários - Interface

  Scenario: Cadastro de novo usuário com sucesso
    Given estou na tela de cadastro
    When preencho o e-mail com "teste_cypress@email.com"
    And preencho o telefone com "(88) 98888-8888"
    And preencho o nome de usuário com "cypress_user"
    And preencho a senha com "Segura@123"
    And clico no botão de cadastro
    Then sou redirecionado para a tela de sucesso

  Scenario: Cadastro com senha menor que 6 caracteres
    Given estou na tela de cadastro
    When preencho o e-mail com "teste@email.com"
    And preencho o telefone com "(88) 98888-8888"
    And preencho o nome de usuário com "usuario_teste"
    And preencho a senha com "abc"
    And clico no botão de cadastro
    Then vejo a mensagem de erro "A senha deve ter no mínimo 6 caracteres"

  Scenario: Cadastro com e-mail já existente
    Given estou na tela de cadastro
    And já existe um usuário com e-mail "existente@email.com"
    When preencho o e-mail com "existente@email.com"
    And preencho o telefone com "(88) 98888-8888"
    And preencho o nome de usuário com "outro_usuario"
    And preencho a senha com "Segura@123"
    And clico no botão de cadastro
    Then vejo a mensagem de erro "E-mail já cadastrado"

  Scenario: Cadastro com e-mail inválido
    Given estou na tela de cadastro
    When preencho o e-mail com "emailinvalido"
    And preencho o telefone com "(88) 98888-8888"
    And preencho o nome de usuário com "usuario_teste"
    And preencho a senha com "Segura@123"
    And clico no botão de cadastro
    Then vejo a mensagem de erro "E-mail inválido"

  Scenario: Cadastro com telefone inválido
    Given estou na tela de cadastro
    When preencho o e-mail com "teste@email.com"
    And preencho o telefone com "123"
    And preencho o nome de usuário com "usuario_teste"
    And preencho a senha com "Segura@123"
    And clico no botão de cadastro
    Then vejo a mensagem de erro "Telefone inválido. Use o formato (88) 98888-8888"

  Scenario: Cadastro com nome de usuário muito curto
    Given estou na tela de cadastro
    When preencho o e-mail com "teste@email.com"
    And preencho o telefone com "(88) 98888-8888"
    And preencho o nome de usuário com "ab"
    And preencho a senha com "Segura@123"
    And clico no botão de cadastro
    Then vejo a mensagem de erro "Nome de usuário deve ter no mínimo 3 caracteres"

  Scenario: Navegação da tela de cadastro para login
    Given estou na tela de cadastro
    When clico no link "Entrar"
    Then sou redirecionado para a tela de boas-vindas

  Scenario: Navegação da tela de login para cadastro
    Given estou na tela de login
    When clico no link "Criar conta"
    Then sou redirecionado para a tela de cadastro