import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

const proxyTarget = process.env.API_PROXY_TARGET || 'http://127.0.0.1:8000'
const proxyChangeOrigin = process.env.API_PROXY_CHANGE_ORIGIN !== 'false'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 5173,
    watch: {
      usePolling: process.env.DEV_SERVER_POLLING === 'true'
    },
    proxy: {
      '/api': {
        target: proxyTarget,
        changeOrigin: proxyChangeOrigin
      },
      '/media': {
        target: proxyTarget,
        changeOrigin: proxyChangeOrigin
      }
    }
  }
})
