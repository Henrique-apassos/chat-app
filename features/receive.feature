feature receber mensagem

Scenario: Recebimento de mensagem com sucesso
    Given Estou em uma conversa com "João"
    When "João" envia uma mensagem "Bom dia"
    Then Observo a mensagem "Bom dia" no histórico
    And A mensagem é sinalizada com o status "Recebida"
