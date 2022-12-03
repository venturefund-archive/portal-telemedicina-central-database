<template>
  <div>
    <!-- Main modal -->
    <div
      v-if="isOpen"
      id="authentication-modal"
      tabindex="-1"
      aria-hidden="true"
      class="fixed top-0 right-0 left-0 bottom-0 mx-auto z-50 h-modal w-full overflow-y-auto overflow-x-hidden p-4 md:inset-0 md:h-full"
    >
      <div class="relative h-full w-full max-w-md md:h-auto">
        <!-- Modal content -->
        <div class="relative rounded-lg bg-white shadow dark:bg-gray-700">
          <button
            type="button"
            @click="closeModal"
            class="absolute top-3 right-2.5 ml-auto inline-flex items-center rounded-lg bg-transparent p-1.5 text-sm text-gray-400 hover:bg-gray-200 hover:text-gray-900 dark:hover:bg-gray-800 dark:hover:text-white"
          >
            <svg
              aria-hidden="true"
              class="h-5 w-5"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill-rule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clip-rule="evenodd"
              ></path>
            </svg>
            <span class="sr-only">Close modal</span>
          </button>
          <div class="py-6 px-6 lg:px-8">
            <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Vacina: BCGI</h3>
            <form class="space-y-6" action="#">
                <div class="flex">
                <div class="px-2">
              <!-- Se for uma dose que esta faltando, ao clicar no checkbox, some o formulário -->
              <div>
                <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">Dose</label>
                <input
                  class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-500 dark:bg-gray-600 dark:text-white dark:placeholder-gray-400"
                />
              </div>

              <div>
                <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">CNES</label>
                <input
                  class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-500 dark:bg-gray-600 dark:text-white dark:placeholder-gray-400"
                />
              </div>
              <div>
                <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">Data</label>
                <input
                  class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-500 dark:bg-gray-600 dark:text-white dark:placeholder-gray-400"
                />
              </div>
              <div>
                <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">Lote</label>
                <input
                  class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-500 dark:bg-gray-600 dark:text-white dark:placeholder-gray-400"
                />
              </div>
            </div>

            <div class="px-2">
              <div>
                <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">Fabricante</label>
                <input
                  class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-500 dark:bg-gray-600 dark:text-white dark:placeholder-gray-400"
                />
              </div>
              <div>
                <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">Vacinador</label>
                <input
                  class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-500 dark:bg-gray-600 dark:text-white dark:placeholder-gray-400"
                />
              </div>
              <div>
                <label class="mb-2 block text-sm font-medium text-gray-900 dark:text-white"
                  >Registro do profissional</label
                >
                <input
                  class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-500 dark:bg-gray-600 dark:text-white dark:placeholder-gray-400"
                />
              </div>
            </div>
            </div>
            <button
                type="submit"
                class="w-full rounded-lg bg-blue-700 px-5 py-2.5 text-center text-sm font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
              >
                Adicionar Vacina
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { DotsHorizontalIcon } from '@heroicons/vue/outline'
import { ref, watch, defineExpose } from 'vue'

const isOpen = ref(false)

const closeModal = function () {
  isOpen.value = false
}
const openModal = function () {
  isOpen.value = true
}

defineExpose({
  openModal,
  closeModal,
})
</script>
