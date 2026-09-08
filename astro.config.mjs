import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
export default defineConfig({ site: 'https://outlet3d.com.br', integrations: [sitemap()], trailingSlash: 'always' });
