<template>
    <Popover v-slot="{ open }" class="relative">
      <PopoverButton :focus="false">
        <div class="hover:scale-125">
          <div v-if="1 == status" class="w-9 h-9 bg-lime-600 border border-lime-600 shadow-md rounded-full"></div>

          <span v-else-if="2 == status"
                class="flex h-9 w-9">
              <span class="animate-ping absolute inline-flex h-9 w-9 rounded-full bg-red-500 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-9 w-9 bg-red-500"></span>
          </span>

          <div v-else-if="3 == status" class="w-9 h-9 bg-red-500 border border-tranparent shadow-md rounded-full"></div>
          <div v-else-if="4 == status" class="w-9 h-9 bg-neutral-200 border border-tranparent shadow-md rounded-full"></div>
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
        <PopoverPanel
          class="absolute left-1/2 z-10 mt-3 w-auto max-w-sm transform-gpu px-4 sm:px-0 lg:max-w-3xl"
          :class="{ '-translate-x-72': rangeIndex == 12, '-translate-x-48': rangeIndex != 12,  }"
        >
          <div
            class="overflow-hidden rounded-lg shadow-lg"
          >
          <slot />
          </div>
        </PopoverPanel>
      </transition>
    </Popover>

</template>


<script setup>
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { ChevronDownIcon } from '@heroicons/vue/outline'
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
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
