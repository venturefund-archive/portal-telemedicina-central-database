<template>
  <div>
    <div class="relative inline-block text-left">
      <button
        type="button"
        class="flex items-center space-x-5 rounded-lg bg-green-500 px-3 py-2 text-sm font-medium text-white hover:bg-green-600"
        @click="dropdownOpen = !dropdownOpen"
      >
        <PlusCircleIcon class="h-6 w-6" />
        <span class="uppercase tracking-wide">{{ $t('patient-details.add-vaccine') }}</span>
      </button>

      <div
        v-show="dropdownOpen"
        class="absolute inset-x-0 mt-2 w-56 rounded-lg bg-white shadow-lg ring-1 ring-black ring-opacity-5"
      >
        <div class="flex flex-col py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
          <div>
            <a
              href="#"
              class="block w-full px-4 py-2 text-center text-sm text-gray-700 hover:bg-white hover:text-gray-900"
              role="menuitem"
              @click="openModal"
              >{{ $t('patient-details.manually-include') }}</a
            >
            <a
              href="#"
              class="block hidden w-full px-4 py-2 text-center text-sm text-gray-700 hover:bg-white hover:text-gray-900"
              role="menuitem"
              @click="openModal2"
              >{{ $t('patient-details.send-booklet') }}</a
            >
          </div>
        </div>
      </div>
    </div>
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
                <div class="border border-transparent bg-blue-500 px-4 py-3">
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
                        class="absolute right-2 ml-auto inline-flex items-center rounded bg-transparent p-1.5 text-sm text-white hover:bg-blue-600 hover:text-white"
                      >
                        <XIcon @click="closeModal" class="flex h-5 w-5 justify-end hover:cursor-pointer" />
                      </button>
                    </div>
                  </DialogTitle>
                </div>
                <form class="w-full max-w-lg" @submit.prevent="submit">
                  <Input type="hidden" name="patient_id" v-model="doseForm.patient_id" />

                  <div class="m-5 rounded-2xl border border-gray-200 bg-white bg-white p-6">
                    <div class="mb-4 flex">
                      <div class="flex-1">
                        <label class="block px-4 py-2 text-sm font-medium text-gray-700" for="vacina">{{
                          $t('patient-details.vaccine')
                        }}</label>
                        <select
                          id="vacina"
                          name="vaccine_id"
                          v-model="doseForm.vaccine_id"
                          required
                          class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 focus:border-green-500 focus:ring-0"
                        >
                          <option v-for="vaccine in filteredVaccines" :key="vaccine.id" :value="vaccine.id">
                            {{ vaccine.display }}: {{ vaccine.description }}
                          </option>
                        </select>

                        <div class="flex-1" v-if="doseForm.vaccine_id">
                          <label class="block px-4 py-2 text-sm font-medium text-gray-700" for="dose">{{
                            $t('patient-details.dose')
                          }}</label>

                          <select
                            id="dose"
                            name="vaccine_dose"
                            v-model="doseForm.vaccine_dose"
                            required
                            class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 focus:border-green-500 focus:ring-0"
                          >
                            <option
                              v-for="dose in filteredDosesByVaccine({ id: doseForm.vaccine_id })"
                              :key="dose.id"
                              :value="dose.id"
                            >
                              {{ dose.dose_order }}° {{ $t('patient-details.dose') }}
                            </option>
                          </select>
                        </div>
                      </div>
                    </div>

                    <div class="mb-4 flex">
                      <div class="flex-1">
                        <label class="block px-4 py-2 text-sm font-medium text-gray-700" for="batch">{{
                          $t('patient-details.batch')
                        }}</label>
                        <Input
                          id="batch"
                          type="text"
                          v-model="doseForm.batch"
                          class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2"
                        />
                      </div>
                    </div>

                    <div class="mb-4 flex">
                      <div class="flex-1 pr-6">
                        <label class="block px-4 py-2 text-sm font-medium text-gray-700" for="cns_number">CNS</label>
                        <Input
                          id="cns_number"
                          type="text"
                          v-model="doseForm.health_professional.cns_number"
                          required
                          class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2"
                        />
                      </div>
                      <div class="flex-1">
                        <label class="block px-4 py-2 text-sm font-medium text-gray-700" for="cnes_number">CNES</label>
                        <Input
                          id="cnes_number"
                          type="text"
                          v-model="doseForm.health_professional.cnes_number"
                          class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2"
                        />
                      </div>
                    </div>

                    <div class="mb-4 flex">
                      <div class="flex-1">
                        <label class="block px-4 py-2 text-sm font-medium text-gray-700" for="health_professional">{{
                          $t('patient-details.profissional')
                        }}</label>
                        <Input
                          id="health_professional"
                          type="text"
                          v-model="doseForm.health_professional.name"
                          required
                          class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2"
                        />
                      </div>
                    </div>

                    <div class="mb-4 flex">
                      <div class="flex-1 pr-6">
                        <label class="block px-4 py-2 text-sm font-medium text-gray-700" for="data-application">
                          {{ $t('patient-details.dose-application-date') }}
                        </label>
                        <Input
                          type="date"
                          id="data_application"
                          required
                          class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2"
                          v-model="doseForm.application_date"
                        />
                      </div>
                      <div class="flex-1">
                        <label class="block px-4 py-2 text-sm font-medium text-gray-700" for="next-data-application">
                          {{ $t('patient-details.next-application') }}
                        </label>
                        <Input
                          type="date"
                          id="next_data_application"
                          required
                          v-model="doseForm.next_dose_application_date"
                          class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2"
                        />
                      </div>
                    </div>
                  </div>

                  <div class="flex items-center justify-center" v-if="!['local', 'production'].includes(node_env)">
                    <span class="ml-10 flex cursor-pointer items-center" @click="openModal2">
                      <CloudUploadIcon class="mr-6 h-6 w-6 text-blue-500" />
                      <span class="text-sm font-semibold text-blue-500">{{ $t('patient-details.uploadbooklet') }}</span>
                    </span>

                    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center">
                      <div class=""></div>
                      <div class="rounded bg-blue-500 p-4 shadow-2xl" style="height: 250px">
                        <div class="flex justify-between">
                          <CloudUploadIcon class="h-7 w-7 text-white" />
                          <h3 class="text-lg font-medium text-white" v-if="!['local', 'production'].includes(node_env)">
                            {{ $t('patient-details.sendbooklet') }}
                          </h3>
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
                          <Input type="file" id="fotoVacina" name="fotoVacina" class="my-3 flex w-full" @click.stop />
                        </div>
                        <div class="flex justify-end pt-3">
                          <button
                            type="button"
                            class="mr-3 inline-flex justify-center rounded-lg bg-[#F3F3F3] px-12 py-2 text-xs font-medium uppercase tracking-wide text-blue-500 shadow-lg hover:bg-gray-200"
                          >
                            {{ $t('patient-details.send') }}
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="flex justify-end p-10 pt-20">
                    <Button type="button" variant="success-outline" @click="closeModal" class="mr-3">
                      {{ $t('patient-details.cancel') }}
                    </Button>
                    <Button variant="success" type="submit">
                      {{ $t('patient-details.send') }}
                    </Button>
                  </div>
                </form>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>
