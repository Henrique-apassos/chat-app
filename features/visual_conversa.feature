Feature: visual da conversa
As a um usuário
I want to ver minhas mensagens trocadas em uma conversa

Scenario: Envio de mensagem de texto com sucesso (Happy Path)
	Given Eu estou na conversa com “João”
	When Eu envio uma mensagem “Olá, joão!”
	Then A mensagem aparece como enviada
	And a rolagem da conversa desce automaticamente para baixo

Scenario: Exclusão de mensagem para todos
	Given Eu enviei uma mensagem a “João” há menos de 10 minutos
	When Eu seleciono a opção “Excluir mensagem para todos”
	Then A mensagem “item excluído” deverá aparecer para todos no lugar da mensagem

Scenario: Arquivo muito grande (Sad Path)
	Given que eu estou em uma conversa e clico para anexar uma mídia
	When eu seleciono um arquivo de vídeo com tamanho superior a 64MB
	Then o sistema deve impedir o anexo And deve exibir um alerta dizendo "O arquivo excede o limite de 64MB

Scenario: Busca por mensagens
	Given que eu possuo um longo histórico de mensagens com a "Maria"
	When eu pesquiso pela palavra "endereço" na barra de busca da conversa
	Then a interface deve filtrar e destacar apenas as bolhas de mensagem que contêm a palavra "endereço"
	And a rolagem irá automaticamente para essa bolha de mensagem

Scenario: Envio de mensagem de texto sem sucesso (Sad Path)
	Given Eu estou na conversa com "joão" e estou sem conexão com a internet
	When Eu envio uma mensagem "Olá, joão!"
	Then A mensagem deve aparecer na minha tela com um ícone de "relógio" (pendente de envio)
	And a mensagem deve ser enviada automaticamente pelo sistema assim que a internet for restabelecida