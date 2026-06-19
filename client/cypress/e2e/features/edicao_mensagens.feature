Feature: Edição de Mensagens - Interface

Scenario: Editar mensagem própria
  Given estou autenticado no chat
  And existe uma mensagem enviada por mim
  When clico em editar
  And altero o texto para "Mensagem Editada"
  Then devo visualizar a mensagem editada

Scenario: Tentar editar mensagem de outro usuário
  Given estou autenticado no chat
  And existe uma mensagem enviada por outro usuário
  When tento editar essa mensagem
  Then o sistema deve impedir a edição
  And a mensagem deve permanecer sem alteração