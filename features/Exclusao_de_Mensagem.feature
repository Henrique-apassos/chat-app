Feature: Exclusão de Mensagens
  As a usuário do aplicativo de chat
  I want to excluir mensagens enviadas
  So that eu possa remover mensagens 

  Scenario: Exclusão de mensagem própria
    Given que estou na conversa com "Ana"
    And existe uma mensagem enviada por mim
    When solicito a exclusão da mensagem
    Then a mensagem deve ser removida da conversa

  Scenario: Tentativa de excluir mensagem de outro usuário
    Given estou na conversa com "Ana"
    And existe uma mensagem enviada por "Ana"
    When tento excluir essa mensagem
    Then o sistema deve impedir a exclusão
    And a mensagem deve permanecer na conversa

  Scenario: Atualização da conversa após exclusão de mensagem
    Given estou na conversa com "Ana"
    And excluí uma mensagem
    And a exclusão foi autorizada
    When a conversa é aberta
    Then a mensagem não deve aparecer na conversa