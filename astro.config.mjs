import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

const isProd = process.env.NODE_ENV === 'production';

export default defineConfig({
  site: isProd ? 'https://eejdev.github.io' : undefined,
  base: isProd ? '/eejdev-blog/' : undefined,
  output: 'static',
  integrations: [tailwind()],
});

