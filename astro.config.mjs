import { defineConfig } from 'astro/config';

const username = 'eej-blog';
const repo = 'eej-blog';

export default defineConfig({
  site: `https://${username}.github.io/${repo}`,
  base: `/${repo}/`,
  output: 'static',
  vite: {
    plugins: [/* your existing tailwindcss plugin */],
  },
});


