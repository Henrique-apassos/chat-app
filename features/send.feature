feature: Enviar Mensagem

Scenario: Editar mensagem
Given estou como “emissor” “João”
And escrevi uma mensagem errada “Mensagem”
When entro no modo de edição
And mudo a mensagem para “Msg”
Then é indicado a edição com o símbolo “*”
And a mensagem “mensagem” foi alterada para “Msg” no “servidor” e “receptor”
And o “receptor” “Maria” observa a mensagem “Msg” com “*” na lista 
