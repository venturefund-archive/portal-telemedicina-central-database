<template>
  <div class="relative">
    <button
      @click="toggleDropdown"
      class="border-r-1 border-l-1 group inline-flex items-center justify-center gap-2 border border-gray-100 border-b-transparent border-t-transparent px-4 py-2"
    >
      <img class="h-5 w-5 rounded" :src="selectedLang.flag" :alt="selectedLang.name" />
      <span class="text-sm font-semibold">{{ selectedLang.name }}</span>
      <svg
        class="h-5 w-5 fill-gray-500 group-hover:fill-gray-500"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path fill-rule="evenodd" d="M10 14.667L3.333 8 5 6.333 10 11.333 15 6.333 16.667 8z" clip-rule="evenodd" />
      </svg>
    </button>
    <div
      v-if="isDropdownOpen"
      class="absolute -right-0 z-20 mt-2 origin-top-right divide-y divide-gray-100 rounded-md border border-gray-100 bg-white p-2 shadow-lg outline-none"
      @click.away="isDropdownOpen = false"
    >
      <div class="py-1">
        <button
          v-for="lang in availableLangsFiltered"
          :key="lang.code"
          @click="selectLang(lang)"
          class="flex px-4 py-2 text-left hover:bg-gray-100 hover:text-gray-900"
        >
          <img class="h-5 w-5 rounded" :src="lang.flag" :alt="lang.name" />
          <span class="ml-3 text-sm font-semibold">{{ lang.name }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue3-i18n'
import { setDefaultOptions } from 'date-fns'
import { ptBR, enUS } from 'date-fns/locale'
import { useStorage } from '@vueuse/core'
const i18n = useI18n()
const { t, locale } = useI18n()

const availableLangs = ref([
  {
    code: 'pt',
    name: 'PT-BR',
    flag: 'https://flagicons.lipis.dev/flags/4x3/br.svg',
  },
  {
    code: 'en',
    name: 'EN-US',
    flag: 'https://flagicons.lipis.dev/flags/4x3/us.svg',
  },
  {
    code: 'es',
    name: 'ES-ES',
    flag: 'https://flagicons.lipis.dev/flags/4x3/es.svg',
  },
])

const availableLangsFiltered = computed(() => {
  return availableLangs.value.filter((lang) => {
    return lang.code !== i18n.getLocale()
  })
})

const currentSelectedLang = ref()

const selectedLang = computed(() => {
  return availableLangs.value.find((lang) => {
    return lang.code === currentSelectedLang.value || lang.code === i18n.getLocale()
  })
})
const setLocale = (lang) => {
  i18n.setLocale(lang)
  currentSelectedLang.value = lang
  setDefaultOptions({ locale: 'pt' == lang ? ptBR : enUS })
  const state = useStorage('app-store', { lang })
  state.value.lang = lang
}

const isDropdownOpen = ref(false)

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
}

const selectLang = (lang) => {
  setLocale(lang.code)
  toggleDropdown()
}
</script>
