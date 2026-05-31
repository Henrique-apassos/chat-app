import { When, Then } from '@badeball/cypress-cucumber-preprocessor'

When('preencho o e-mail com {string}', (email) => {
  cy.get('[data-cy="input-email"]').clear().type(email)
})

When('preencho a senha com {string}', (senha) => {
  cy.get('[data-cy="input-senha"]').clear().type(senha)
})

Then('vejo a mensagem de erro {string}', (mensagem) => {
  cy.get('[data-cy="msg-erro"]').should('be.visible').and('contain', mensagem)
})