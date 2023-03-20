<template>
  <div class="flex justify-center gap-5 px-4 scale-90">
        <button
                @click="setLocale('en')"
                class="inline-flex hover:border-trasparent border-neutral-400 shadow-lg border rounded">
          <img class="w-10 cursor-pointer rounded"
              :class="i18n.getLocale() == 'en' ? 'grayscale-0' : 'grayscale hover:grayscale-0'"
                src="https://flagicons.lipis.dev/flags/4x3/us.svg" />
        </button>
        <button
                @click="setLocale('pt')"
                class="inline-flex hover:border-trasparent border-neutral-400 shadow-lg border rounded">
          <img class="w-10 cursor-pointer rounded"
              :class="i18n.getLocale() == 'pt' ? 'grayscale-0' : 'grayscale hover:grayscale-0'"
                src="https://flagicons.lipis.dev/flags/4x3/br.svg" />
        </button>
          <button
                  @click="setLocale('es')"
                  class="inline-flex hover:border-trasparent border-neutral-400 shadow-lg border rounded">
            <img class="w-10 cursor-pointer rounded"
                :class="i18n.getLocale() == 'es' ? 'grayscale-0' : 'grayscale hover:grayscale-0'"
                  src="https://flagicons.lipis.dev/flags/4x3/es.svg" />
          </button>
    </div>
</template>

<script setup>
import { useI18n } from "vue3-i18n"
import { setDefaultOptions } from 'date-fns'
import { ptBR, enUS } from 'date-fns/locale'
import { useStorage } from '@vueuse/core'
const i18n = useI18n()
const { t, locale } = useI18n()

const setLocale = (lang) => {
  i18n.setLocale(lang)
  setDefaultOptions({ locale: 'pt' == lang ? ptBR : enUS })
  const state = useStorage('app-store', { lang })
  state.value.lang = lang
}
</script>