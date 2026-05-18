Feature: Confirmação de mensagens
    as a usuário do aplicativo de chat
    I want to visualizar o status de envio das minhas mensagens
    so that eu possa saber se a mensagem foi enviada, entregue ou lida

Scenario: Mensagem enviada com sucesso
    Given que o usuário "Ana" está autenticado no sistema
    And está na conversa com "João"
    When ela envia a mensagem "Olá, João!"
    Then o sistema deve exibir um check na mensagem
    And a mensagem deve aparecer como enviada com sucesso

Scenario: Mensagem entregue ao destinatário
    Given que o usuário "Ana" enviou uma mensagem para "João"
    And "João" está conectado à internet
    When a mensagem chega ao dispositivo de "João"
    Then o sistema deve exibir dois checks na mensagem
    And a mensagem deve aparecer como entregue

Scenario: Mensagem lida pelo destinatário
    Given que o usuário "Ana" enviou uma mensagem para "João"
    And a mensagem já foi entregue ao destinatário
    When "João" abre a conversa e visualiza a mensagem
    Then o sistema deve destacar os dois checks da mensagem
    And a mensagem deve aparecer como lida

Scenario: Falha ao enviar mensagem sem internet
    Given que o usuário "Ana" está na conversa com "João"
    And está sem conexão com a internet
    When ela tenta enviar a mensagem "Olá, João!"
    Then o sistema não deve exibir check de mensagem enviada
    And deve notificar o usuário de que o envio falhou por falta de internet


