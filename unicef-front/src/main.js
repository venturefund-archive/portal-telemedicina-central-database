import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from '@/App.vue'
import router from '@/router'
import Toast from 'vue-toastification'
import 'flowbite'
import './tailwind.css'
import '@/assets/css/main.css'
import { createMetaManager, plugin as metaPlugin } from 'vue-meta/dist/vue-meta.esm-browser'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { faWindowClose } from '@fortawesome/free-solid-svg-icons'
// import { createI18n } from 'vue-i18n/index'
import { messages } from 'vite-i18n-resources'
// import axios from 'axios'
import PrimeVue from 'primevue/config'
import AutoComplete from 'primevue/autocomplete';


import 'primevue/resources/themes/saga-blue/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';


const app = createApp(App)

app.use(PrimeVue);

// // Allow axios in all components with this.$http.get
// app.config.globalProperties.axios = axios;

app.use(router)
app.use(Toast, {
  hideProgressBar: true,
  closeOnClick: false,
  closeButton: false,
  icon: false,
  timeout: 5000,
  transition: 'Vue-Toastification__fade',
})
app.component('AutoComplete', AutoComplete);
app.mount('#app')
