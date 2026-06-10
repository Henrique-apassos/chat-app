Feature: Autenticação de Usuários
  As a usuário registrado do sistema
  I want to realizar login com minhas credenciais
  So that eu possa acessar as funcionalidades do chat com segurança

  Scenario: Login com credenciais válidas
    Given o usuário "joao@email.com" com senha "Segura@123" está registrado no sistema
    And o usuário "joao@email.com" possui os contatos "maria@email.com" e "pedro@email.com"
    When envio uma requisição de login com e-mail "joao@email.com" e senha "Segura@123"
    Then o sistema retorna status 200
    And o corpo da resposta contém um token de acesso
    And o corpo da resposta contém expires_in positivo
    And o corpo da resposta contém a mensagem de boas-vindas "Bem-vindo, joao@email.com"
    And o corpo da resposta contém o contato "maria@email.com" na lista
    And o corpo da resposta contém o contato "pedro@email.com" na lista

  Scenario: Login com senha incorreta
    Given o usuário "joao@email.com" com senha "Segura@123" está cadastrado
    When envio uma requisição de login com e-mail "joao@email.com" e senha "Errada456"
    Then o sistema retorna status 401
    And o corpo da resposta contém o erro "Credenciais inválidas"
    And o corpo da resposta não contém token de acesso
    And o usuário "joao@email.com" ainda consegue autenticar com a senha "Segura@123"

  Scenario: Login com e-mail inexistente
    Given o sistema não possui nenhum usuário cadastrado
    When envio uma requisição de login com e-mail "fantasma@email.com" e senha "qualquer123"
    Then o sistema retorna status 401
    And o corpo da resposta contém o erro "Credenciais inválidas"