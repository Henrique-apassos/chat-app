Feature: Interface de Chat
  As an usuário do aplicativo de mensagens
  I want interagir com a interface do chat
  So that enviar e receber mensagens em tempo real

  Scenario: Envio de mensagem exibe a mensagem no histórico
    Given que estou autenticado como "joao"
    And estou na tela de conversa com "maria"
    When eu digito "Olá, Maria" no campo de texto
    And clico no botão de enviar
    Then a mensagem "Olá, Maria" aparece no histórico alinhada à direita
    And o campo de texto fica vazio

  Scenario: Mensagem enviada exibe status de enviada
    Given que estou autenticado como "joao"
    And estou na tela de conversa com "maria"
    When eu digito "Tudo bem?" no campo de texto
    And clico no botão de enviar
    Then a mensagem "Tudo bem?" aparece no histórico com o status "Enviada"

  Scenario: Recebimento de mensagem exibe a mensagem no histórico
    Given que estou autenticado como "joao"
    And estou na tela de conversa com "maria"
    When "maria" envia a mensagem "Oi, João!"
    Then a mensagem "Oi, João!" aparece no histórico alinhada à esquerda
    And a mensagem exibe o nome "maria" como remetente

  Scenario: Botão de enviar desabilitado com campo vazio
    Given que estou autenticado como "joao"
    And estou na tela de conversa com "maria"
    When o campo de texto está vazio
    Then o botão de enviar está desabilitado

  Scenario: Botão de enviar desabilitado com apenas espaços
    Given que estou autenticado como "joao"
    And estou na tela de conversa com "maria"
    When eu digito apenas espaços no campo de texto
    Then o botão de enviar está desabilitado

  Scenario: Botão de enviar habilitado com texto válido
    Given que estou autenticado como "joao"
    And estou na tela de conversa com "maria"
    When eu digito "Olá" no campo de texto
    Then o botão de enviar está habilitado

  Scenario: Envio de mensagem sem conexão exibe status pendente
    Given que estou autenticado como "joao"
    And estou na tela de conversa com "maria"
    And estou sem conexão com a internet
    When eu digito "Bom dia" no campo de texto
    And clico no botão de enviar
    Then a mensagem "Bom dia" aparece no histórico com o status "Aguardando conexão"

  Scenario: Reconexão envia mensagem pendente e atualiza status
    Given que estou autenticado como "joao"
    And estou na tela de conversa com "maria"
    And estou sem conexão com a internet
    And enviei a mensagem "Bom dia" que ficou com o status "Aguardando conexão"
    When a conexão com a internet é restabelecida
    Then a mensagem "Bom dia" é enviada automaticamente
    And o status da mensagem é atualizado para "Enviada"

  Scenario: Histórico exibe mensagens anteriores ao abrir a conversa
    Given que "joao" e "maria" já trocaram mensagens anteriormente
    When eu abro a conversa com "maria"
    Then as mensagens anteriores aparecem no histórico em ordem cronológica
