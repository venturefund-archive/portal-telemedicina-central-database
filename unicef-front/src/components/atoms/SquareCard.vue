<template>
  <div
    @click="clicked = !clicked"
    :class="{
      'scale-105 border bg-gradient-to-t from-gray-100  via-transparent to-transparent shadow-lg ': clicked,
      'shadow-md': !clicked,
    }"
    :actions="actions"
    class="transition-shadow-md flex w-52 transform cursor-pointer flex-col items-center justify-center overflow-hidden rounded-2xl border border-gray-200 bg-white p-4 shadow transition-transform duration-500 duration-500 ease-in-out hover:scale-105 hover:shadow-lg"
  >
    <div class="flex w-full items-center justify-center py-2">
      <slot name="icon" :sizeClasses="'w-8 h-8 text-yellow-500 mr-2'"></slot>
      <span class="text-4xl font-semibold">{{ result }}</span>
    </div>

    <div class="flex flex-grow flex-col items-center justify-center pt-3">
      <h4 class="break-word text-center text-xl font-light text-black">{{ title }}</h4>
      <span class="text-md break-word hidden text-center text-gray-400">subtitle</span>
    </div>

    <div v-if="protocolStore.isLoading" class="flex flex-col p-2">
      <SkeletonLoader type="text" animation="fade-in" class="w-52" />
    </div>
  </div>
</template>

<script setup>
import { ref, toRef } from 'vue'

// Props
const props = defineProps({
  actions: {
    type: Array,
    default: () => [],
  },
  result: {
    type: String,
    default: '',
  },
  title: {
    type: String,
    default: '',
  },
  protocolStore: {
    type: Object,
    default: () => ({}),
  },
  icon: {
    type: String,
    default: '',
  },
})

// Convert props to reactive references
const actions = toRef(props, 'actions')
const result = toRef(props, 'result')
const title = toRef(props, 'title')
const protocolStore = toRef(props, 'protocolStore')
const icon = toRef(props, 'icon')
const clicked = ref(false)
</script>

<style scoped>
h4,
p {
  word-break: break-word;
  line-height: 1.2;
}
</style>
