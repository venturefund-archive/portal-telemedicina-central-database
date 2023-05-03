describe('Bootstrap Test', () => {
  it('builds, tests runs and visits the app root url', async () => {
    cy.visit('/')
    cy.contains('h1', 'UNICEF')
    cy.get('#username').type('camila')
    cy.get('#password').type('asd+1234{enter}')
    cy.contains('h2', 'Dashboard')
    const value = await cy.window().its('localStorage.app-store')
    const data = JSON.parse(value)
    expect(data).to.have.property('token')
    // cy.getCookie('fakeCookie1').should('have.property', 'value', '123ABC')
  })
  it('visits the app vaccine url', () => {
    cy.window().its('localStorage.app-store').should('exist')
    cy.visit('/patients')
    // cy.contains('h2', 'Patients')
  })
  // it('visits the app home when logout', () => {
  //   cy.visit('/patients')
  //   cy.get('.mx-5').click()
  //   cy.get('#headlessui-menu-item-3').click()
  //   cy.contains('a', 'Register')
  // })
})
