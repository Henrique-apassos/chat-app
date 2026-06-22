Feature: Notificações e Alertas
  As a usuário do aplicativo de chat web
  I want to receber avisos visuais e sonoros de novas mensagens
  So that eu saiba que recebi algo mesmo navegando em outras abas ou dispositivos

  Scenario: Banner de notificação exibido em outra tela
    Given que o usuário "Ana" está na tela "Configurações de Perfil"
    And possui conexão ativa com o servidor
    When o usuário "Filipe" envia a mensagem "E aí, tudo bem?" para "Ana"
    Then o sistema exibe um banner responsivo no topo da viewport com "Filipe" e "E aí, tudo bem?"
    And o banner desaparece após 4 segundos sem bloquear a navegação

  Scenario: Badge zerado ao abrir conversa
    Given que o usuário "Ana" está na tela "Lista de Conversas"
    And o badge ao lado de "João" exibe "3" mensagens não lidas
    When "Ana" abre a conversa com "João"
    Then o badge ao lado de "João" é removido
    And todas as mensagens de "João" ficam marcadas como lidas
    And o indicador de não lidas na aba do navegador é removido

  Scenario: Feedback de falha de conexão ao tentar atualizar notificações
    Given que o usuário "Ana" está na tela "Lista de Conversas"
    And o dispositivo está offline ou sem conexão com o servidor
    When "Ana" tenta atualizar a lista de notificações
    Then o sistema exibe o banner de erro "Sem conexão. Verifique sua internet."
    And o badge numérico permanece inalterado
    And a interface de atualização é desabilitada temporariamente

  Scenario: Erro interno do servidor ao consultar badges
    Given que o usuário "Ana" está autenticada no sistema
    And o servidor de notificações está em estado de manutenção
    When o serviço recebe a requisição "GET /api/v1/notifications/badges"
    Then o serviço retorna HTTP 503 Service Unavailable
    And o corpo da resposta contém a mensagem "Serviço temporariamente indisponível"

  Scenario: Notificação push recebida com app em segundo plano
    Given que o usuário "Ana" autorizou notificações no navegador
    And o aplicativo está minimizado ou em outra aba
    When o serviço de push recebe a mensagem urgente de "João" para "Ana"
    Then o sistema operacional exibe uma notificação nativa com "João" e o trecho da mensagem
    And ao clicar na notificação, o navegador abre a conversa correspondente

  Scenario: Som de notificação customizado por contato
    Given que o usuário "Ana" configurou um som personalizado para "Filipe"
    And possui permissão de áudio habilitada no navegador
    When "Filipe" envia uma nova mensagem
    Then o sistema reproduz o som customizado ao invés do som padrão
    And o indicador visual de nova mensagem é atualizado simultaneamente