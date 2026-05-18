Feature: Perfil e configurações
    as a usuário do aplicativo de chat
    I want to acessar e modificar minhas configurações de perfil
    so that eu possa personalizar minha experiência no aplicativo


    Scenario: Atualizar foto de perfil
        Given que o usuário "Ana" está autenticada no sistema
        And está na tela "Configurações de Perfil"
        When ela seleciona uma nova imagem válida para foto de perfil
        Then o sistema deve exibir a pré-visualização da nova foto
        And permitir a confirmação da alteração

    Scenario: Atualizar nome de usuário com nome já existente
        Given que o usuário "Ana" está autenticada no sistema
        And está na tela "Configurações de Perfil"
        And existe um usuário "João" com o nome de usuário "pessoa01"
        When "Ana" insere "pessoa01" como nome de usuário e clica em "Salvar"
        Then o sistema deve mostrar uma mensagem de erro "Nome de usuário já em uso. Por favor, escolha outro."

    Scenario: Atualizar email de usuário com email já existente
        Given que o usuário "Ana" está autenticada no sistema
        And está na tela "Configurações de Perfil"
        And existe um usuário "João" com o email "joao@example.com"
        When "Ana" insere "joao@example.com" como email e clica em "Salvar"
        Then o sistema deve mostrar uma mensagem de erro "Email já em uso. Por favor, escolha outro."

    Scenario: Atualizar telefone de usuário com telefone já existente
        Given que o usuário "Ana" está autenticada no sistema
        And está na tela "Configurações de Perfil"
        And existe um usuário "João" com o telefone "1234567890"
        When "Ana" insere "1234567890" como telefone e clica em "Salvar"
        Then o sistema deve mostrar uma mensagem de erro "Telefone já em uso. Por favor, escolha outro."

    Scenario: Atualizar bio com menos de 300 caracteres
        Given que o usuário "Ana" está autenticada no sistema
        And está na tela "Configurações de Perfil"
        When ela insere uma nova bio com menos de 300 caracteres
        And clica em "Salvar"
        Then o sistema deve exibir a nova bio atualizada

    Scenario: Atualizar bio com mais de 300 caracteres
        Given que o usuário "Ana" está autenticada no sistema
        And está na tela "Configurações de Perfil"
        When ela insere uma nova bio com mais de 300 caracteres
        And clica em "Salvar"
        Then o sistema deve mostrar uma mensagem de erro "Bio não pode exceder 300 caracteres."

    Scenario: Alternar de modo claro para modo escuro
        Given que o usuário "Ana" está autenticada no sistema
        And está na tela "Configurações"
        And o "tema" do aplicativo é "Modo Claro"
        When ela ativa a opção "Modo Escuro"
        Then o "tema" do aplicativo deve ser atualizado para "Modo Escuro"

    Scenario: Excluir conta
        Given que o usuário "Ana" está autenticada no sistema
        And está na tela "Configurações"
        When ela clica na opção "Excluir Conta"
        And digita seu nome de usuário para confirmar a exclusão
        Then o sistema exclui a conta de "Ana" e a redireciona para a tela de login