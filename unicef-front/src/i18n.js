import { createI18n } from "vue3-i18n"
import { messages } from "vite-i18n-resources"
import { useStorage } from '@vueuse/core'
import { setDefaultOptions } from 'date-fns'
import { ptBR, enUS, es } from 'date-fns/locale'

const appDefaultLang = 'pt'

const state = useStorage('app-store', { lang: appDefaultLang })
const locale = appDefaultLang == state.value.lang ? ptBR : 'es' == state.value.lang ? es : enUS || ptBR
setDefaultOptions({ locale })

const i18n = createI18n({
  legacy: false,
  locale: appDefaultLang == state.value.lang ? appDefaultLang : 'es' == state.value.lang ? 'es'  : 'en',
  fallbackLocale: appDefaultLang == state.value.lang ? appDefaultLang : 'es' == state.value.lang ? 'es': 'en',
  globalInjection: true,
  silentTranslationWarn: true,
  messages
})

// https://github.com/fvena/vite-plugin-i18n-resources/issues/49
// if (import.meta.hot) {
//   import.meta.hot.on("locales-update", (data) => {
//     Object.keys(data).forEach((lang) => {
//       i18n.i18n.global.setLocaleMessage(lang, data[lang])
//     })
//   })
// }

export default i18n