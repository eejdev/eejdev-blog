import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'static',
  vite: {
    plugins: [/* your existing tailwindcss plugin */],
  },
});


