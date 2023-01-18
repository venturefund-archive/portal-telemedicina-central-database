<template>
  <transition name="fade" mode="out-in">
  <div class="flex justify-center h-96" v-if="loggedUserStore.isLoading || vaccinesStore.items.length == 0" >
    <svg class="animate-spin text-blue-600 -ml-1 mr-3 w-20 w-20 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
  </div>
  <div class="flex flex-col" v-else>
    <div class="flex flex-col sm:flex-row justify-between px-2">
      <ProfileCard :id="id" class="sm:w-2/3 md:w-fu" />
      <div class="flex pl-2 justify-end">
        <div class="flex place-items-end pt-5 md:mt-0">
          <div class="flex flex-col items-end md:flex-row md:items-center rounded-md bg-neutral-200 px-3 py-2 text-neutral-500">
            <span class="flex items-center px-2">Completo: <VaccineAlert :status="1" class="scale-75 pl-2 pl-2" /></span>
            <span class="flex items-center px-2">Alerta: <VaccineAlert :status="3" class="scale-75 pl-2 pl-2" /></span>
            <span class="flex items-center px-2">Recomendado: <VaccineAlert :status="4" class="scale-75 pl-2 pl-2" /></span>
          </div>
        </div>
      </div>
    </div>
    <div class="py-2">
      <div class="overflow-auto px-2 pt-2 pb-52">
        <table class="table-auto md:table-fixed lg:table-fixed w-full bg-neutral-50 text-left rounded-md shadow tracking-wider">
          <thead class="bg-neutral-200 text-white">
            <tr>
              <th scope="col" colspan="2" class="bg-blue-200 px-6 py-4 text-center text-gray-900 uppercase w-80">Vacinas</th>
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
              <th scope="col" colspan="2" class="pt-2 text-gray-900 whitespace-nowrap px-2.5 font-normal">
                <InputIconWrapper>
                  <Input
                    v-model="vaccineQuery"
                    placeholder="Pesquisar vacinas"
                    withIcon
                    class="shadow focus:shadow-none rounded-md bg-gray-50 w-full"
                  />
                </InputIconWrapper>
                <div class="py-0.6 py-3 text-center font-normal text-neutral-500 text-sm">
                  Total de
                  <span v-if="filteredVaccines.length == 1"><span class="font-semibold">{{ filteredVaccines.length }}</span> vacina</span>
                  <span v-else-if="filteredVaccines.length == 0"><span class="font-semibold">{{ filteredVaccines.length }}</span> vacinas</span>
                  <span v-else><span class="font-semibold">{{ filteredVaccines.length }}</span> vacinas</span>
                </div>
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[0]) }"
                class="px-6 py-4 text-gray-900 whitespace-nowrap"
              >
                0 a 2
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[1]) }"
                class="px-6 py-4 text-gray-900 whitespace-nowrap"
              >
                3
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[2]) }"
                class="px-6 py-4 text-gray-900 whitespace-nowrap"
              >
                4
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[3]) }"
                class="px-6 py-4 text-gray-900 whitespace-nowrap"
              >
                5
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[4]) }"
                class="px-6 py-4 text-gray-900 whitespace-nowrap"
              >
                6
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[5]) }"
                class="px-6 py-4 text-gray-900 whitespace-nowrap"
              >
                7 a 11
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[6]) }"
                class="px-6 py-4 text-gray-900 whitespace-nowrap"
              >
                12
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[7]) }"
                class="px-6 py-4 text-gray-900 whitespace-nowrap"
              >
                15
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[8]) }"
                class="px-6 py-4 text-gray-900 whitespace-nowrap"
              >
                18
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[9]) }"
                class="px-6 py-4 text-gray-900 whitespace-nowrap"
              >
                1 a 5
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[10]) }"
                class="px-6 py-4 text-gray-900 whitespace-nowrap"
              >
                5 a 10
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[11]) }"
                class="px-6 py-4 text-gray-900 whitespace-nowrap"
              >
                10 a 12
              </th>
              <th
                scope="col"
                :class="{ 'border-x-2 border-sky-500': isWithinInterval(new Date(), ranges[12]) }"
                class="px-6 py-4 text-gray-900 whitespace-nowrap"
              >
                12 a 15
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr class="hover:bg-neutral-200" v-for="(vaccine, k) in orderedVaccinesByDoseAlerts" :key="k">
              <td colspan="2" class="px-6 py-4 font-medium text-gray-900">
                <span class="">{{ vaccine.display }}</span> <span class="">{{ vaccine.description }}</span>
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
                      <VaccineAlertInfo :vaccine="vaccine" :dose="dose" :withoutDetails="true" />
                    </VaccineAlert>


                </div>

              </td>
            </tr>
          </tbody>
        </table>
        <div class="py-3 text-neutral-400 grid justify-items-end">
          <span>
            Gerado dia {{ format(new Date(), 'dd/MM/yyyy kk:mm') }}
          </span>
        </div>
      </div>
    </div>
  </div>
  </transition>
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
import { formatDistance, format, parseISO, formatISO9075, add, isWithinInterval, differenceInMonths, differenceInDays, subDays, setDefaultOptions } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import { usePatientsStore } from '@/stores/patients'
import { useDosesStore } from '@/stores/doses'
import { useVaccinesStore } from '@/stores/vaccines'
import { useLoggedUserStore } from '@/stores/loggedUser'
import VaccineAlert from '../atoms/VaccineAlert.vue'
const patientsStore = usePatientsStore()
const dosesStore = useDosesStore()
const vaccinesStore = useVaccinesStore()
const loggedUserStore = useLoggedUserStore()
setDefaultOptions({ locale: ptBR })

const router = useRouter()

const birthDate = computed(() => parseISO(patientsStore.item.birth_date))
//const birthDateInMonthsFromNow = computed(() => differenceInMonths(birthDate, new Date()) )

const vaccineQuery = ref('')

const filteredVaccines = computed(() => {
  return vaccinesStore.items.filter((vaccine) => {
    return (
      vaccine.system == 'BRI' &&
      dosesStore.items.map(e => e.vaccine).includes(vaccine.id) &&
      (vaccine.description.toLowerCase().includes(vaccineQuery.value.toLowerCase()) ||
        vaccine.display.toLowerCase().includes(vaccineQuery.value.toLowerCase()))
    )
  })
})
const selectedVaccine = ref(filteredVaccines.value[0])

const totalAlerts = computed(() => {
  return (vaccine) => filteredDosesByVaccine.value(vaccine).map(d => d.alerts.length).reduce((total, current)=>  total + current)
})

const orderedVaccinesByDoseAlerts = computed(() => {
  return filteredVaccines.value.sort((a, b) => totalAlerts.value(b) - totalAlerts.value(a));
});


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
</script>

<style scoped>
.table-row:hover > td:not(.col-birth) {
  @apply border-none;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

</style>
