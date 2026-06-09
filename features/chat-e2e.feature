Feature: Chat — Testes End-to-End
  As um usuário do aplicativo de mensagens
  I Want que o fluxo completo de envio e recebimento funcione de ponta a ponta
  So that garantir que a interface, o servidor e o banco de dados estão integrados corretamente

  Scenario: Troca de mensagem em tempo real entre dois usuários conectados
    Given que "joao" está autenticado e conectado via WebSocket
    And "maria" está autenticada e conectada via WebSocket
    When "joao" envia a mensagem "Oi, Maria!" pela interface
    Then a mensagem "Oi, Maria!" aparece no histórico de "joao" com o status "Enviada"
    And a mensagem "Oi, Maria!" aparece no histórico de "maria" com o remetente "joao"
    And a mensagem é persistida no banco com o status "ENVIADO" e o usuario "joao"

  Scenario: Histórico carrega mensagens do banco ao reabrir a conversa
    Given que "joao" e "maria" já trocaram as mensagens "Olá" e "Tudo bem?"
    When "joao" fecha e reabre a conversa com "maria"
    Then as mensagens "Olá" e "Tudo bem?" aparecem no histórico
    And as mensagens estão em ordem cronológica

  Scenario: Mensagem vazia não chega ao banco
    Given que "joao" está autenticado e conectado via WebSocket
    When "joao" tenta enviar uma mensagem contendo apenas espaços pela interface
    Then o botão de enviar permanece desabilitado
    And nenhum registro é criado na tabela "mensagem" para o usuario "joao"

  Scenario: Mensagem pendente é enviada ao banco após reconexão
    Given que "joao" está autenticado
    And "joao" está sem conexão com a internet
    When "joao" envia a mensagem "Mensagem offline" pela interface
    Then a mensagem aparece no histórico com o status "Aguardando conexão"
    And nenhum registro é criado na tabela "mensagem" ainda
    When a conexão de "joao" é restabelecida
    Then a mensagem é enviada automaticamente ao servidor
    And um registro é criado na tabela "mensagem" com o texto "Mensagem offline" e o status "ENVIADO"
    And o status da mensagem no histórico é atualizado para "Enviada"
