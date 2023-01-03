describe('Bootstrap Test', () => {
  it('builds, tests runs and visits the app root url', () => {
    cy.visit('/')
    cy.contains('h1', 'UNICEF')
    cy.get('#email').type('teste@teste.com')
    cy.get('#password').type('teste')
    cy.get('.inline-flex > span').click()
  })
  it('visits the app dashboard when logo got clicked', () => {
    cy.visit('/')
    cy.get('.h-16').click()
    cy.contains('h2', 'Dashboard')
  })
  it('visits the app vaccine url', () => {
    cy.visit('/#/pages/Patients')
    cy.contains('h2', 'Patients')
  })
  it('visits the app home when logout', () => {
    cy.visit('/#/pages/Patients')
    cy.get('.mx-5').click()
    cy.get('#headlessui-menu-item-3').click()
    cy.contains('a', 'Register')
  })
})
