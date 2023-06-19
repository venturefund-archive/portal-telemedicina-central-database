<template>
  <div>
    <button
      type="button"
      @click="openModal"
      class="flex items-center space-x-5 rounded-full bg-blue-500 py-2 px-3 text-sm font-medium text-white hover:bg-blue-600"
    >
      <PlusCircleIcon class="h-6 w-6" />
      <span class="uppercase tracking-wide">{{ $t('patient-details.add-vaccine') }}</span>
    </button>
    <TransitionRoot appear :show="isOpen" as="template">
      <Dialog as="div" @close="closeModal" class="relative z-10">
        <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black bg-opacity-25" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel
                class="transform overflow-hidden rounded bg-[#F8F9FB] text-left align-middle shadow-xl transition-all"
              >
                <div class="border border-transparent border-b-gray-500 bg-blue-500 p-6">
                  <DialogTitle as="h3" class="flex justify-between text-lg font-medium leading-6 text-gray-900">
                    <div class="flex items-center">
                      <div class="rounded-full bg-white p-2">
                        <img class="h-7 w-7" src="@/assets/images/profile-menu-02.png" />
                      </div>
                      <span class="ml-2 text-white">{{ $t('patient-details.add-vaccine') }}</span>
                    </div>
                    <div class="relative rounded-lg bg-white shadow">
                      <button
                        type="button"
                        @click="closeModal"
                        class="absolute right-2 ml-auto inline-flex items-center rounded bg-transparent p-1.5 text-sm text-white"
                      >
                        <XIcon @click="closeModal" class="flex h-5 w-5 justify-end hover:cursor-pointer" />
                      </button>
                    </div>
                  </DialogTitle>
                </div>
                <div class="m-5 rounded-2xl border border-gray-50 bg-white p-6 shadow-lg">
                  <form class="w-full max-w-md">
                    <div class="mb-4 flex items-center">
                      <div class="mr-6 w-1/2">
                        <label class="text-sm" for="vacina">{{ $t('patient-details.vaccine') }}</label>
                        <input
                          type="text"
                          id="vacina"
                          name="vacina"
                          required
                          class="w-full rounded-full border-none bg-gray-100 py-2 px-4"
                        />
                      </div>
                      <div class="w-1/2">
                        <label class="text-sm" for="dose">{{ $t('patient-details.dose') }}</label>
                        <select
                          id="dose"
                          name="dose"
                          required
                          class="w-full rounded-full border-none bg-gray-100 py-2 px-4"
                        >
                          <option value="">{{ $t('patient-details.select') }}...</option>
                          <option value="1">1° {{ $t('patient-details.dose') }}</option>
                          <option value="2">2º {{ $t('patient-details.dose') }}</option>
                          <option value="3">3° {{ $t('patient-details.dose') }}</option>
                          <option value="única">{{ $t('patient-details.single-dose') }}</option>
                        </select>
                      </div>
                    </div>

                    <div class="mb-4 flex items-center">
                      <div class="mr-6 w-1/2">
                        <label class="text-sm" for="unidade">{{ $t('patient-details.unity') }}</label>
                        <input
                          type="text"
                          id="unidade"
                          name="unidade"
                          required
                          class="w-full rounded-full border-none bg-gray-100 py-2 px-4"
                        />
                      </div>
                      <div class="w-1/2">
                        <label class="text-sm" for="cnes">CNES</label>
                        <input
                          type="text"
                          id="cnes"
                          name="cnes"
                          required
                          class="w-full rounded-full border-none bg-gray-100 py-2 px-4"
                        />
                      </div>
                    </div>
                    <div class="mb-4 flex items-center">
                      <div class="mr-6 w-1/2">
                        <label class="text-sm" for="data">{{ $t('patient-details.date') }}</label>
                        <input
                          type="date"
                          id="data"
                          name="data"
                          required
                          class="w-full rounded-full border-none bg-gray-100 py-2 px-4"
                        />
                      </div>
                      <div class="w-1/2">
                        <label class="text-sm" for="lote">{{ $t('patient-details.batch') }}</label>
                        <input
                          type="text"
                          id="lote"
                          name="lote"
                          required
                          class="w-full rounded-full border-none bg-gray-100 py-2 px-4"
                        />
                      </div>
                    </div>
                    <div class="mb-4">
                      <label class="text-sm" for="fabricante">{{ $t('patient-details.manufacturer') }}</label>
                      <input
                        type="text"
                        id="fabricante"
                        name="fabricante"
                        required
                        class="w-full rounded-full border-none bg-gray-100 py-2 px-4"
                      />
                    </div>

                    <div class="mb-4">
                      <label class="text-sm" for="vacinador">{{ $t('patient-details.vaccinator') }}</label>
                      <input
                        type="text"
                        id="vacinador"
                        name="vacinador"
                        required
                        class="w-full rounded-full border-none bg-gray-100 py-2 px-4"
                      />
                    </div>

                    <div class="mb-4">
                      <label class="text-sm" for="profissional">{{ $t('patient-details.profissional') }}</label>
                      <input
                        type="text"
                        id="profissional"
                        name="profissional"
                        required
                        class="w-full rounded-full border-none bg-gray-100 py-2 px-4"
                      />
                    </div>
                  </form>
                </div>
                <div>
                  <span class="ml-10 flex cursor-pointer items-center" @click="openModal2">
                    <CloudUploadIcon class="mr-6 h-6 w-6 text-blue-500" />
                    <span class="text-sm font-semibold text-blue-500">{{ $t('patient-details.uploadbooklet') }}</span>
                  </span>

                  <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center">
                    <div class=""></div>
                    <div class="rounded bg-blue-500 p-4 shadow-2xl" style="height: 250px">
                      <div class="flex justify-between">
                        <CloudUploadIcon class="h-7 w-7 text-white" />
                        <h3 class="text-lg font-medium text-white">{{ $t('patient-details.sendbooklet') }}</h3>
                        <div class="flex justify-end">
                          <button
                            type="button"
                            @click="closeModal2"
                            class="right-2 ml-auto inline-flex items-center rounded bg-transparent p-1.5 text-sm text-white"
                          >
                            <XIcon @click="closeModal2" class="flex h-5 w-5 justify-end hover:cursor-pointer" />
                          </button>
                        </div>
                      </div>
                      <hr class="my-4 border-white" />
                      <div class="rounded-lg bg-white p-4" style="height: 100px">
                        <input type="file" id="fotoVacina" name="fotoVacina" class="my-3 flex w-full" @click.stop />
                      </div>
                      <div class="flex justify-end pt-3">
                        <button
                          type="button"
                          class="mr-3 inline-flex justify-center rounded-full bg-[#F3F3F3] px-12 py-2 text-xs font-medium uppercase tracking-wide text-blue-500 shadow-lg hover:bg-gray-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                        >
                          {{ $t('patient-details.send') }}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="flex justify-end p-10 pt-20">
                  <button
                    type="button"
                    class="mr-3 inline-flex justify-center rounded-full border border-transparent bg-[#F3F3F3] px-12 py-2 text-xs font-medium uppercase tracking-wide text-blue-500 shadow-lg hover:bg-gray-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                    @click="closeModal"
                  >
                    {{ $t('patient-details.cancel') }}
                  </button>
                  <button
                    type="button"
                    class="inline-flex justify-center rounded-full border border-transparent bg-blue-500 px-12 py-2 text-xs font-medium uppercase tracking-wide text-white shadow-lg hover:bg-blue-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  >
                    {{ $t('patient-details.send') }}
                  </button>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>
<script setup>
import { ref, watch } from 'vue'
import { PlusCircleIcon, SearchIcon, XIcon } from '@heroicons/vue/outline'
import { CloudUploadIcon } from '@heroicons/vue/solid'
import { usePatientsStore } from '@/stores/patients'
import { useDosesStore } from '@/stores/doses'
import { useVaccinesStore } from '@/stores/vaccines'
import { useLoggedUserStore } from '@/stores/loggedUser'
import { TransitionRoot, TransitionChild, Dialog, DialogPanel, DialogTitle } from '@headlessui/vue'

const isModalOpen = ref(false)

function openModal2() {
  isModalOpen.value = true
}

function closeModal2() {
  isModalOpen.value = false
}
const isOpen = ref(false)

function openModal() {
  isOpen.value = true
}

function closeModal() {
  isOpen.value = false
}
</script>
