import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor';

Given('que estou autenticado como {string}', (usuario) => {
  // Registrar usuário via API
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/auth/register',
    failOnStatusCode: false,
    body: {
      usuario: usuario,
      email: `${usuario}@email.com`,
      telefone: `119${Math.floor(10000000 + Math.random() * 90000000)}`,
      senha: 'senha123'
    }
  });
  
  // Fazer login
  cy.visit('/login');
  cy.get('[data-cy="input-email"]').type(`${usuario}@email.com`);
  cy.get('[data-cy="input-senha"]').type('senha123');
  cy.get('[data-cy="btn-entrar"]').click();
  cy.url().should('include', '/chat');
});

Given('{string} envia a mensagem {string} para {string}', (remetente, mensagem, destinatario) => {
  // Registrar remetente
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/auth/register',
    failOnStatusCode: false,
    body: {
      usuario: remetente,
      email: `${remetente}@email.com`,
      telefone: `119${Math.floor(10000000 + Math.random() * 90000000)}`,
      senha: 'senha123'
    }
  });
  
  // Enviar mensagem via WebSocket
  cy.window().then((win) => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${remetente}`);
    ws.onopen = () => {
      ws.send(JSON.stringify({
        para: destinatario,
        texto: mensagem
      }));
      setTimeout(() => ws.close(), 100);
    };
  });
  cy.wait(500);
});

Given('{string} envia {int} mensagens não lidas para {string}', (remetente, quantidade, destinatario) => {
  // Registrar remetente
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/auth/register',
    failOnStatusCode: false,
    body: {
      usuario: remetente,
      email: `${remetente}@email.com`,
      telefone: `119${Math.floor(10000000 + Math.random() * 90000000)}`,
      senha: 'senha123'
    }
  });
  
  // Enviar múltiplas mensagens
  for (let i = 0; i < quantidade; i++) {
    cy.window().then((win) => {
      const ws = new WebSocket(`ws://localhost:8000/ws/${remetente}`);
      ws.onopen = () => {
        ws.send(JSON.stringify({
          para: destinatario,
          texto: `Mensagem ${i + 1}`
        }));
        setTimeout(() => ws.close(), 100);
      };
    });
    cy.wait(200);
  }
});

When('eu acesso a tela de chat', () => {
  cy.url().should('include', '/chat');
  cy.reload();
});

When('eu abro a conversa com {string}', (contato) => {
  cy.get(`[data-cy="contato-${contato}"]`).click();
});

Then('vejo o badge {string} ao lado de {string} na lista de contatos', (badge, contato) => {
  cy.get(`[data-cy="contato-${contato}"] [data-cy="badge-notificacao"]`)
    .should('be.visible')
    .and('contain', badge);
});

Then('o badge ao lado de {string} é removido', (contato) => {
  cy.get(`[data-cy="contato-${contato}"] [data-cy="badge-notificacao"]`)
    .should('not.exist');
});

Then('vejo o banner de notificação com {string} e {string}', (remetente, texto) => {
  cy.get('[data-cy="banner-notificacao"]')
    .should('be.visible')
    .and('contain', remetente)
    .and('contain', texto);
});

Then('o banner desaparece após 4 segundos', () => {
  cy.wait(4000);
  cy.get('[data-cy="banner-notificacao"]').should('not.exist');
});