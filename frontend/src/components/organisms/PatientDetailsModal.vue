<template>
  <TransitionRoot appear :show="props.isOpen" as="template">
    <Dialog as="div" @close="closeModal" class="fixed inset-0 z-10 flex items-center justify-end">
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
        <div class="relative h-full w-5/6">
          <div class="flex h-full flex-col overflow-y-scroll bg-white shadow-xl">
            <DialogPanel class="flex h-full flex-col bg-[#F8F9FB]">
              <div class="z-10 flex items-start justify-between rounded-t bg-gray-50 p-2 shadow-md">
                <DialogTitle
                  as="h3"
                  class="flex items-center bg-gray-50 px-6 py-2 text-2xl text-xl font-semibold leading-6 text-gray-700"
                >
                  <span class="rounded-full border border-gray-300 p-2">
                    <UserIcon class="h-6 w-6 text-blue-500" />
                  </span>
                  <h4 class="pl-3">
                    {{ $t('manager.patient-details') }}
                  </h4>
                </DialogTitle>
                <button
                  type="button"
                  @click="closeModal"
                  class="rounded p-1.5 text-sm text-gray-500 hover:bg-gray-100 hover:text-blue-500"
                >
                  <XIcon @click="closeModal" class="flex h-6 w-6 justify-end" />
                </button>
              </div>
              <div class="flex-grow overflow-y-auto">
                <div>
                  <PatientDetails :id="props.patient.id" no-menubar />
                </div>
              </div>
            </DialogPanel>
          </div>
        </div>
      </TransitionChild>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref } from 'vue'
import { XIcon, UserIcon } from '@heroicons/vue/outline'
import { TransitionRoot, TransitionChild, Dialog, DialogOverlay, DialogPanel, DialogTitle } from '@headlessui/vue'
import PatientDetails from '@/views/pages/PatientDetails.vue'
const emit = defineEmits(['on-close'])

const props = defineProps({
  patient: {
    type: Object,
    default: null,
  },
  isOpen: {
    type: Boolean,
    default: false,
  },
})

function closeModal() {
  emit('on-close')
}
</script>
