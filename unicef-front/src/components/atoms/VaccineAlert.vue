<template>
  <div class="relative">
    <button @click="open" :class="{ 'relative z-30': isOpen }">
      <div v-if="1 == status" class="h-9 w-9 rounded-full border border-lime-600 bg-lime-600 shadow-md"></div>

      <span v-else-if="2 == status" class="flex h-9 w-9">
        <span
          class="absolute inline-flex h-9 w-9 rounded-full bg-red-500"
          :class="{ 'animate-ping': hasActiveAlert }"
        ></span>
        <span v-if="hasActiveAlert" class="relative inline-flex h-9 w-9 rounded-full bg-red-500">
          <span class="flex h-full w-full items-center justify-center align-middle text-2xl font-semibold text-white"
            >!</span
          >
        </span>
        <div v-else class="relative flex items-center justify-center px-1">
          <VolumeOffIcon class="h-8 w-7 text-white" />
        </div>
      </span>

      <div v-else-if="3 == status" class="h-9 w-9 rounded-full border bg-red-500">
        <span class="text-2xl font-semibold text-white">!</span>
      </div>
      <div v-else-if="4 == status" class="border-tranparent h-9 w-9 rounded-full border bg-blue-300 shadow-md"></div>
    </button>

    <TransitionRoot appear :show="isOpen" as="template">
      <Dialog as="div" @close="close" class="fixed inset-0 z-50 flex items-center justify-end">
        <DialogOverlay class="fixed inset-0 bg-black opacity-50" />

        <TransitionChild
          as="template"
          enter="transform transition ease-in-out duration-500 sm:duration-700"
          enter-from="translate-x-full"
          enter-to="translate-x-0"
          leave="transform transition ease-in-out duration-500 sm:duration-700"
          leave-from="translate-x-0"
          leave-to="translate-x-full"
        >
          <DialogPanel class="fixed top-0 bottom-0 right-0 overflow-auto" style="width: 800px">
            <div class="flex items-center justify-between bg-blue-500 p-4 text-white">
              <div class="flex items-center">
                <div class="rounded-full bg-white p-2">
                  <img class="h-7 w-8" src="@/assets/images/profile-menu-02.png" />
                </div>
                <div class="flex w-full items-center justify-between space-x-4">
                  <h2 class="ml-2 text-lg font-semibold">{{ props.vaccine.description }}</h2>
                  <span>{{ $t('patient-details.dose') }} #{{ props.dose.dose_order }}</span>
                </div>
              </div>
              <button @click="close" class="text-white">
                <XIcon class="h-6 w-6" />
              </button>
            </div>

            <div class="h-full bg-white p-4">
              <slot />
            </div>
          </DialogPanel>
        </TransitionChild>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, reactive, ref, computed } from 'vue'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { XIcon, UserGroupIcon, VolumeOffIcon } from '@heroicons/vue/outline'

import { TransitionRoot, TransitionChild, Dialog, DialogOverlay, DialogPanel, DialogTitle } from '@headlessui/vue'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'
import { Transition } from 'vue'
import { usePatientsStore } from '@/stores/patients'

const patientsStore = usePatientsStore()
const router = useRouter()
const emit = defineEmits(['click'])

let isOpen = ref(false)

const open = () => {
  isOpen.value = true
}

const close = () => {
  isOpen.value = false
}

const hasActiveAlert = computed(() => props.dose.alerts.filter((alert) => alert.active).length > 0)

const props = defineProps({
  status: {
    type: Number,
    default: 0,
    validator(value) {
      return [0, 1, 2, 3, 4, 5].includes(value)
    },
  },
  rangeIndex: {
    type: Number,
    default: 1,
    validator(value) {
      return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13].includes(value)
    },
  },
  vaccine: {
    type: Object,
    default: {},
  },
  dose: {
    type: Object,
    default: {},
  },
})
</script>

<style scoped>
.slide-right-enter-active {
  transition: all 0.3s ease;
}
.slide-right-leave-active {
  transition: all 0.3s ease;
}
.slide-right-enter {
  transform: translateX(100%);
}
.slide-right-leave-to {
  transform: translateX(100%);
}
</style>
