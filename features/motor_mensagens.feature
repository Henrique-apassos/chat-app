Feature: Motor de Mensagens
  As a serviço de mensagens
  I want to processar, persistir e rotear mensagens corretamente
  So that garantir a integridade e entrega das mensagens entre usuários

  Scenario: Persistência de mensagem enviada com sucesso
    Given que o usuário "joao" está conectado via WebSocket
    When "joao" envia a mensagem "Olá, Maria"
    Then a mensagem é persistida no banco com o texto "Olá, Maria"
    And a mensagem é registrada com o status "ENVIADO"
    And o campo "usuario" da mensagem aponta para "joao"

  Scenario: Roteamento de mensagem para destinatário conectado
    Given que o usuário "joao" está conectado via WebSocket
    And o usuário "maria" está conectado via WebSocket
    When "joao" envia a mensagem "Bom dia, Maria"
    Then "maria" recebe a mensagem no WebSocket
    And "joao" não recebe a própria mensagem de volta

  Scenario: Persistência de mensagem recebida com status correto
    Given que o usuário "joao" está conectado via WebSocket
    And o usuário "maria" está conectado via WebSocket
    When "joao" envia a mensagem "Bom dia"
    Then a mensagem é persistida no banco com o status "ENVIADO"
    And o campo "usuario" da mensagem aponta para "joao"

  Scenario: Rejeição de mensagem com conteúdo vazio
    Given que o usuário "joao" está conectado via WebSocket
    When "joao" tenta enviar uma mensagem contendo apenas espaços ou quebras de linha
    Then nenhuma mensagem é persistida no banco
    And nenhuma mensagem é roteada para outros usuários conectados
