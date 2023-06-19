<template>
  <div class="group relative inline-block flex items-center">
    <slot name="trigger"></slot>

    <div
      :class="[
        'absolute z-10 w-36 rounded py-1 px-2 text-xs font-semibold text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100',
        tooltipClass,
      ]"
      :style="tooltipStyle"
    >
      <slot name="content"></slot>
      <div :class="['absolute h-3 w-3', arrowClass]" :style="arrowStyle"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'blue',
  },
  position: {
    type: String,
    default: 'top',
  },
})

const tooltipClass = computed(() => {
  switch (props.variant) {
    case 'gray':
      return 'bg-white drop-shadow-lg shadow-2xl text-gray-700 font-normal'
    case 'green':
      return 'bg-green-500 bg-opacity-70'
    default:
      return 'bg-blue-500 bg-opacity-70'
  }
})

const arrowClass = tooltipClass

const tooltipStyle = computed(() => {
  switch (props.position) {
    case 'bottom':
      return { bottom: '100%', transform: 'translateY(0)' }
    case 'right':
      return { left: '70%', transform: 'translateY(-30%)' }
    default: // top
      return { top: '0%', transform: 'translateY(-100%)' }
  }
})

const arrowStyle = computed(() => {
  switch (props.position) {
    case 'bottom':
      return {
        clipPath: 'polygon(50% 0%, 0 100%, 100% 100%)',
        top: '0',
        left: '50%',
        transform: 'translate(-50%, -100%)',
      }
    case 'right':
      return {
        clipPath: 'polygon(0 50%, 100% 0%, 100% 100%)',
        left: '0',
        top: '50%',
        transform: 'translate(-100%, -50%)',
      }
    default: // top
      return {
        clipPath: 'polygon(50% 100%, 100% 0, 0 0)',
        bottom: '0',
        left: '50%',
        transform: 'translate(-50%, 100%)',
      }
  }
})
</script>
