<template>
  <transition name="fade" mode="out-in">
    <div class="flex h-96 justify-center" v-if="loggedUserStore.isLoading || vaccinesStore.items.length == 0">
      <svg
        class="-ml-1 mr-3 w-20 animate-spin text-blue-500"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        ></path>
      </svg>
    </div>
    <div class="mt-16 flex bg-[#F8F9FB]" v-else>
      <div class="p-8">
        <ProfileCard :id="id" class="mt-10" />
      </div>

      <div class="-mt-16 flex flex-col pt-20">
        <nav class="flex" aria-label="Breadcrumb">
          <ol class="inline-flex items-center space-x-1 md:space-x-3">
            <li>
              <div class="flex items-center">
                <router-link class="ml-1 text-gray-500 hover:text-blue-600" to="/patients">{{
                  $t('patient-details.search-patients')
                }}</router-link>
                <!-- <a href="#" class="ml-1  text-gray-500">vacinas</a> -->
              </div>
            </li>
            <li>
              <div class="flex items-center">
                <svg
                  aria-hidden="true"
                  class="h-6 w-6 text-gray-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    fill-rule="evenodd"
                    d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
                <a href="#" class="ml-1 text-gray-500 hover:text-blue-600 md:ml-2">{{
                  $t('patient-details.patient')
                }}</a>
                <!-- <a href="#" class="ml-1  text-gray-500">vacinas</a> -->
              </div>
            </li>
            <li>
              <div class="flex items-center">
                <svg
                  aria-hidden="true"
                  class="h-6 w-6 text-gray-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    fill-rule="evenodd"
                    d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
                <span class="ml-1 font-medium text-gray-500 md:ml-2">{{ $t('patient-details.booklet') }}</span>
              </div>
            </li>
          </ol>
        </nav>

        <p class="pt-4 text-2xl font-semibold tracking-tight text-gray-700">
          {{ $t('patient-details.booklet') }} <span class="font-normal"> {{ $t('patient-details.zero-to-fif') }}</span>
        </p>
        <div class="flex justify-end">
          <div class="flex items-center">
            <IncludeVaccineModal />
          </div>

          <div scope="col" colspan="2" class="px-6 pt-8 text-center uppercase">
            <InputIconWrapper>
              <template #icon>
                <SearchIcon aria-hidden="true" class="h-5 w-5" />
              </template>
              <Input
                v-model="vaccineQuery"
                :placeholder="$t('patient-details.search-vaccines')"
                withIcon
                class="w-full rounded-full bg-[#F3F3F3] px-10 py-3 !shadow-md focus:shadow-none"
              />
            </InputIconWrapper>
            <div class="py-2 text-right text-sm font-normal lowercase text-gray-400">
              {{ $t('patient-details.total-of') }}
              <span class="lowercase">
                <span v-if="filteredVaccines.length == 1"
                  ><span class="font-semibold">{{ filteredVaccines.length }}</span> vacina{{
                    $t('patient-details.vaccine')
                  }}</span
                >
                <span v-else-if="filteredVaccines.length == 0"
                  ><span class="font-semibold">{{ filteredVaccines.length }}</span>
                  {{ $t('patient-details.vaccines') }}</span
                >
                <span v-else
                  ><span class="font-semibold">{{ filteredVaccines.length }}</span>
                  {{ $t('patient-details.vaccines') }}</span
                >
              </span>
            </div>
          </div>
        </div>
        <div class="flex flex-col justify-between sm:flex-row">
          <div class="pl-2">
            <div class="flex place-items-end md:mt-0">
              <div
                class="flex flex-col items-end rounded-md px-3 py-2 text-sm font-semibold text-gray-600 md:flex-row md:items-center"
              >
                <span class="flex w-40 items-center px-2 text-[#636464]">
                  <VaccineAlert :status="3" class="pr-3" />{{ $t('patient-details.overdue-doses') }}</span
                >
                <span class="flex w-40 items-center px-2 text-[#636464]">
                  <VaccineAlert :status="1" class="pr-3" />{{ $t('patient-details.completed-doses') }}</span
                >
                <span class="flex w-40 items-center px-2 text-[#636464]">
                  <VaccineAlert :status="4" class="pr-3" />{{ $t('patient-details.recommended-doses') }}</span
                >
              </div>
            </div>
          </div>
        </div>
        <div class="py-2">
          <div class="overflow-auto px-2 pt-2 pb-52">
            <table class="w-full table-auto text-left tracking-wide md:table-fixed lg:table-fixed">
              <thead class="">
                <tr>
                  <th scope="col" colspan="12" class="pt-10 pb-2 text-center">
                    <span class="rounded-t-full border border-transparent bg-[#DDDDDD] p-2 pt-3 uppercase">{{
                      $t('patient-details.months')
                    }}</span>
                  </th>
                  <th scope="col" colspan="4" class="pt-10 pb-2 text-center">
                    <span class="rounded-t-full border border-transparent bg-[#D4D4D4] p-2 pt-3 uppercase">{{
                      $t('patient-details.years')
                    }}</span>
                  </th>
                </tr>
                <tr class="divide-x-4 divide-[#F8F9FB] border-b-2 border-[#F8F9FB] text-center">
                  <th
                    scope="col"
                    colspan="2"
                    class="whitespace-nowrap px-2.5 pt-2 pl-6 text-left !font-semibold uppercase text-gray-700"
                  >
                    {{ $t('patient-details.vaccines') }}
                  </th>
                  <th
                    scope="col"
                    :class="{ 'border-x-2 border-t-2 border-sky-500': ageInMonths >= 0 && ageInMonths < 2 }"
                    class="whitespace-nowrap rounded-l-3xl bg-[#E9E9E9] px-6 py-4"
                  >
                    0
                  </th>
                  <th
                    scope="col"
                    :class="{ 'border-x-2 border-t-2 border-sky-500': ageInMonths >= 2 && ageInMonths < 3 }"
                    class="whitespace-nowrap bg-[#DDDDDD] px-6 py-4"
                  >
                    2
                  </th>
                  <th
                    scope="col"
                    :class="{ 'border-x-2 border-t-2 border-sky-500': ageInMonths >= 3 && ageInMonths < 4 }"
                    class="whitespace-nowrap bg-[#DDDDDD] px-6 py-4"
                  >
                    3
                  </th>
                  <th
                    scope="col"
                    :class="{ 'border-x-2 border-t-2 border-sky-500': ageInMonths >= 4 && ageInMonths < 5 }"
                    class="whitespace-nowrap bg-[#DDDDDD] px-6 py-4"
                  >
                    4
                  </th>
                  <th
                    scope="col"
                    :class="{ 'border-x-2 border-t-2 border-sky-500': ageInMonths >= 5 && ageInMonths < 6 }"
                    class="whitespace-nowrap bg-[#DDDDDD] px-6 py-4"
                  >
                    5
                  </th>
                  <th
                    scope="col"
                    :class="{ 'border-x-2 border-t-2 border-sky-500': ageInMonths >= 6 && ageInMonths < 7 }"
                    class="whitespace-nowrap bg-[#DDDDDD] px-6 py-4"
                  >
                    6
                  </th>
                  <th
                    scope="col"
                    :class="{ 'border-x-2 border-t-2 border-sky-500': ageInMonths >= 7 && ageInMonths < 9 }"
                    class="whitespace-nowrap bg-[#DDDDDD] px-6 py-4"
                  >
                    7
                  </th>
                  <th
                    scope="col"
                    :class="{ 'border-x-2 border-t-2 border-sky-500': ageInMonths >= 9 && ageInMonths < 12 }"
                    class="whitespace-nowrap bg-[#DDDDDD] px-6 py-4"
                  >
                    9
                  </th>
                  <th
                    scope="col"
                    :class="{ 'border-x-2 border-t-2 border-sky-500': ageInMonths >= 12 && ageInMonths < 15 }"
                    class="whitespace-nowrap bg-[#DDDDDD] px-6 py-4"
                  >
                    12
                  </th>
                  <th
                    scope="col"
                    :class="{ 'border-x-2 border-t-2 border-sky-500': ageInMonths >= 15 && ageInMonths < 48 }"
                    class="whitespace-nowrap bg-[#DDDDDD] px-6 py-4"
                  >
                    15
                  </th>
                  <th
                    scope="col"
                    :class="{ 'border-x-2 border-t-2 border-sky-500': ageInMonths >= 48 && ageInMonths < 60 }"
                    class="whitespace-nowrap bg-[#D4D4D4] px-6 py-4"
                  >
                    4
                  </th>
                  <th
                    scope="col"
                    :class="{ 'border-x-2 border-t-2 border-sky-500': ageInMonths >= 60 && ageInMonths < 108 }"
                    class="whitespace-nowrap bg-[#D4D4D4] px-6 py-4"
                  >
                    5
                  </th>
                  <th
                    scope="col"
                    :class="{ 'border-x-2 border-t-2 border-sky-500': ageInMonths >= 108 && ageInMonths < 168 }"
                    class="whitespace-nowrap bg-[#D4D4D4] px-6 py-4"
                  >
                    9
                  </th>
                  <th
                    scope="col"
                    :class="{ 'border-x-2 border-t-2 border-sky-500': ageInMonths >= 168 && ageInMonths < 200 }"
                    class="whitespace-nowrap rounded-r-full bg-[#D4D4D4] px-6 py-4"
                  >
                    14
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y-4 divide-[#F8F9FB]">
                <tr
                  class="h-16 divide-x-4 divide-[#F8F9FB]"
                  v-for="(vaccine, k) in orderedVaccinesByDoseAlerts"
                  :key="k"
                >
                  <td colspan="2" class="rounded-l-full bg-[#F1F1F1] px-6 py-1 text-sm">
                    <span class="">{{ vaccine.display }}</span> <span class="">{{ vaccine.description }}</span>
                  </td>

                  <td
                    :class="{
                      'col-birth box-border border-x-2 border-sky-500':
                        ageInMonthss >= monthRanges[rangeIndex].start && ageInMonths < monthRanges[rangeIndex].end,
                      'rounded-r-full': rangeIndex == monthRanges.length - 1,
                      'bg-[#E9E9E9]': rangeIndex == 0,
                      'bg-[#DDDDDD]': rangeIndex > 0 && rangeIndex < 10,
                      'bg-[#D4D4D4]': rangeIndex >= 10,
                    }"
                    class="whitespace-nowrap text-sm font-light"
                    v-for="(range, rangeIndex) in ranges"
                    :key="rangeIndex"
                  >
                    <div v-for="(dose, dk) in filteredDosesByVaccine(vaccine)" :key="dk" class="flex justify-center">
                      <VaccineAlert
                        v-if="
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
                          (Math.floor(dose.minimum_recommended_age / 13) >= rangeIndex + 1 ||
                            Math.floor(dose.maximum_recommended_age / 13) <= rangeIndex + 1) &&
                          isWithinInterval(add(birthDate, { months: dose.maximum_recommended_age }), {
                            start: range.start,
                            end: range.end,
                          })
                        "
                      >
                        <VaccineAlertInfo :vaccine="vaccine" :dose="dose" :withoutDetails="true" />
                      </VaccineAlert>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            <div class="grid justify-items-end py-3 text-sm text-gray-400">
              <span>
                {{ $t('patient-details.generated-date', [format(new Date(), 'dd/MM/yyyy kk:mm')]) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch } from 'vue'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { PlusCircleIcon, SearchIcon, XIcon } from '@heroicons/vue/outline'
import { CloudUploadIcon } from '@heroicons/vue/solid'
import { useRouter } from 'vue-router'
import { computed } from 'vue'
import {
  format,
  parseISO,
  add,
  isWithinInterval,
  startOfMonth,
  differenceInMonths,
  differenceInDays,
  subDays,
  setDefaultOptions,
} from 'date-fns'
import { usePatientsStore } from '@/stores/patients'
import { useDosesStore } from '@/stores/doses'
import { useVaccinesStore } from '@/stores/vaccines'
import { useLoggedUserStore } from '@/stores/loggedUser'
import VaccineAlert from '../atoms/VaccineAlert.vue'
import { TransitionRoot, TransitionChild, Dialog, DialogPanel, DialogTitle } from '@headlessui/vue'

const patientsStore = usePatientsStore()
const dosesStore = useDosesStore()
const vaccinesStore = useVaccinesStore()
const loggedUserStore = useLoggedUserStore()

const router = useRouter()
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
const birthDate = computed(() => parseISO(patientsStore.item.birth_date))
//const birthDateInMonthsFromNow = computed(() => differenceInMonths(birthDate, new Date()) )
const ageInMonths = computed(() => differenceInMonths(new Date(), birthDate.value))

const vaccineQuery = ref('')

const filteredVaccines = computed(() => {
  return vaccinesStore.items.filter((vaccine) => {
    return (
      vaccine.system == 'BRI' &&
      dosesStore.items.map((e) => e.vaccine).includes(vaccine.id) &&
      (vaccine.description.toLowerCase().includes(vaccineQuery.value.toLowerCase()) ||
        vaccine.display.toLowerCase().includes(vaccineQuery.value.toLowerCase()))
    )
  })
})
const selectedVaccine = ref(filteredVaccines.value[0])

const totalAlerts = computed(() => {
  return (vaccine) =>
    filteredDosesByVaccine
      .value(vaccine)
      .map((d) => d.alerts.length)
      .reduce((total, current) => total + current)
})

const orderedVaccinesByDoseAlerts = computed(() => {
  return filteredVaccines.value.sort((a, b) => totalAlerts.value(b) - totalAlerts.value(a))
})

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

const monthRanges = computed(() => [
  { start: 0, end: 2 },
  { start: 2, end: 3 },
  { start: 3, end: 4 },
  { start: 4, end: 5 },

  { start: 5, end: 6 },
  { start: 6, end: 7 },
  { start: 7, end: 9 },

  { start: 9, end: 12 },

  { start: 12, end: 15 },

  { start: 15, end: 48 },
  { start: 48, end: 60 },
  { start: 60, end: 108 },
  { start: 108, end: 168 },
  { start: 168, end: 200 },
])

const ranges = computed(() => [
  { start: birthDate.value, end: add(birthDate.value, { months: 0 }) }, //ao nascer
  { start: add(birthDate.value, { months: 0, seconds: 1 }), end: add(birthDate.value, { months: 2 }) },
  { start: add(birthDate.value, { months: 2, seconds: 1 }), end: add(birthDate.value, { months: 3 }) },
  { start: add(birthDate.value, { months: 3, seconds: 1 }), end: add(birthDate.value, { months: 4 }) },
  { start: add(birthDate.value, { months: 4, seconds: 1 }), end: add(birthDate.value, { months: 5 }) },

  { start: add(birthDate.value, { months: 5, seconds: 1 }), end: add(birthDate.value, { months: 6 }) },
  { start: add(birthDate.value, { months: 6, seconds: 1 }), end: add(birthDate.value, { months: 7 }) },
  { start: add(birthDate.value, { months: 7, seconds: 1 }), end: add(birthDate.value, { months: 9 }) },

  { start: add(birthDate.value, { months: 9, seconds: 1 }), end: add(birthDate.value, { months: 12 }) },

  { start: add(birthDate.value, { months: 12, seconds: 1 }), end: add(birthDate.value, { months: 15 }) },

  { start: add(birthDate.value, { months: 15, seconds: 1 }), end: add(birthDate.value, { months: 48 }) },
  { start: add(birthDate.value, { months: 48, seconds: 1 }), end: add(birthDate.value, { months: 60 }) },
  { start: add(birthDate.value, { months: 60, seconds: 1 }), end: add(birthDate.value, { months: 108 }) },
  { start: add(birthDate.value, { months: 108, seconds: 1 }), end: add(birthDate.value, { months: 168 }) },
])

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
th {
  font-weight: 400;
}
</style>
