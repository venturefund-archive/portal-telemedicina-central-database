<template>
  <Popover v-slot="{ open }" class="relative">
    <PopoverButton :focus="false" :class="{ 'relative z-30': open }">
      <div class="hover:scale-125" :class="{ 'scale-125': open }">
        <div v-if="1 == status" class="h-9 w-9 rounded-full border border-lime-600 bg-lime-600 shadow-md"></div>

        <span v-else-if="2 == status" class="flex h-9 w-9">
          <span class="absolute inline-flex h-9 w-9 animate-ping rounded-full bg-red-500 opacity-75"></span>
          <span class="relative inline-flex h-9 w-9 rounded-full bg-red-500"></span>
        </span>

        <div v-else-if="3 == status" class="border-tranparent h-9 w-9 rounded-full border bg-red-500 shadow-md"></div>
        <div v-else-if="4 == status" class="border-tranparent h-9 w-9 rounded-full border bg-blue-300 shadow-md"></div>
        <div v-else class=""></div>
      </div>
    </PopoverButton>
    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="translate-y-1 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="translate-y-1 opacity-0"
    >
      <div>
        <PopoverOverlay class="fixed inset-0 z-10 bg-black opacity-30" />
        <PopoverPanel
          class="absolute z-20 mt-3 w-auto max-w-sm transform-gpu px-4 sm:px-0 lg:max-w-3xl"
          :class="[rangeIndex == 11 ? '-translate-x-48' : rangeIndex <= 1 ? '' : '-translate-x-64']"
        >
          <div class="overflow-hidden rounded-lg shadow-lg">
            <slot />
          </div>
        </PopoverPanel>
      </div>
    </transition>
  </Popover>
</template>

<script setup>
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { ChevronDownIcon } from '@heroicons/vue/outline'
import { Popover, PopoverButton, PopoverPanel, PopoverOverlay } from '@headlessui/vue'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'
import { computed } from 'vue'
const router = useRouter()
const emit = defineEmits(['click'])

const props = defineProps({
  status: {
    type: Number,
    default: 0,
    validator(value) {
      return [0, 1, 2, 3, 4].includes(value)
    },
  },
  rangeIndex: {
    type: Number,
    default: 1,
    validator(value) {
      return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13].includes(value)
    },
  },
})
</script>
