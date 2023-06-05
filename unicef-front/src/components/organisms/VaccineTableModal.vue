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
        <div class="relative h-full w-2/3">
          <div class="flex h-full flex-col overflow-y-scroll bg-white shadow-xl">
            <DialogPanel class="flex h-full flex-col bg-[#F8F9FB]">
              <div class="shadow-b-3xl z-10 flex items-start justify-between rounded-t bg-gray-50 p-2 shadow-md">
                <DialogTitle
                  as="h3"
                  class="flex items-center bg-gray-50 py-5 px-6 text-2xl text-xl font-semibold leading-6 text-gray-700"
                >
                  <UserGroupIcon class="mr-2 h-7 w-7 text-green-500" />
                  {{ $t('manager.details') }}
                </DialogTitle>
                <button
                  type="button"
                  @click="closeModal"
                  class="rounded bg-white p-1.5 text-sm text-gray-500 hover:text-green-500"
                >
                  <XIcon @click="closeModal" class="flex h-8 w-8 justify-end" />
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
import { XIcon, UserGroupIcon } from '@heroicons/vue/outline'
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
