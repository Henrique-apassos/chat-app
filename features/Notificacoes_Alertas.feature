Feature: Notificações e Alertas
  As a usuário do aplicativo de chat
  I want to receber avisos visuais e sonoros de novas mensagens
  So that eu saiba que recebi algo mesmo estando fora da tela do chat

  Scenario: Banner de notificação exibido em outra tela
    Given que o usuário "Ana" está na tela "Configurações de Perfil"
    And possui conexão ativa com o servidor
    When o usuário "Filipe" envia a mensagem "E aí, tudo bem?" para "Ana"
    Then o sistema exibe um banner no topo da tela com "Filipe" e "E aí, tudo bem?"
    And o banner desaparece após 4 segundos

  Scenario: Badge zerado ao abrir conversa
    Given que o usuário "Ana" está na tela "Lista de Conversas"
    And o badge ao lado de "João" exibe "3" mensagens não lidas
    When "Ana" abre a conversa com "João"
    Then o badge ao lado de "João" é removido
    And todas as mensagens de "João" ficam marcadas como lidas