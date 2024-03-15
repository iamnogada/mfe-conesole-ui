/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../**/*.html"],
  theme: {
    extend: {
      gridTemplateColumns: {
        'lnbwidth': 'var(--lnbwidth) 1fr',
      },
      size: {
        'gnbheight': 'var(--gnbheight)',
      },
      spacing: {
        'gnbheight': 'var(--gnbheight)',
      },
    }
  },
  plugins: []
}

