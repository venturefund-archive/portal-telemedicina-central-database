import { resolve } from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJSX from '@vitejs/plugin-vue-jsx'
import EnvironmentPlugin from 'vite-plugin-environment'
import i18nResources from 'vite-plugin-i18n-resources'
import Components from 'unplugin-vue-components/vite'

export default defineConfig({
  plugins: [
    Components(),
    i18nResources({
      path: resolve(__dirname, 'src/locales'),
    }),
    vue(),
    vueJSX(),
    EnvironmentPlugin(
      {
        NODE_ENV: 'local',
        URL: '',
        NODE_VERSION: '',
        REPOSITORY_URL: '',
        COMMIT_REF: '',
        BRANCH: '',
        CONTEXT: '',
      },
      { defineOn: 'import.meta.env' }
    ),
  ],
  // AutoImport({
  //    imports: [
  //      'vue',
  //      'vue-router',
  //      'vue-i18n',
  //      'vue/macros',
  //      '@vueuse/head',
  //      '@vueuse/core',
  //    ],
  //    dts: 'src/auto-imports.d.ts',
  //    dirs: [
  //      'src/components',
  //      // 'src/composables',
  //      // 'src/store',
  //    ],
  //    vueTemplate: true,
  //  }),

  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  // vueCompilerOptions: {
  //   isCustomElement: tag => tag.startsWith('Vue-Toastification-')
  // },

  optimizeDeps: {
    exclude: ['.out'],
  },
  server: {
    host: true,
    port: 3000,
    proxy: {
      "/api": {
        target: "http://django:8000/api",
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
  base: '/',
})
