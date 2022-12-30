<template>
  <div class="flex flex-col">
    <div class="px-3 py-2 sm:-mx-6 lg:-mx-5">
      <div class="inline-block min-w-full sm:px-6 lg:px-8">
        <div class="flex justify-end py-3">
          <div class="flex items-center rounded-md bg-neutral-200 px-3 py-2 text-neutral-500">
            <span class="flex items-center px-2">Completo: <VaccineAlert :status="1" class="scale-75 pl-2 pl-2" /></span>
            <span class="flex items-center px-2">Alerta: <VaccineAlert :status="3" class="scale-75 pl-2 pl-2" /></span>
            <span class="flex items-center px-2">Recomendado: <VaccineAlert :status="4" class="scale-75 pl-2 pl-2" /></span>
          </div>
        </div>
        <table class="w-full table-fixed rounded bg-neutral-50 text-left text-sm shadow-lg">
          <thead class="bg-neutral-200 text-xs uppercase text-white">
            <tr>
              <th scope="col" colspan="2" class="bg-blue-200 px-6 py-4 text-center text-gray-900">Vacinas</th>
              <th scope="col" colspan="9" class="bg-blue-300 px-6 py-4 text-center">
                <span class="rounded-t-xl border border-transparent bg-neutral-500 p-2 font-semibold text-white"
                  >Meses</span
                >
              </th>
              <th scope="col" colspan="4" class="bg-blue-400 px-6 py-4 text-center text-gray-900">
                <span class="rounded-t-xl border border-transparent bg-neutral-500 p-2 font-semibold text-white"
                  >Anos</span
                >
              </th>
            </tr>
            <tr class="text-center">
              <th scope="col" colspan="2" class="pt-2 text-gray-900">
                <InputIconWrapper>
                  <template #icon>
                    <SearchIcon aria-hidden="true" class="h-5 w-5" />
                  </template>
                  <Input
                    v-model="vaccineQuery"
                    withIcon
                    placeholder="Pesquisar vacinas"
                    class="mx-auto flex rounded-md bg-gray-50 p-2 text-sm font-normal sm:w-20 lg:w-48"
                  />
                </InputIconWrapper>
                <div class="py-0.6 py-3 text-center font-normal lowercase text-neutral-500">
                  <span v-if="vaccineQuery"> {{ filteredVaccines.length }} resultados </span>
                  <span v-else>{{ filteredVaccines.length }} Total de vacinas</span>
                </div>
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[0]) }"
                class="px-6 py-4 text-gray-900"
              >
                0 a 2
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[1]) }"
                class="px-6 py-4 text-gray-900"
              >
                3
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[2]) }"
                class="px-6 py-4 text-gray-900"
              >
                4
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[3]) }"
                class="px-6 py-4 text-gray-900"
              >
                5
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[4]) }"
                class="px-6 py-4 text-gray-900"
              >
                6
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[5]) }"
                class="px-6 py-4 text-gray-900"
              >
                7 a 11
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[6]) }"
                class="px-6 py-4 text-gray-900"
              >
                12
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[7]) }"
                class="px-6 py-4 text-gray-900"
              >
                15
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[8]) }"
                class="px-6 py-4 text-gray-900"
              >
                18
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[9]) }"
                class="px-6 py-4 text-gray-900"
              >
                1 a 5
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[10]) }"
                class="px-6 py-4 text-gray-900"
              >
                5 a 10
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[11]) }"
                class="px-6 py-4 text-gray-900"
              >
                10 a 12
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[12]) }"
                class="px-6 py-4 text-gray-900"
              >
                12 a 15
              </th>
            </tr>
          </thead>
          <tbody>
            <tr class="table-row border-b hover:bg-neutral-200" v-for="(vaccine, k) in filteredVaccines" :key="k">
              <td colspan="2" class="truncate whitespace-nowrap px-6 py-4 text-sm font-medium capitalize text-gray-900">
                {{ vaccine.display }} {{ vaccine.description }}
              </td>
              <td
                :class="{
                  'col-birth box-border border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[rangeIndex]),
                }"
                class="whitespace-nowrap px-6 py-4 text-sm font-light text-gray-900"
                v-for="(range, rangeIndex) in ranges"
                :key="rangeIndex"
              >

                <div v-for="(dose, dk) in filteredDosesByVaccine(vaccine)" :key="dk" class="text-center">


                  <VaccineAlert v-if="
                      dose.is_completed &&
                      null != dose.maximum_recommended_age &&
                      isWithinInterval(add(birthDate, { months: dose.maximum_recommended_age }), {
                        start: range.start,
                        end: range.end,
                      })
                    "
                    :rangeIndex="rangeIndex"
                    :status="1"
                  >
                    <VaccineAlertInfo :vaccine="vaccine" :dose="dose" />
                  </VaccineAlert>

                  <div v-else-if="dose.alerts.length > 0" v-for="(alert, ak) in dose.alerts" :key="ak">
                    <VaccineAlert
                      :rangeIndex="rangeIndex"
                      :status="2"
                      v-if="
                        null != dose.maximum_recommended_age &&
                        isWithinInterval(add(birthDate, { months: dose.maximum_recommended_age }), {
                          start: range.start,
                          end: range.end,
                        })
                      "
                    >
                      <VaccineAlertInfo :vaccine="vaccine" :dose="dose" />
                    </VaccineAlert>
                  </div>

                  <VaccineAlert
                      :rangeIndex="rangeIndex"
                      :status="4"
                      v-else-if="
                        dose.alerts.length == 0 &&
                        null != dose.maximum_recommended_age &&
                        (Math.floor(dose.minimum_recommended_age/13) >= rangeIndex +1 || Math.floor(dose.maximum_recommended_age/13) <= rangeIndex +1) &&
                        isWithinInterval(add(birthDate, { months: dose.maximum_recommended_age }), {
                          start: range.start,
                          end: range.end,
                        })">
                      <VaccineAlertInfo :vaccine="vaccine" :dose="dose" />
                    </VaccineAlert>


                </div>

              </td>
            </tr>
          </tbody>
        </table>
        <div class="py-3 text-neutral-500">
          <span v-if="vaccineQuery">
            Pesquisa por "{{ vaccineQuery }}" retornou {{ filteredVaccines.length }} vacinas.
          </span>
          <span v-else>{{ filteredVaccines.length }} Total de vacinas</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { MailIcon, LockClosedIcon, LoginIcon, UserIcon, SearchIcon, ChevronDownIcon } from '@heroicons/vue/outline'
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'
import { computed } from 'vue'
import {
  formatDistance,
  parseISO,
  formatISO9075,
  add,
  isWithinInterval,
  differenceInMonths,
  differenceInDays,
  subDays,
} from 'date-fns'
import { usePatientsStore } from '@/stores/patients'
import { useDosesStore } from '@/stores/doses'
import { useVaccinesStore } from '@/stores/vaccines'
import VaccineAlert from '../atoms/VaccineAlert.vue'
const patientsStore = usePatientsStore()
const dosesStore = useDosesStore()
const vaccinesStore = useVaccinesStore()

