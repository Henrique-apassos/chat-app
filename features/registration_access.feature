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
    And o sistema NÃO possui usuário com nome "NovoUsuario"
    And o sistema NÃO possui usuário com e-mail "existente@email.com" além do já existente
    And o sistema mantém o usuário "UsuarioExistente" com e-mail "existente@email.com" inalterado


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
    Then o sistema exibe mensagem "Bem-vindo, joao@email.com"
    And o sistema me redireciona para tela "Lista de Contatos"
    And eu vejo o contato "maria@email.com" na lista
    And eu vejo o contato "pedro@email.com" na lista
    And o sistema me mantém logado como "joao@email.com" por um tempo determinado

Scenario: Login com senha incorreta
    Given o usuário "joao@email.com" com senha "Segura@123" está cadastrado
    When informo e-mail "joao@email.com" e senha "Errada456"
    Then o sistema deve impedir o acesso
    And exibir mensagem "Credenciais inválidas"
    And o campo de senha é limpo ou permanece vazio
    And o sistema NÃO me mantém logado como "joao@email.com"
    And o usuário "joao@email.com" permanece com senha "Segura@123" inalterada

Scenario: [EXPERIMENTAL] Recuperação de conta via SMS
    Given que esqueci minha senha de acesso
    When eu solicito a recuperação via número de celular
    Then o sistema deve enviar um código de verificação por SMS
    And permitir a criação de uma nova senha temporária

Scenario: [EXPERIMENTAL] Validação de segurança por e-mail
    Given que o sistema detectou um acesso de um novo dispositivo
    When eu confirmo minha identidade através do link enviado por e-mail
    Then o sistema deve autorizar o novo dispositivo para uso

Scenario: [FINAL] Validação de segurança por e-mail com expiração
    Given que o sistema detectou um acesso de um novo dispositivo
    When eu confirmo minha identidade através do link enviado por e-mail em até 10 minutos
    Then o sistema deve autorizar o novo dispositivo
    But o link deve expirar após esse período por questões de segurança
