// astro.config.mjs
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

const isProd = process.env.NODE_ENV === 'production';

export default defineConfig({
  site: isProd ? 'https://eejdev.github.io' : undefined,
  // no `base`—your repo is the personal pages root, so no subdirectory
  output: 'static',
  vite: {
    plugins: [tailwindcss()],
  },
});

