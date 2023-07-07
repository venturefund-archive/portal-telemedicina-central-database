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
              <div class="z-10 flex items-start justify-between rounded-t bg-gray-50 p-2 shadow-md">
                <DialogTitle
                  as="h3"
                  class="flex items-center bg-gray-50 py-5 px-6 text-2xl text-xl font-semibold leading-6 text-gray-700"
                >
                  <UserGroupIcon class="mr-2 h-7 w-7 text-green-500" />
                  {{ $t('editPatient.details') }}
                </DialogTitle>
                <button type="button" @click="closeModal" class="p-1.5 text-sm text-gray-500 hover:text-green-500">
                  <XIcon @click="closeModal" class="flex h-6 w-6 justify-end" />
                </button>
              </div>
              <div class="flex-grow overflow-y-auto p-4">
                <!-- Include form inputs for editing patient details here -->
                <div>
                  <!-- Example input for patient name -->
                  <label for="patientName" class="block text-sm font-medium text-gray-700">Name</label>
                  <input type="text" id="patientName" v-model="editedPatient.name" class="mt-1 block w-full p-2" />
                </div>

                <button @click="saveChanges" class="mt-4 rounded bg-green-500 p-2 text-white">Save Changes</button>
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

const emit = defineEmits(['on-close', 'on-saved'])

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

const editedPatient = ref({ ...props.patient })

function closeModal() {
  emit('on-close')
}

function saveChanges() {
  emit('on-saved', editedPatient.value)
  closeModal()
}
</script>
