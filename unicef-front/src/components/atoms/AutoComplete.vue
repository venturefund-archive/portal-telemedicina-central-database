<template>
  <div ref="target">
    <input
      :type="type"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value);hideSuggestions = false"
      class="block w-full rounded-lg border border-transparent bg-gray-50 p-4 pl-10 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500 md:w-96"
      placeholder="Procure por pacientes, numero de documento etc"
      required
    />

    <ul class="absolute w-full rounded bg-white p-2" v-if="suggestions.length && !hideSuggestions">
      <li v-for="suggestion in asd" :key="suggestion.name" class="cursor-pointer hover:bg-neutral-200">
        <router-link
          :to="{ name: 'PatientDetails', params: { id: suggestion.id } }"
          class="hover:underline"
          @click="hideSuggestions = true"
        >
          <div class="flex items-center gap-4 px-2 py-2">
            <img class="h-10 w-10 rounded-full bg-neutral-200 p-1" src="/avatar.png" />
            <span class="text-sm font-medium text-slate-900 capitalize">{{ suggestion.name.join().toLowerCase() }}</span>
          </div>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, toRefs, computed } from 'vue'
import { onClickOutside } from '@vueuse/core'

const emit = defineEmits(['click', 'update:modelValue'])
const props = defineProps({
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

const asd = computed(() => {
return props.suggestions.slice(0,5)
} )

const hideSuggestions = ref(true)
const target = ref(null)

onClickOutside(target, (event) => hideSuggestions.value = true)

// <AutoComplete v-model="queryText" :suggestions="filteredResultsBasic" @complete="search($event)" optionLabel="name" />
</script>
