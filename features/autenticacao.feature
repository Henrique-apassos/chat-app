Feature: Autenticação de Usuários
  As a usuário registrado do sistema
  I want to realizar login com minhas credenciais
  So that eu possa acessar as funcionalidades do chat com segurança

  Scenario: Login com credenciais válidas
    Given o usuário "joao@email.com" com senha "Segura@123" está registrado no sistema
    And o usuário "joao@email.com" possui os contatos "maria@email.com" e "pedro@email.com"
    And estou na tela de "Login" do sistema
    And não estou logado no sistema
    When informo e-mail "joao@email.com" e senha "Segura@123"
    And clico no botão "Entrar"
    Then o sistema exibe mensagem de boas-vindas "Bem-vindo, joao@email.com"
    And eu vejo o contato "maria@email.com" na lista
    And eu vejo o contato "pedro@email.com" na lista
    And o sistema me mantém logado por um tempo determinado

  Scenario: Login com senha incorreta
    Given o usuário "joao@email.com" com senha "Segura@123" está cadastrado
    When informo e-mail "joao@email.com" e senha "Errada456"
    And clico no botão "Entrar"
    Then o sistema deve impedir o acesso
    And exibir mensagem "Credenciais inválidas"
    And o sistema NÃO me mantém logado como "joao@email.com"
    And o usuário "joao@email.com" permanece com senha "Segura@123" inalterada

    Scenario: Login com e-mail inexistente
    Given o sistema não possui nenhum usuário cadastrado
    When informo e-mail "fantasma@email.com" e senha "qualquer123"
    And clico no botão "Entrar"
    Then o sistema deve impedir o acesso
    And exibir mensagem "Credenciais inválidas"