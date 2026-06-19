# language: pt
Funcionalidade: Lista de Conversas e Busca
  Como um usuário autenticado do aplicativo de mensagens
  Quero buscar minhas conversas e encontrar outros usuários pelo nome
  Para abrir conversas existentes ou iniciar novas

  Contexto:
    Dado que o usuário é identificado pelo token JWT (Authorization: Bearer)
    E a busca é por prefixo e ignora maiúsculas/minúsculas
    E cada conversa pode ser de uma pessoa ("usuario") ou de um grupo ("grupo")

  Cenário: Acesso sem autenticação é negado
    Dado um cliente sem token JWT
    Quando ele chama a busca de conversas
    Então o sistema responde 401 Não Autorizado
    # Garante que ninguém acesse as conversas de outro usuário (IDOR)

  Cenário: Busca vazia lista as conversas existentes, mais recentes primeiro
    Dado que "paulo" conversou com "joao" e, depois, com "paula"
    Quando "paulo" busca com o termo vazio
    Então as duas conversas são retornadas com status verdadeiro
    E a conversa com "paula" (mais recente) aparece antes da conversa com "joao"
    E cada conversa traz a última mensagem com o remetente e o texto

  Cenário: Busca por prefixo ignorando maiúsculas e minúsculas
    Dado que existem os usuários "paula" e "joao"
    Quando "paulo" busca pelo termo "PA"
    Então "paula" é retornada
    E "joao" não é retornado
    E o próprio "paulo" nunca aparece no resultado

  Cenário: Usuário sem conversa iniciada aparece como conversa vazia
    Dado que existe "carla", com quem "paulo" nunca conversou
    Quando "paulo" busca pelo termo "ca"
    Então "carla" é retornada com status falso
    E sem última mensagem

  Cenário: Conversas existentes têm prioridade sobre usuários novos
    Dado que "paulo" já conversou com "paula", mas nunca com "pamela"
    Quando "paulo" busca pelo termo "pa"
    Então "paula" (status verdadeiro) aparece antes de "pamela" (status falso)

  Cenário: Um usuário não enxerga as conversas de outro
    Dado que "paulo" e "paula" trocaram mensagens
    E que "joao" não possui nenhuma conversa
    Quando "joao" autenticado busca com o termo vazio
    Então ele recebe uma lista vazia
    # Não vê a conversa entre "paulo" e "paula" (proteção contra IDOR)

  Cenário: Grupos dos quais o usuário participa entram na lista
    Dado que "paulo" participa do grupo "Paladinos"
    Quando ele busca com o termo vazio
    Então o grupo "Paladinos" é retornado com tipo "grupo" e status verdadeiro
    E sem última mensagem, pois o envio de mensagens em grupo ainda não foi implementado
