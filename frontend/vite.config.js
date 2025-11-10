import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // 允许所有网络接口访问（包括 cpolar 公网域名）
    port: 5174,
    strictPort: false,
    // 注意：Vite 可能不支持 allowedHosts（这是 webpack 的选项）
    // 如果遇到问题，可以尝试移除 allowedHosts，CORS headers 应该足够
    // 允许 cpolar 公网域名访问，解决跨域问题
    // 如果有多个域名，可以添加多个
    allowedHosts: [
      '4e14a460.20.vp.cpolar.cn',  // 之前的域名
      '4534f746.r30.cpolar.top',    // 当前使用的域名
      // cpolar 域名通配符（支持所有 cpolar 域名）
      '.vp.cpolar.cn',
      '.cpolar.cn',
      '.cpolar.top',
      '.r30.cpolar.top',
      // 如果还有其他格式的 cpolar 域名，可以继续添加
    ],
    // 添加 CORS 头，解决跨域问题（这是主要解决方案）
    cors: true, // 启用 CORS
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    },
    // 代理后端 API - 统一通过 /api 前缀访问
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8021',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        configure: (proxy, _options) => {
          proxy.on('error', (err, _req, _res) => {
            console.log('proxy error', err);
          });
          proxy.on('proxyReq', (proxyReq, req, _res) => {
            console.log('Proxying:', req.method, req.url);
          });
        }
      }
    }
  },
  preview: {
    host: '0.0.0.0',
    port: 5174,
    strictPort: false
  }
})
