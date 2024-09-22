import { defineUserConfig } from 'vuepress'
import { defaultTheme } from '@vuepress/theme-default'
import { viteBundler } from '@vuepress/bundler-vite'

export default defineUserConfig({
  lang: 'en-US',
  title: 'Child Health Tracker',
  description: 'Frontend documentation for the Child Health Tracker',
  theme: defaultTheme({
    navbar: [
      { text: 'Home', link: '/' },
      { text: 'Getting Started', link: '/getting-started.html' },
      { text: 'Components', link: '/components/' },
      { text: 'Views', link: '/views/' },
      { text: 'State Management', link: '/state-management.html' },
      { text: 'API Integration', link: '/api-integration.html' },
    ],
    sidebar: [
      '/',
      '/getting-started',
      {
        text: 'Components',
        children: [
          '/components/',
          '/components/component1',
          '/components/component2',
        ]
      },
      {
        text: 'Views',
        children: [
          '/views/',
          '/views/view1',
          '/views/view2',
        ]
      },
      '/state-management',
      '/api-integration',
    ]
  }),
  bundler: viteBundler(),
})
