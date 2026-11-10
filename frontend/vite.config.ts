import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  // GitHub Pages serves this project from /<repository-name>/, not /.
  base: '/igebra-ai-platform/',
  plugins: [react()],
  server: {
    port: 5173,
    host: true
  }
});
