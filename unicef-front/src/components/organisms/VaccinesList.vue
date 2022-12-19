<template>
  <!-- component -->
  <div class="flex flex-col">
    <div class="overflow-x-auto sm:-mx-6 lg:-mx-8 px-3 py-2">
      <div class="inline-block min-w-full sm:px-6 lg:px-8">
        <div class="overflow-hidden">
          <div class="relative overflow-x-auto shadow-md sm:rounded-lg p-20">
            <table class="table-fixed w-full text-left text-sm text-neutral-100 dark:text-neutral-100">
              <thead class="bg-neutral-200 text-xs uppercase text-white dark:text-white">
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
                  <th scope="col" class="px-20 py-4 text-gray-900"></th>
                  <th scope="col" class="text-gray-900">
                    <span class="rounded-t-xl border border-transparent bg-neutral-500 p-2 font-semibold text-white"
                      >Ao nascer</span
                    >
                  </th>
                  <th scope="col" class="px-6 py-4 text-gray-900">2</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">3</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">4</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">5</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">6</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">7-11</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">12</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">15</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">18</th>
                  <!-- anos -->
                  <th scope="col" class="px-6 py-4 text-gray-900">4 a 6</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">10</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">11 a 12</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">13 a 15</th>
                </tr>
              </thead>
              <tbody>
                <tr class="border-b hover:bg-neutral-300" v-for="(vaccine, k) in vaccinesStore.items" :key="k">
                  <td colspan="2"
                    class="show-truncate truncate whitespace-nowrap px-6 py-4 text-sm font-medium capitalize text-gray-900">
                    {{ vaccine.description }}
                  </td>
                  <td
                    class="cursor-pointer whitespace-nowrap px-6 py-4 text-sm font-light text-gray-900"
                    v-for="(range, rangeKey) in [
                      { start: birthDate, end: add(birthDate, { months: 2 }) }, //ao nascer
                      { start: add(birthDate, { months: 2 }), end: add(birthDate, { months: 3 }) },
                      { start: add(birthDate, { months: 3 }), end: add(birthDate, { months: 4 }) },
                      { start: add(birthDate, { months: 4 }), end: add(birthDate, { months: 5 }) },
                      { start: add(birthDate, { months: 5 }), end: add(birthDate, { months: 6 }) },

                      { start: add(birthDate, { months: 6 }), end: add(birthDate, { months: 11 }) },
                      { start: add(birthDate, { months: 11 }), end: add(birthDate, { months: 12 }) },
                      { start: add(birthDate, { months: 12 }), end: add(birthDate, { months: 15 }) },

                      { start: add(birthDate, { months: 15 }), end: add(birthDate, { months: 18 }) },

                      { start: add(birthDate, { months: 18 }), end: add(birthDate, { years: 6 }) },
                      { start: add(birthDate, { years: 6 }), end: add(birthDate, { years: 10 }) },
                      { start: add(birthDate, { years: 10 }), end: add(birthDate, { years: 12 }) },
                      { start: add(birthDate, { years: 12 }), end: add(birthDate, { years: 15 }) },
                    ]" :key="rangeKey">
                    <div v-for="(dose, dk) in filteredDosesByVaccine(vaccine)" :key="dk">

                      <VaccineAlert :status="1" v-if="dose.is_completed" />
                      <div v-else v-for="(alert, ak) in dose.alerts" :key="ak">
                        <!--
                        <div class="absolute bg-neutral-500">
                          <span>birth_parsed: {{ birthDate }}</span>
                          <span>created_at: {{ parseISO(alert.created_at) }}</span>
                          {{ differenceInDays(birthDate, parseISO(alert.created_at)) }}

                          <span>resultado={{ Boolean(isWithinInterval(parseISO(alert.created_at), { start: range.start, end:range.end } )) }}</span>
                          <span>resultado={{ isWithinInterval(parseISO(alert.created_at), { start: range.start, end:range.end } ) }}</span>
                        </div>
                        -->
                        <VaccineAlert :status="2"
                          v-if="isWithinInterval(parseISO(alert.created_at), { start: range.start, end:range.end } )" />
                      </div>

                    </div>

                  </td>

                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { onMounted, onUnmounted, reactive, ref, onUpdated } from 'vue'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { MailIcon, LockClosedIcon, LoginIcon, UserIcon } from '@heroicons/vue/outline'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'
import { computed } from 'vue'
import { formatDistance, parseISO, formatISO9075, add, isWithinInterval, differenceInDays, subDays } from 'date-fns'
import { usePatientsStore } from '@/stores/patients'
import { useDosesStore } from '@/stores/doses'
import { useVaccinesStore } from '@/stores/vaccines'
const patientsStore = usePatientsStore()
const dosesStore = useDosesStore()
const vaccinesStore = useVaccinesStore()

const router = useRouter()

const birthDate = computed(() => parseISO(patientsStore.item.birth_date) )

const filteredDosesByVaccine = computed(() => {
  return (vaccine) => dosesStore.items.filter(dose => {
    return dose.vaccine == vaccine.id
  })

  //const filteredName = this.doses.filter(dose => {
  //  return dose.name.toLowerCase().includes(this.searchTerm.toLowerCase());
  //})
  //const orderedDoses = filteredDoses.sort((a, b) => {
  //  return b.order - a.order;
  //})
  //return orderedDoses;
})

const key = ref(0)

const addDose = () => {
  return console.log('dose adicionada')
}

onMounted(async () => {
  await vaccinesStore.fetchVaccines()
})
</script>

<style scoped>
.show-truncate:hover{
    overflow: visible;
    white-space: normal;
    height:auto;  /* just added this line */
    cursor: default
}
</style>
