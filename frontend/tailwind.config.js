/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'et-orange': '#FF6B35',
        'et-blue': '#004E89',
        'et-dark': '#1A1A2E',
      },
    },
  },
  plugins: [],
}