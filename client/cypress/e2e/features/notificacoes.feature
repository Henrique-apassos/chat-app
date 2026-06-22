Feature: Notificacoes e Alertas
  Scenario: Badge exibido ao receber mensagem nao lida
    Given que iniciei sessao como "ana"
    And "joao" envia a mensagem "Ola Ana!" para "ana"
    When atualizo a tela de chat
    Then vejo o badge "1" ao lado de "joao" na lista de contatos

  Scenario: Badge zerado ao abrir conversa
    Given que iniciei sessao como "ana"
    And "joao" envia 3 mensagens nao lidas para "ana"
    When clico no contato "joao" na barra lateral
    Then o badge ao lado de "joao" e removido

  Scenario: Banner de notificacao exibido ao receber mensagem
    Given que iniciei sessao como "ana"
    When atualizo a tela de chat
    And "joao" envia a mensagem "E ai, tudo bem?" para "ana"
    Then vejo o banner de notificacao com "joao" e "E ai, tudo bem?"
    And o banner desaparece apos 4 segundos