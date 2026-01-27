import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    proxy: {
      // Frontend calls "/api/..." and Vite proxies to FastAPI in dev.
      '/api': 'http://nostromo.yutani.tech:54321'
    }
  }
});
