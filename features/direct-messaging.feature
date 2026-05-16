feature: Troca de Mensagens

Scenario: Recebimento de mensagem com sucesso
    Given Estou em uma conversa com "João"
    When "João" envia uma mensagem "Bom dia"
    Then Observo a mensagem "Bom dia" no histórico
    And A mensagem é sinalizada com o status "Recebida"

Scenario: Envio de mensagem de texto com sucesso
    Given Eu estou na conversa com "João"
    When Eu mando a mensagem "Olá, João"
    Then A mensagem vai para uma fila no servidor
    And A mensagem aparece no histórico da conversa
    And Deve ser sinalizada com o status "Enviada"

Scenario: Envio de mensagem de texto offline
    Given Estou na conversa com "João"
    And Estou sem conexão a internet
    When Eu envio a mensagem "Bom dia, João"
    Then A mensagem entra em uma fila de espera interna
    And A mensagem deve aparecer no chat com o status "Aguardando conexão"

Scenario: Envio de mensagem vazia
    Given Eu estou na conversa com "Maria"
    When Eu digito a mensagem contendo apenas espaços ou '\n'
    And tento enviar a mensagem
    Then Eu vejo que a mensagem não é adicionada no histórico da tela
    And observo que nenhum evento de envio foi disparado para o servidor
