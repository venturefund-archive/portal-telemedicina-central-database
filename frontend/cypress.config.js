const { defineConfig } = require('cypress')
// https://github.com/cypress-io/cypress-realworld-app/blob/develop/cypress.config.js
module.exports = defineConfig({
  e2e: {
    specPattern: 'cypress/e2e/**/*.{cy,spec}.{js,jsx,ts,tsx}',
    baseUrl: 'http://localhost:4173',
  },
  experimentalStudio: true,
  e2e: {
    experimentalSessionAndOrigin: true,
  },
})