<script setup>
import { ref, watch, computed, reactive } from 'vue'
import { PlusCircleIcon, SearchIcon, XIcon } from '@heroicons/vue/outline'
import { CloudUploadIcon } from '@heroicons/vue/solid'
import { usePatientsStore } from '@/stores/patients'
import { useDosesStore } from '@/stores/doses'
import { useVaccinesStore } from '@/stores/vaccines'
import { useLoggedUserStore } from '@/stores/loggedUser'
import { TransitionRoot, TransitionChild, Dialog, DialogPanel, DialogTitle } from '@headlessui/vue'
import { parseISO, formatRelative, formatDuration, add, setDefaultOptions, differenceInMonths, format } from 'date-fns'
import { errorToast, successToast } from '@/toast'

const node_env = ref(import.meta.env.NODE_ENV)
const patientsStore = usePatientsStore()
const dosesStore = useDosesStore()
const vaccinesStore = useVaccinesStore()

const filteredVaccines = computed(() => {
  return vaccinesStore.items.filter((vaccine) => {
    return vaccine.system == 'BRI' && dosesStore.items.map((e) => e.vaccine).includes(vaccine.id)
  })
})
const dropdownOpen = ref(false)
const filteredDosesByVaccine = computed(() => {
  return (vaccine) =>
    dosesStore.items.filter((dose) => {
      return dose.vaccine == vaccine.id
    })

  //const orderedDoses = filteredDoses.sort((a, b) => {
  //  return b.order - a.order;
  //})
  //return orderedDoses;
})

const doseForm = ref({
  patient_id: patientsStore.item.id,
  vaccine_id: null,
  vaccine_dose: null,
  health_professional: {
    name: '',
    cns_number: '',
    cnes_number: '',
  },
  batch: '',
  application_date: '',
  next_dose_application_date: '',
  fhir_store: 1,
  completed: true,
  processing: false,
})

const doseApplicationDate = computed(() => parseISO(doseForm.value.application_date))
const nextDoseApplicationDate = computed(() => parseISO(doseForm.value.next_dose_application_date))

const vaccine = ref(null)
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

const emit = defineEmits(['saved'])

const submit = async () => {
  try {
    await dosesStore.addVaccine(doseForm.value)
    successToast({ text: 'Dose cadastrada com sucesso!' })
    emit('saved', dosesStore.item)
  } catch (err) {
    errorToast({ text: err.response.data.detail })
    console.log(err)
  }
  closeModal()
}
</script>
