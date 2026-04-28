feature: Enviar Mensagem

Scenario: Envio de mensagem de texto com sucesso
    Given Eu estou na conversa com "João"
    When Eu mando a mensagem "Olá, João"
    Then A mensagem vai para uma fila no servidor
    And A mensagem aparece na minha lista de mensagem

Scenario: Envio de mensagem de texto offline
    Given Estou na conversa com "João"
    And Estou sem conexão a internet
    When Eu envio a mensagem "Bom dia, João"
    Then A mensagem entra em uma fila de espera interna
    And A mensagem deve aparecer no chat com o status "Aguardando conexão"