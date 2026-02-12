import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue2'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  // 定义全局变量，处理process.env.NODE_ENV
  define: {
    'process.env.NODE_ENV': JSON.stringify('production')
  },
  build: {
    outDir: path.resolve('../backend/frontend'),
    emptyOutDir: true,
    // 使用默认的应用模式构建
    rollupOptions: {
      output: {
        // 生成单个文件，不使用代码分割
        manualChunks: undefined,
        // 输出文件名称
        entryFileNames: 'assets/index.js'
      }
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
})