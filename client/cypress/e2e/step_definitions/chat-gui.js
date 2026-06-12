import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";

// Contexto (GIVEN) e navegação
Given("que estou autenticado como {string}", (usuario) => {
  const emailFalso = `${usuario}@email.com`;
  const senhaFalsa = 'senha123'; // O FastAPI exige no mínimo 6 caracteres!

  // Prepara a base de dados: Tenta cadastrar o utilizador via API direto no backend
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/auth/register',
    failOnStatusCode: false, // Se der erro 409 (Utilizador já existe), o teste não quebra e segue em frente
    body: {
      usuario: usuario,
      email: emailFalso,
      telefone: '11999999999', // Telefone fictício para satisfazer o seu schema
      senha: senhaFalsa
    }
  });

  cy.visit('/login');
  cy.get('[data-cy="input-email"]').type(`${usuario}@email.com`);
  cy.get('[data-cy="input-senha"]').type('senha123');
  cy.get('[data-cy="btn-entrar"]').click();

  // Aguarda carregar a página principal
  cy.url().should('include', '/chat');
});

Given("estou na tela de conversa com {string}", (contato) => {
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/auth/register',
    failOnStatusCode: false, // Ignora o erro se a pessoa já existir
    body: {
      usuario: contato,
      email: `${contato}@email.com`,
      // Gera um telefone aleatório para evitar o erro de "Telefone já cadastrado"
      telefone: `119${Math.floor(10000000 + Math.random() * 90000000)}`,
      senha: 'senha123'
    }
  });

  // 2. Dá um "F5" na página para o useEffect do React ir buscar a lista atualizada
  cy.reload();
  // Clica no contato na barra lateral
  cy.get(`[data-cy="contato-${contato}"]`).click();
});

Given("que {string} e {string} já trocaram mensagens anteriormente", (user1, user2) => {
  // 1. Intercepta a requisição e injeta um histórico falso
  const historicoFalso = [
    { id_mensagem: 1, remetente: user1, texto: 'Mensagem antiga 1', data: '2026-06-11T10:00:00' },
    { id_mensagem: 2, remetente: user2, texto: 'Mensagem antiga 2', data: '2026-06-11T10:05:00' }
  ];
  cy.intercept('GET', `**/mensagens/${user1}/${user2}`, historicoFalso).as('getHistorico');

  // 2. CADASTRAR O USER 1 (joao) - O passo que faltava!
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/auth/register',
    failOnStatusCode: false,
    body: {
      usuario: user1,
      email: `${user1}@email.com`,
      telefone: `119${Math.floor(10000000 + Math.random() * 90000000)}`,
      senha: 'senha123'
    }
  });

  // 3. CADASTRAR O USER 2 (maria)
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/auth/register',
    failOnStatusCode: false,
    body: {
      usuario: user2,
      email: `${user2}@email.com`,
      telefone: `119${Math.floor(10000000 + Math.random() * 90000000)}`,
      senha: 'senha123'
    }
  });

  // 4. Agora sim, com o João existindo no banco, fazemos o login visual!
  cy.visit('/login');
  cy.get('[data-cy="input-email"]').clear().type(`${user1}@email.com`);
  cy.get('[data-cy="input-senha"]').clear().type('senha123');
  cy.get('[data-cy="btn-entrar"]').click();
  
  // Aguarda a aplicação liberar o acesso para a tela de chat
  cy.url().should('include', '/chat');
});

When("eu abro a conversa com {string}", (contato) => {
  cy.get(`[data-cy="contato-${contato}"]`).click();
  cy.wait('@getHistorico');
});

// Ações de usuário (WHEN)

When("eu digito {string} no campo de texto", (mensagem) => {
  cy.get('[data-cy="input-mensagem"]').clear().type(mensagem);
});

When("eu digito apenas espaços no campo de texto", () => {
  cy.get('[data-cy="input-mensagem"]').clear().type('   ');
});

When("o campo de texto está vazio", () => {
  cy.get('[data-cy="input-mensagem"]').clear();
});

When("clico no botão de enviar", () => {
  cy.get('[data-cy="btn-enviar"]').click();
});

