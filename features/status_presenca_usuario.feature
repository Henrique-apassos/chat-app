Feature: Status de presença do usuário
    as a usuário do aplicativo de chat
    I want to visualizar se meus contatos estão online ou quando foram vistos por último
    so that eu possa saber a disponibilidade deles no aplicativo

Scenario: Exibir usuário online
    Given que o usuário "João" está conectado ao aplicativo
    And o usuário "Ana" está na conversa com "João"
    When o sistema identifica que "João" está ativo
    Then deve exibir o status "Online" abaixo do nome de "João"
    And o status deve permanecer visível enquanto ele estiver conectado

Scenario: Exibir visto por último
    Given que o usuário "João" estava online no aplicativo
    And saiu ou ficou inativo
    When o usuário "Ana" abre a conversa com "João"
    Then o sistema deve exibir "Visto por último"
    And deve mostrar a data e o horário do último acesso de "João"

Scenario: Atualizar status após mudança de conexão
    Given que o usuário "João" está com o status "Online"
    When ele perde a conexão com a internet
    Then o sistema deve atualizar seu status após identificar a desconexão
    And deve exibir o último status conhecido até a atualização ser concluída

Scenario: Não permitir ocultar online ou visto por último
    Given que o usuário "Ana" está nas configurações do aplicativo
    When ela procura uma opção para ocultar "Online" ou "Visto por último"
    Then o sistema não precisa exibir essa configuração
    And o status de presença deve continuar sendo mostrado normalmente


