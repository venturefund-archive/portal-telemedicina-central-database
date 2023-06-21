describe('Bootstrap Test', () => {
  it('builds, tests runs and visits the app root url', async () => {
    // clean()
    cy.visit('http://localhost:4173/patients/682b9259-1e18-4c2f-9a13-b4ba6f72f230/', { timeout: 10000 })
    cy.get('#username').type('asd')
    cy.get('#password').type('asd+1234{enter}')

    cy.get('div[data-dose-id="2"][data-dose-type="recomended"]');

    cy.get('div[data-dose-id="2"][data-dose-type="recomended"]').click()
        cy.get('div[data-dose-id="2"][data-dose-type="recomended"]').should('be.visible')
        cy.contains('h2', 'Dose recomendada').should('be.visible')
    cy.get('body').type('{esc}');


    cy.get('.-mt-24 > :nth-child(1) > div > .flex > .uppercase', { timeout: 10000 }).click()
    cy.get('#vacina').select('8')
    cy.get('#dose').select('2')
    cy.get('#data_application').type('2023-01-01')
    cy.get('#next_data_application').type('2023-01-01')
    cy.get('#batch').type('aaa')
    cy.get('#cns_number').type('aaa')
    cy.get('#cnes_number').type('aaa')
    cy.get('input#health_professional').type('aaa')
    cy.get('input#health_professional').type('{enter}')
    cy.reload()
    cy.wait(5000)

    cy.get('body').then(($body) => {
      if ($body.find('div[data-dose-id="2"][data-dose-type="completed"]').length > 0) {
        // verifica se o elemento existe
        cy.get('div[data-dose-id="2"][data-dose-type="completed"]').click()
        cy.get('div[data-dose-id="2"][data-dose-type="completed"]').should('be.visible')
        cy.contains('h2', 'Dose completa').should('be.visible')
        cy.get('body').type('{esc}');
      }
    })
  })

  const clean = () => {
    cy.visit('http://localhost:8000/api/admin/vaccines/vaccinestatus/', { timeout: 10000 })
    cy.get(':nth-child(2) > .required').click()
    cy.get('#id_username').click()
    cy.get('#id_username').type('admin')
    cy.get('#id_password').type('admin{enter}')
    cy.get('body').then(($body) => {
      if ($body.find('#action-toggle', { timeout: 10000 }).length > 0) {
        // verifica se o elemento existe
        cy.get('#action-toggle').check() // executa a ação somente se o elemento existe
        cy.get('select').select('delete_selected')
        cy.get('.button').click()
        cy.get('[type="submit"]').click()
      }
    })
  }
})