When("{string} envia a mensagem {string}", (remetente, mensagem) => {
  cy.window().then((win) => {
    // Descobre quem é o utilizador que está a ver o ecrã agora (o "joao")
    const meuUsuario = win.localStorage.getItem('usuario'); 

    // Cria uma nova ligação WebSocket diretamente para o backend, assumindo a identidade da Maria
    const wsMaria = new WebSocket(`ws://localhost:8000/ws/${remetente}`);

    wsMaria.onopen = () => {
      // Assim que a Maria conectar, ela dispara a mensagem para o João
      wsMaria.send(JSON.stringify({
        para: meuUsuario,
        texto: mensagem
      }));

      // Espera 100ms para garantir que o pacote foi enviado e fecha o chat da Maria
      setTimeout(() => wsMaria.close(), 100);
    };
  });

  // Aguarda meio segundo para a mensagem viajar até ao servidor e voltar para o ecrã do João
  cy.wait(500); 
});

// Validações (THEN)

Then("a mensagem {string} aparece no histórico alinhada à direita", (mensagem) => {
  cy.get('[data-cy="mensagem-chat"]').last()
    .should('contain', mensagem)
    .and('have.css', 'text-align', 'right'); // Ajuste conforme o seu CSS/Tailwind
});

Then("a mensagem {string} aparece no histórico alinhada à esquerda", (mensagem) => {
  cy.get('[data-cy="mensagem-chat"]').last()
    .should('contain', mensagem)
    .and('have.css', 'text-align', 'left'); // Ajuste conforme o seu CSS/Tailwind
});

Then("o campo de texto fica vazio", () => {
  cy.get('[data-cy="input-mensagem"]').should('have.value', '');
});

Then("a mensagem {string} aparece no histórico com o status {string}", (mensagem, status) => {
  cy.get('[data-cy="mensagem-chat"]').last().within(() => {
    cy.contains(mensagem).should('be.visible');
    cy.contains(status).should('be.visible'); 
  });
});

Then("a mensagem exibe o nome {string} como remetente", (remetente) => {
  cy.get('[data-cy="mensagem-chat"]').last().should('contain', remetente);
});

Then("o botão de enviar está desabilitado", () => {
  cy.get('[data-cy="btn-enviar"]').should('be.disabled');
});

Then("o botão de enviar está habilitado", () => {
  cy.get('[data-cy="btn-enviar"]').should('not.be.disabled');
});

Then("as mensagens anteriores aparecem no histórico em ordem cronológica", () => {
  cy.get('[data-cy="mensagem-chat"]').should('have.length.at.least', 2);
  cy.get('[data-cy="mensagem-chat"]').eq(0).should('contain', 'Mensagem antiga 1');
  cy.get('[data-cy="mensagem-chat"]').eq(1).should('contain', 'Mensagem antiga 2');
});

// Simulação de queda de rede

Given("estou sem conexão com a internet", () => {
  cy.window().then((win) => {
    // Dispara o evento exato que o nosso React está à escuta para cortar o envio
    win.dispatchEvent(new Event('offline'));
  });
});

Given("enviei a mensagem {string} que ficou com o status {string}", (mensagem, status) => {
  cy.get('[data-cy="input-mensagem"]').clear().type(mensagem);
  cy.get('[data-cy="btn-enviar"]').click();

  // Valida que o React segurou a mensagem localmente
  cy.get('[data-cy="mensagem-chat"]').last().within(() => {
    cy.contains(mensagem).should('be.visible');
    cy.contains(status).should('be.visible');
  });
});

When("a conexão com a internet é restabelecida", () => {
  cy.window().then((win) => {
    // Liga a internet de volta, o que vai acionar o useEffect de despache no React
    win.dispatchEvent(new Event('online'));
  });
  
  // Dá meio segundo para o React empacotar a mensagem e o WebSocket confirmar o envio
  cy.wait(500); 
});

Then("a mensagem {string} é enviada automaticamente", (mensagem) => {
  // Apenas garante que o balão não desapareceu da interface durante a transição
  cy.get('[data-cy="mensagem-chat"]').last().should('contain', mensagem);
});

Then("o status da mensagem é atualizado para {string}", (status) => {
  cy.get('[data-cy="mensagem-chat"]').last().within(() => {
    // Confirma que o "Aguardando conexão" sumiu e deu lugar ao "Enviada"
    cy.contains(status).should('be.visible');
  });
});