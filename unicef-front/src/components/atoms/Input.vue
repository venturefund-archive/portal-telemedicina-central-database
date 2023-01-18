<template>
  <input
    :class="[
      'rounded-md py-2',
      'focus:outline-none focus:ring focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-white',
      {
        'px-4': !withIcon,
        'pl-8 pr-2': withIcon,
      },
    ]"
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
    ref="input"
  />
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: String,
  withIcon: {
    type: Boolean,
    default: false,
  },
})

const input = ref(null)

const emit = defineEmits(['update:modelValue'])

const focus = () => {
  input.value.focus()
}
</script>
