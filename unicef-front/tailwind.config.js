const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        green: {
          500: '#009334',
        },
        gray: {
          400: '#B0B0B0',
        },
        blue: {
          500: '#009FE3',
          600: '#0082C9',
          660: ' #035886',
        },
        red: {
          500: '#FF5363',
          600: '#FF5363',
        },
        yellow: {
          500: '#FFA901',
        },

        // ...
      },
      fontSize: {
        xl: '1.25rem',
      },

      fontFamily: {
        roboto: ['Roboto', 'sans-serif'],
      },
      boxShadow: {
        't-lg':
          'var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), 0 -10px 15px -3px rgba(0, 0, 0, 0.1), 0 -4px 6px -2px rgba(0, 0, 0, 0.05)',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/line-clamp'),
    require('@tailwindcss/aspect-ratio'),
  ],
}
