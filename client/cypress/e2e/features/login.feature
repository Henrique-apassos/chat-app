Feature: Autenticação de Usuários - Interface

  Scenario: Login com credenciais inválidas
    Given estou na tela de login
    When preencho o e-mail com "inexistente@email.com"
    And preencho a senha com "Errada456"
    And clico no botão de entrar
    Then vejo a mensagem de erro "Credenciais inválidas"

  Scenario: Login com senha incorreta
    Given o usuário "joao@email.com" está cadastrado com senha "Segura@123"
    And estou na tela de login
    When preencho o e-mail com "joao@email.com"
    And preencho a senha com "SenhaErrada"
    And clico no botão de entrar
    Then vejo a mensagem de erro "Credenciais inválidas"

  Scenario: Login com credenciais válidas
    Given o usuário "joao@email.com" está cadastrado com senha "Segura@123"
    And estou na tela de login
    When preencho o e-mail com "joao@email.com"
    And preencho a senha com "Segura@123"
    And clico no botão de entrar
    Then sou redirecionado para o chat