import { defineConfig } from 'astro/config';
import tailwind from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://eejdev.github.io',
  base: '/',
  output: 'static',
  vite: {
    plugins: [tailwind()],
  },
});
