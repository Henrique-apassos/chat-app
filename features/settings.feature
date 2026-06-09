Feature: Perfil de usuário
As a usuário do aplicativo de chat
I want to consultar, atualizar e gerenciar meus dados de perfil
So that eu possa manter minhas informações atualizadas e controlar minha conta

Scenario: Atualizar perfil com sucesso
    Given existe uma pessoa cadastrada com usuário "bruna"
    When atualizo o perfil com nome "Bruna", sobrenome "Chalegre" e biografia "Desenvolvedora mobile"
    Then o sistema deve retornar status 200

Scenario: Buscar perfil com sucesso
    Given existe uma pessoa cadastrada com usuário "bruna"
    And o perfil de "bruna" foi atualizado com nome "Bruna", sobrenome "Chalegre" e biografia "Desenvolvedora mobile"
    When busco o perfil do usuário "bruna"
    Then o sistema deve retornar status 200
    And deve retornar o usuário "bruna"

Scenario: Atualização parcial não deve apagar campos existentes
    Given existe uma pessoa cadastrada com usuário "bruna"
    And o perfil de "bruna" possui nome "Bruna", sobrenome "Chalegre", biografia "Bio antiga" e caminho da foto "/images/bruna.jpg"
    When atualizo apenas a biografia para "Bio atualizada"
    Then o sistema deve retornar status 200
    And o nome deve continuar "Bruna"
    And o sobrenome deve continuar "Chalegre"
    And a biografia deve ser "Bio atualizada"
    And o caminho da foto deve continuar "/images/bruna.jpg"

Scenario: Atualizar perfil de usuário inexistente
    Given não existe pessoa cadastrada com usuário "fantasma"
    When tento atualizar o perfil do usuário "fantasma"
    Then o sistema deve retornar status 404
    And o sistema deve exibir a mensagem "Usuário não encontrado"

Scenario: Buscar perfil de usuário inexistente
    Given não existe pessoa cadastrada com usuário "fantasma"
    When tento buscar o perfil do usuário "fantasma"
    Then o sistema deve retornar status 404
    And o sistema deve exibir a mensagem "Usuário não encontrado"

Scenario: Validar biografia com no máximo 300 caracteres
    Given existe uma pessoa cadastrada com usuário "bruna"
    When tento atualizar a biografia com mais de 300 caracteres
    Then o sistema deve retornar status 422
    And o sistema deve informar erro de validação na biografia

Scenario: Impedir atualização para email já cadastrado
    Given existe uma pessoa cadastrada com usuário "bruna" e email "bruna@email.com"
    And existe uma pessoa cadastrada com usuário "joao" e email "joao@email.com"
    When tento atualizar o email de "bruna" para "joao@email.com"
    Then o sistema deve retornar status 409
    And o sistema deve exibir a mensagem "E-mail já cadastrado"

Scenario: Impedir atualização para telefone já cadastrado
    Given existe uma pessoa cadastrada com usuário "bruna" e telefone "81999999999"
    And existe uma pessoa cadastrada com usuário "joao" e telefone "81888888888"
    When tento atualizar o telefone de "bruna" para "81888888888"
    Then o sistema deve retornar status 409
    And o sistema deve exibir a mensagem "Telefone já cadastrado"

Scenario: Trocar nome de usuário com sucesso
    Given existe uma pessoa cadastrada com usuário "bruna"
    When atualizo o nome de usuário de "bruna" para "brunaveiga"
    Then o sistema deve retornar status 200
    And ao buscar o perfil do usuário "brunaveiga" o sistema deve retornar status 200

Scenario: Impedir troca para nome de usuário já cadastrado
    Given existe uma pessoa cadastrada com usuário "bruna"
    And existe uma pessoa cadastrada com usuário "joao"
    When tento atualizar o nome de usuário de "bruna" para "joao"
    Then o sistema deve retornar status 409
    And o sistema deve exibir a mensagem "Nome de usuário já cadastrado"

Scenario: Excluir conta com sucesso
    Given existe uma pessoa cadastrada com usuário "bruna" e senha "123456"
    When excluo a conta do usuário "bruna" informando a senha correta "123456"
    Then o sistema deve retornar status 200
    And ao buscar o perfil do usuário "bruna" o sistema deve retornar status 404

Scenario: Impedir exclusão de conta com senha incorreta
    Given existe uma pessoa cadastrada com usuário "bruna" e senha "123456"
    When tento excluir a conta do usuário "bruna" informando a senha incorreta "senhaerrada"
    Then o sistema deve retornar status 401
    And ao buscar o perfil do usuário "bruna" o sistema deve retornar status 200

Scenario: Impedir exclusão de conta inexistente
    Given não existe pessoa cadastrada com usuário "fantasma"
    When tento excluir a conta do usuário "fantasma" informando a senha "123456"
    Then o sistema deve retornar status 404
    And o sistema deve exibir a mensagem "Usuário não encontrado"