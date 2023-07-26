<template>
  <div ref="target">
    <Input
      :value="modelValue"
      @input="updateModelValue"
      :placeholder="$t('dashboard.pesquisar-por-pacientes-numero-de-documento-etc')"
      class="py-4.5 block w-full pl-10 text-gray-900 focus:ring-none !focus:ring-white !focus:ring-offset-none"
      :class="{ 'w-full rounded-md bg-[#F3F3F3]  py-2.5 !shadow-md focus:shadow-none ': isInPage }"
      :autofocus="isInPage"
    />
<div class="flex justify-center">
    <ul class="border border-gray-100 absolute rounded-2xl bg-white p-2 !w-96 mt-1"
        v-if="suggestions.length && !hideSuggestions">
      <li v-for="suggestion in filtedSuggestions" :key="suggestion.name" class="cursor-pointer hover:bg-gray-100 rounded">
        <router-link
          :to="{ name: 'PatientDetails', params: { id: suggestion.id } }"
          class="hover:underline"
          @click="handleClick({id:suggestion.id})"
        >
          <div class="flex items-center gap-4 px-2 py-3">
            <img class="h-10 w-10 rounded-full bg-neutral-200 p-1" src="/avatar.png" />
            <span class="text-sm font-medium capitalize text-slate-900">{{
              suggestion.name.toLowerCase()
            }}</span>
          </div>
        </router-link>
      </li>
    </ul>
  </div>
  </div>
</template>

<script setup>
import { ref, toRefs, computed } from 'vue'
import { onClickOutside } from '@vueuse/core'

const emit = defineEmits(['click', 'update:modelValue'])
const props = defineProps({
  isInPage: {
    type: Boolean,
    default: false,
  },
  suggestions: {
    type: Array,
    default: [],
  },
  modelValue: {
    type: String,
    default: '',
  },
  variant: {
    type: String,
    default: 'primary',
    validator(value) {
      return ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'black'].includes(value)
    },
  },
  type: {
    type: String,
    default: 'search',
  },
  size: {
    type: String,
    default: 'base',
    validator(value) {
      return ['sm', 'base', 'lg'].includes(value)
    },
  },
})
import { useStorage } from '@vueuse/core'
const state = useStorage('app-store', { token: '' })
const handleClick = ({id}) => {
  hideSuggestions.value = true
  state.value.patientLastViewed = id
}
const filtedSuggestions = computed(() => {
  return props.suggestions.slice(0, 5)
})

const hideSuggestions = ref(true)
const updateModelValue = (event) => {
  emit('update:modelValue', event.target.value)
  hideSuggestions.value = false
}

const target = ref(null)

onClickOutside(target, (event) => (hideSuggestions.value = true))

// <AutoComplete v-model="queryText" :suggestions="filteredResultsBasic" @complete="search($event)" optionLabel="name" />
</script>
