/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'ink': '#2c2c2c',
        'paper': '#f7f3e9',
        'wood': '#8b5a2b',
        'cinnabar': '#c23a30',
        'jade': '#5a8f7b',
      },
    },
  },
  plugins: [],
}
