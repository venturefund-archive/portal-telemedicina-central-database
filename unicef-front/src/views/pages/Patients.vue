<template>
  <PageWrapper title="Patients">
    {{isOpen}}
    <div class="flex">
      <Dialog :open="isOpen" @close="setIsOpen">
        <DialogPanel>
          <DialogTitle>Edit Vaccine</DialogTitle>
          <DialogDescription>
            This will vaccine
          </DialogDescription>

          <p>
            Are you sure you want to vaccine?
          </p>

          <button @click="setIsOpen(false)">Yes</button>
          <button @click="setIsOpen(false)">Cancel</button>
        </DialogPanel>
      </Dialog>

      <aside class="w-64" aria-label="Sidebar">
        <div class="overflow-y-auto rounded border border-neutral-100 px-3 py-4 dark:bg-gray-800 decoration-none bg-gray-50 shadow-l-md">
          <ul class="space-y-2">
            <li>
              <a
                href="#"
                class="flex items-center rounded-lg p-2 text-base font-normal text-gray-900 hover:bg-neutral-200"
              >
                <span class="ml-3">Peso, altura, IMC</span>
              </a>
            </li>
            <li>
              <a
                href="#"
                target="_blank"
                class="flex items-center rounded-lg p-2 text-base font-normal text-blue-600 hover:bg-neutral-200"
              >
                <span class="ml-3 flex-1 whitespace-nowrap">Cartilha de Vacinas</span>
              </a>
            </li>
            <li>
              <a
                href="#"
                target="_blank"
                class="flex items-center rounded-lg p-2 text-base font-normal text-gray-900 hover:bg-neutral-200"
              >
                <span class="ml-3 flex-1 whitespace-nowrap">Período fetal</span>
              </a>
            </li>
            <li>
              <a
                href="#"
                class="flex items-center rounded-lg p-2 text-base font-normal text-gray-900 hover:bg-neutral-200"
              >
                <span class="ml-3 flex-1 whitespace-nowrap">Alergias</span>
              </a>
            </li>
            <li>
              <a
                href="#"
                class="flex items-center rounded-lg p-2 text-base font-normal text-gray-900 hover:bg-neutral-200"
              >
                <span class="ml-3 flex-1 whitespace-nowrap">Medicamentos</span>
              </a>
            </li>
            <li>
              <a
                href="#"
                class="flex items-center rounded-lg p-2 text-base font-normal text-gray-900 hover:bg-neutral-200"
              >
                <span class="ml-3 flex-1 whitespace-nowrap">Doenças</span>
              </a>
            </li>
            <li>
              <a
                href="#"
                class="flex items-center rounded-lg p-2 text-base font-normal text-gray-900 hover:bg-neutral-200"
              >
                <span class="ml-3 flex-1 whitespace-nowrap">Dados socioculturais</span>
              </a>
            </li>
          </ul>
        </div>
      </aside>

      <div>
        <ProfileCard />
        <VaccinesList />
      </div>
    </div>
  </PageWrapper>
</template>

}
<script setup>
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import { DotsVerticalIcon, PlusCircleIcon, MinusCircleIcon } from '@heroicons/vue/outline'
import {
    Dialog,
    DialogPanel,
    DialogTitle,
    DialogDescription,
  } from '@headlessui/vue'

const isOpen = ref(true)

function setIsOpen(value) {
  console.log('hit')
  isOpen.value = value
}
</script>
