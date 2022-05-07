const colors = require('tailwindcss/colors')
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: [
    './unnamed/templates/base/*.html',
    './unnamed/templates/*.html'
  ],
  theme: {
    extend: {
      colors: {
        transparent: 'transparent',
        current: 'currentColor',
        black: colors.black,
        white: colors.white,
        red: colors.red,
        'neutral': {
          50: '#fafafa',
          100: '#f5f5f5',
          200: '#e5e5e5',
        },
      },
    },
    fontFamily: {
      'inter': ['Inter', 'sans-serif'],
    },
    fontSize: {
      'ultra-mini': '.5rem',
      'mini': '.65rem',
      'xs': '.75rem',
      'sm': '.875rem',
      'tiny': '.875rem',
      'base': '1rem',
      'lg': '1.125rem',
      'xl': '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
      '4xl': '2.25rem',
      '5xl': '3rem',
      '6xl': '4rem',
      '7xl': '5rem',
    },
    screens: {
      'xxs': '1px',
      'xs': '475px',
      ...defaultTheme.screens,
    },
  },
  plugins: [],
}