const router = useRouter()

const birthDate = computed(() => parseISO(patientsStore.item.birth_date))
//const birthDateInMonthsFromNow = computed(() => differenceInMonths(birthDate, new Date()) )

const vaccineQuery = ref('')
const filteredVaccines = computed(() => {
  return vaccinesStore.items.filter((vaccine) => {
    return (
      vaccine.system == 'BRI' &&
      (vaccine.description.toLowerCase().includes(vaccineQuery.value.toLowerCase()) ||
        vaccine.display.toLowerCase().includes(vaccineQuery.value.toLowerCase()))
    )
  })
})
const selectedVaccine = ref(filteredVaccines.value[0])

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

const key = ref(0)

const ranges = computed(() => [
  { start: birthDate.value, end: add(birthDate.value, { months: 2 }) }, //ao nascer
  { start: add(birthDate.value, { months: 2, seconds: 1 }), end: add(birthDate.value, { months: 3 }) },
  { start: add(birthDate.value, { months: 3, seconds: 1 }), end: add(birthDate.value, { months: 4 }) },
  { start: add(birthDate.value, { months: 4, seconds: 1 }), end: add(birthDate.value, { months: 5 }) },
  { start: add(birthDate.value, { months: 5, seconds: 1 }), end: add(birthDate.value, { months: 6 }) },

  { start: add(birthDate.value, { months: 6, seconds: 1 }), end: add(birthDate.value, { months: 11 }) },
  { start: add(birthDate.value, { months: 11, seconds: 1 }), end: add(birthDate.value, { months: 12 }) },
  { start: add(birthDate.value, { months: 12, seconds: 1 }), end: add(birthDate.value, { months: 15 }) },

  { start: add(birthDate.value, { months: 15, seconds: 1 }), end: add(birthDate.value, { months: 18 }) },

  { start: add(birthDate.value, { months: 18, seconds: 1 }), end: add(birthDate.value, { years: 6 }) },
  { start: add(birthDate.value, { years: 6, seconds: 1 }), end: add(birthDate.value, { years: 10 }) },
  { start: add(birthDate.value, { years: 10, seconds: 1 }), end: add(birthDate.value, { years: 12 }) },
  { start: add(birthDate.value, { years: 12, seconds: 1 }), end: add(birthDate.value, { years: 15 }) },
])

const addDose = () => {
  return console.log('dose adicionada')
}

const props = defineProps({
  id: {
    type: String,
    default: '0',
  },
})

watch(
  () => props.id,
  async () => {
    await vaccinesStore.fetchVaccines()
  },
  { immediate: true }
)
</script>

<style scoped>
.table-row:hover > td:not(.col-birth) {
  @apply border-none;
}

.table-row td:not(:nth-child(1)):not(.col-birth) {
  @apply border-x;
}
</style>
