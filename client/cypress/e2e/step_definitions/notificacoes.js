import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor';

Given('que iniciei sessao como {string}', (usuario) => {
  // Limpa o BD e cadastra os usuarios necessarios antes do login
  cy.request({
    method: 'DELETE',
    url: 'http://localhost:8000/auth/test/cleanup',
    failOnStatusCode: false,
  });

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

  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/auth/register',
    failOnStatusCode: false,
    body: {
      usuario: 'joao',
      email: 'joao@email.com',
      telefone: `119${Math.floor(10000000 + Math.random() * 90000000)}`,
      senha: 'senha123'
    }
  });
  
  cy.visit('/login');
  cy.get('[data-cy="input-email"]').type(`${usuario}@email.com`);
  cy.get('[data-cy="input-senha"]').type('senha123');
  cy.get('[data-cy="btn-entrar"]').click();
  cy.url().should('include', '/chat');
});

Given('{string} envia a mensagem {string} para {string}', (remetente, mensagem, destinatario) => {
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
  // Espera a mensagem trafegar
  cy.wait(500);
});

Given('{string} envia {int} mensagens nao lidas para {string}', (remetente, quantidade, destinatario) => {
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
  // Espera os websocekts fecharem
  cy.wait(500);
});

When('atualizo a tela de chat', () => {
  cy.url().should('include', '/chat');
  cy.reload();
  cy.wait(500); // Aguarda renderizacao do React pos-reload
});

When('clico no contato {string} na barra lateral', (contato) => {
  // Recarrega a tela para garantir que o contato apareca na lista antes do clique
  cy.reload();
  cy.wait(500);
  cy.get(`[data-cy="contato-${contato}"]`).should('be.visible').click();
});

Then('vejo o badge {string} ao lado de {string} na lista de contatos', (badge, contato) => {
  cy.get(`[data-cy="contato-${contato}"] [data-cy="badge-notificacao"]`)
    .should('be.visible')
    .and('contain', badge);
});

Then('o badge ao lado de {string} e removido', (contato) => {
  cy.get(`[data-cy="contato-${contato}"] [data-cy="badge-notificacao"]`)
    .should('not.exist');
});

Then('vejo o banner de notificacao com {string} e {string}', (remetente, texto) => {
  cy.get('[data-cy="banner-notificacao"]')
    .should('be.visible')
    .and('contain', remetente)
    .and('contain', texto);
});

Then('o banner desaparece apos 4 segundos', () => {
  // Aumentado ligeiramente para evitar que o cypress faca assercao antes da animacao acabar
  cy.wait(4500);
  cy.get('[data-cy="banner-notificacao"]').should('not.exist');
});