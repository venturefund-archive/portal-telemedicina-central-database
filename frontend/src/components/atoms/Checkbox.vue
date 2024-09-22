<template>
  <input
    type="checkbox"
    :value="value"
    v-model="isChecked"
    class="rounded border-gray-300 text-blue-500 focus:border-blue-300 focus:ring focus:ring-blue-500"
    @change="$emit('update:checked', isChecked)"
  />
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['update:checked'])

const props = defineProps({
  checked: {
    type: [Array, Boolean],
    default: false,
  },
  value: {
    default: null,
  },
})

const { value, checked } = props

const isChecked = ref(checked)
</script>
