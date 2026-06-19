Feature: Exclusão de Mensagens - Interface

Scenario: Excluir mensagem própria
  Given estou autenticado no chat
  And existe uma mensagem enviada por mim
  When clico em excluir
  Then a mensagem deve ser removida da conversa

Scenario: Tentar excluir mensagem de outro usuário
  Given estou autenticado no chat
  And existe uma mensagem enviada por outro usuário
  When tento excluir essa mensagem
  Then o sistema deve impedir a exclusão
  And a mensagem deve permanecer na conversa

Scenario: Atualização da conversa após exclusão
  Given estou autenticado no chat
  And excluí uma mensagem
  When a conversa é atualizada
  Then a mensagem não deve aparecer na conversa