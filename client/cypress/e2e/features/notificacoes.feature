Feature: Notificações e Alertas
  Scenario: Badge exibido ao receber mensagem não lida
    Given que estou autenticado como "ana"
    And "joao" envia a mensagem "Olá Ana!" para "ana"
    When eu acesso a tela de chat
    Then vejo o badge "1" ao lado de "joao" na lista de contatos

  Scenario: Badge zerado ao abrir conversa
    Given que estou autenticado como "ana"
    And "joao" envia 3 mensagens não lidas para "ana"
    When eu abro a conversa com "joao"
    Then o badge ao lado de "joao" é removido

  Scenario: Banner de notificação exibido ao receber mensagem
    Given que estou autenticado como "ana"
    And estou na tela de chat
    When "joao" envia a mensagem "E aí, tudo bem?" para "ana"
    Then vejo o banner de notificação com "joao" e "E aí, tudo bem?"
    And o banner desaparece após 4 segundos