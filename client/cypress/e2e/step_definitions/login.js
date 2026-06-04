import { Given, When, Then, Before } from '@badeball/cypress-cucumber-preprocessor'

Before(() => {
  cy.request({
    method: 'DELETE',
    url: 'http://localhost:8000/auth/test/cleanup',
    failOnStatusCode: false,
  })
})

Given('estou na tela de login', () => {
  cy.visit('/login')
})

Given('o usuário {string} está cadastrado com senha {string}', (email, senha) => {
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/auth/register',
    body: {
      email: email,
      nome_usuario: email.split('@')[0],
      telefone: '(88) 98888-8888',
      senha: senha,
    },
    failOnStatusCode: false,
  })
})

When('clico no botão de entrar', () => {
  cy.get('[data-cy="btn-entrar"]').click()
})

Then('sou redirecionado para o chat', () => {
  cy.url().should('include', '/chat')
})