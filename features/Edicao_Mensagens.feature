Feature: Edição de Mensagens
  As a usuário do aplicativo de chat
  I want to editar mensagens enviadas
  So that eu possa corrigir ou atualizar o conteúdo das mensagens
  

  Scenario: Edição de mensagem própria
    Given que estou na conversa com "João"
    And existe uma mensagem enviada por mim
    When edito a mensagem para "Mensagem Editada"
    Then a mensagem deve ser atualizada na conversa 
    And deve aparecer como editada

  Scenario: Tentativa de editar mensagem de outro usuário
    Given que estou na conversa com "João"
    And existe uma mensagem enviada por "João"
    When tento editar essa mensagem 
    Then o sistema deve impedir a edição
    And a mensagem deve permanecer sem alteração 