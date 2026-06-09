import { Given, When, Then, Before } from '@badeball/cypress-cucumber-preprocessor'

Before(() => {
  cy.request({
    method: 'DELETE',
    url: 'http://localhost:8000/auth/test/cleanup',
    failOnStatusCode: false,
  })
})

Given('estou na tela de cadastro', () => {
  cy.visit('/cadastro')
})

Given('já existe um usuário com e-mail {string}', (email) => {
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/auth/register',
    body: {
      email: email,
      usuario: 'usuario_existente',
      telefone: '(88) 98888-8888',
      senha: 'Segura@123',
    },
    failOnStatusCode: false,
  })
})

When('preencho o telefone com {string}', (telefone) => {
  cy.get('[data-cy="input-telefone"]').clear().type(telefone)
})

When('preencho o nome de usuário com {string}', (nome) => {
  cy.get('[data-cy="input-usuario"]').clear().type(nome)
})

When('clico no botão de cadastro', () => {
  cy.get('[data-cy="btn-cadastrar"]').click()
})

Then('sou redirecionado para a tela de sucesso', () => {
  cy.url().should('include', '/cadastro-sucesso')
  cy.get('[data-cy="msg-sucesso"]').should('be.visible')
})

When('clico no link {string}', (texto) => {
  cy.contains(texto).click()
})

Then('sou redirecionado para a tela de boas-vindas', () => {
  cy.url().should('include', '/')
  cy.url().should('not.include', '/cadastro')
})

Then('sou redirecionado para a tela de cadastro', () => {
  cy.url().should('include', '/cadastro')
})