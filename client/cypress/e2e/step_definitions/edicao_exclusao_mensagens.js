import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor'

const usuarioLogado = 'usuario_teste'
const contato = 'joao'

function prepararChatComMensagem({ minha = true, texto = 'Mensagem original' } = {}) {
  localStorage.setItem('usuario', usuarioLogado)

  cy.intercept('GET', 'http://127.0.0.1:8000/auth/usuarios', {
    statusCode: 200,
    body: [{ usuario: contato, nome: 'João' }],
  }).as('getContatos')

  cy.intercept('GET', `http://127.0.0.1:8000/mensagens/${usuarioLogado}/${contato}`, {
    statusCode: 200,
    body: [
      {
        id_mensagem: 1,
        remetente: minha ? usuarioLogado : contato,
        texto,
      },
    ],
  }).as('getMensagens')

  cy.visit('/chat')
  cy.wait('@getContatos')
  cy.contains('João').click()
  cy.wait('@getMensagens')
  cy.contains(texto).should('be.visible')
}

// =========================
// GIVEN
// =========================

Given('estou autenticado no chat', () => {
  localStorage.setItem('usuario', usuarioLogado)
})

Given('existe uma mensagem enviada por mim', () => {
  prepararChatComMensagem({
    minha: true,
    texto: 'Mensagem original',
  })
})

Given('existe uma mensagem enviada por outro usuário', () => {
  prepararChatComMensagem({
    minha: false,
    texto: 'Mensagem de outro usuário',
  })
})

Given('excluí uma mensagem', () => {
  prepararChatComMensagem({
    minha: true,
    texto: 'Mensagem para excluir',
  })

  cy.intercept('DELETE', 'http://127.0.0.1:8000/mensagens/1', {
    statusCode: 200,
    body: {
      mensagem: 'Mensagem excluída com sucesso',
      id_mensagem: 1,
    },
  }).as('excluirMensagem')

  cy.get('[data-cy="btn-excluir-mensagem"]').click()
  cy.wait('@excluirMensagem')
})

Given('a exclusão foi autorizada', () => {
  cy.contains('Mensagem para excluir').should('not.exist')
})

// =========================
// WHEN
// =========================

When('clico em editar', () => {
  cy.window().then((win) => {
    cy.stub(win, 'prompt').returns('Mensagem Editada')
  })

  cy.intercept('PUT', 'http://127.0.0.1:8000/mensagens/1', {
    statusCode: 200,
    body: {
      mensagem: 'Mensagem editada com sucesso',
      id_mensagem: 1,
      texto: 'Mensagem Editada',
      editada: true,
    },
  }).as('editarMensagem')

  cy.get('[data-cy="btn-editar-mensagem"]').click()
})

When('altero o texto para {string}', () => {
  cy.wait('@editarMensagem')
})

When('tento editar essa mensagem', () => {
  cy.get('[data-cy="btn-editar-mensagem"]').should('not.exist')
})

When('clico em excluir', () => {
  cy.intercept('DELETE', 'http://127.0.0.1:8000/mensagens/1', {
    statusCode: 200,
    body: {
      mensagem: 'Mensagem excluída com sucesso',
      id_mensagem: 1,
    },
  }).as('excluirMensagem')

  cy.get('[data-cy="btn-excluir-mensagem"]').click()
  cy.wait('@excluirMensagem')
})

When('tento excluir essa mensagem', () => {
  cy.get('[data-cy="btn-excluir-mensagem"]').should('not.exist')
})

When('a conversa é atualizada', () => {
  cy.reload()
})

// =========================
// THEN
// =========================

Then('devo visualizar a mensagem editada', () => {
  cy.contains('Mensagem Editada').should('be.visible')
  cy.contains('(editada)').should('be.visible')
})

Then('o sistema deve impedir a edição', () => {
  cy.get('[data-cy="btn-editar-mensagem"]').should('not.exist')
})

Then('a mensagem deve permanecer sem alteração', () => {
  cy.contains('Mensagem de outro usuário').should('be.visible')
})

Then('a mensagem deve ser removida da conversa', () => {
  cy.contains('Mensagem original').should('not.exist')
})

Then('o sistema deve impedir a exclusão', () => {
  cy.get('[data-cy="btn-excluir-mensagem"]').should('not.exist')
})

Then('a mensagem deve permanecer na conversa', () => {
  cy.contains('Mensagem de outro usuário').should('be.visible')
})

Then('a mensagem não deve aparecer na conversa', () => {
  cy.contains('Mensagem para excluir').should('not.exist')
})