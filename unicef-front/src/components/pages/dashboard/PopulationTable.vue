<template>
  <section class="mx-auto grid w-full grid-cols-1 place-content-center gap-6 pt-5 md:pt-0 lg:pt-0">
    <p class="mt-5 text-xl font-semibold uppercase tracking-tight text-gray-700">
      {{ $t('dashboard.health-population') }}
    </p>

    <div class="w-full rounded-t-2xl !bg-white shadow">
      <div>
        <div class="flex flex-col items-center justify-between space-y-5 p-5 md:flex-row md:space-x-5 md:space-y-0">
          <div class="flex flex-col items-center space-y-5 md:flex-row md:space-x-5 md:space-y-0">
            <div class="flex items-center space-x-5">
              <div class="flex items-center">
                <UserIcon class="mr-3 h-6 w-6 text-blue-500" />
                <div class="flex flex-col items-start justify-center">
                  <h4 class="pl-1 text-xl font-semibold">{{ filterAndSortPatients.length }}</h4>
                  <span class="text-sm text-gray-500">{{ $t('dashboard.patients') }}</span>
                </div>
              </div>
              <div
                class="border-r-1 inline-flex items-center justify-center gap-2 border border-l-0 border-gray-200 border-b-transparent border-t-transparent py-7"
              ></div>
              <div>
                <form @submit.prevent="searchAddress">
                  <label for="default-search" class="sr-only">Procurar</label>
                  <div class="relative flex items-center">
                    <svg
                      class="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 transform text-gray-500"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                      ></path>
                    </svg>
                    <div>
                      <Input
                        :placeholder="$t('dashboard.pesquisar-por-pacientes-numero-de-documento-etc')"
                        v-model="patientQuery"
                        @update:query="searchHandler"
                        class="w-96 rounded-lg py-2 pl-10 pr-3 focus:outline-none"
                      />
                    </div>
                  </div>
                </form>
              </div>
            </div>

            <!-- User List and Alerts -->
            <div class="flex items-center md:space-x-10">
              <div ref="dropdown" class="relative hidden">
                <button
                  @click="showList = !showList"
                  class="relative flex flex-col items-center rounded-md px-4 py-2 text-gray-500"
                >
                  <UsersIcon :title="t('manager.population')" class="h-6 w-6 text-gray-500" />
                  <span class="text-sm">{{ $t('manager.population') }}</span>
                </button>
                <ul v-if="showList" class="absolute z-10 w-40 rounded-md bg-white shadow-md">
                  <li
                    v-for="item in items"
                    :class="{ 'font-bold': item === selectedItem }"
                    class="w-full cursor-pointer px-4 py-2 font-normal capitalize hover:bg-gray-100"
                    :key="item"
                  >
                    {{ item }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="flex flex-col rounded rounded-b-2xl bg-white shadow-lg">
        <div class="flex justify-between gap-4 border-b text-left text-xs font-medium uppercase text-gray-500">
          <span class="flex-grow p-2 pl-5">{{ $t('dashboard.patient') }}</span>
          <span class="hidden w-36 p-2 text-center">{{ $t('dashboard.priority') }}</span>
          <span class="hidden w-36 p-2 text-center">{{ $t('dashboard.alerts') }}</span>
          <span class="hidden w-36 p-2 text-center">{{ $t('dashboard.team') }}</span>
          <span class="w-48 p-2 text-center">{{ $t('manager.alerts-protocol') }}</span>
          <span class="w-36 p-2 text-center"></span>
          <span class="w-36 p-2 text-center"></span>
        </div>

        <div class="max-h-[580px] overflow-y-auto">
          <div
            class="text-md h-18 flex flex-col items-center gap-4 p-2 text-left hover:bg-gray-100 md:flex-row"
            v-for="(patient, index) in paginated"
            :key="index"
            :class="{ 'bg-gray-50': index % 2 }"
          >
            <span class="flex-grow whitespace-nowrap p-2 font-semibold capitalize">
              <router-link
                :to="{ name: 'PatientDetails', params: { id: patient.id } }"
                class="hover:underline"
                @click="handleClick({ id: patient.id })"
              >
                {{ patient.name.toLowerCase() }}
              </router-link>
            </span>
            <span class="w-36 p-2 text-center text-gray-500">{{ patient.number_of_alerts_by_protocol }}</span>
            <span class="hidden w-72 p-2 pl-16 text-center">
              <span :class="['inline-block rounded-full px-2 py-1 text-sm', getClassByPriority(priority)]">
                {{ priority }}
              </span>
            </span>
            <span class="hidden w-auto p-2 text-center">
              <span
                class="mr-0.5 inline-block rounded-full px-2 py-2 opacity-90"
                v-for="(color, index) in colors"
                :key="index"
                :class="color"
              >
              </span>
            </span>
            <span class="hidden w-36 p-2 text-center text-gray-500">49 - Integração</span>
            <span class="hidden w-36 p-2 text-center text-gray-500">
              <!-- <router-link :to="`/map/area/${area.id}`">{{ area.name }}</router-link>
              <router-link :to="`/map/area/1`">Região Exemplo</router-link> -->
            </span>
            <router-link :to="`/map/patient/${patient.id}`">
              <span class="group flex w-36 cursor-pointer flex-col items-center text-center">
                <MapIcon class="h-6 w-6 font-light text-gray-500" />
                <span class="text-sm lowercase text-gray-500 group-hover:underline">
                  {{ $t('dashboard.see-on-map') }}</span
                >
              </span>
            </router-link>
            <span class="flex w-36 justify-end pr-5">
              <a
                :href="`/patients/${patient.id}`"
                class="cursor-pointer font-normal lowercase text-blue-600 hover:underline"
                @click.prevent="handlePatientDetails(patient)"
              >
                {{ $t('manager.see-details') }}
              </a>
              <PatientDetailsModal
                v-if="patient.id === vaccineModalIndex"
                :patient="patientsStore.item"
                :is-open="patient.id === vaccineModalIndex"
                @on-close="vaccineModalIndex = null"
              />
            </span>
          </div>
        </div>

        <div v-if="patientsStore.isLoading" class="max-h-[580px] overflow-y-auto">
          <div class="flex flex-col pt-4">
            <SkeletonLoader type="text" animation="fade-in" class="h-20 py-3" v-for="i in 100" />
          </div>
        </div>
        <div class="flex h-full flex-col items-center justify-center p-48" v-else-if="paginated.length == 0">
          <div class="flex justify-center">
            <EmptyResultPhoto />
          </div>
          <span class="flex justify-center font-semibold">{{ $t('manager.no-results') }}</span>
          <span class="flex justify-center text-gray-500">{{ $t('manager.no-results-description') }}. </span>
        </div>

        <div class="flex" v-if="paginated.length > 0">
          <div class="flex w-full justify-between p-4" v-if="0 != totalPages">
            <div>
              <Button
                :disabled="isFirstPage"
                size="sm"
                iconOnly
                variant="secondary"
                v-slot="{ iconSizeClasses }"
                @click="prev"
              >
                <ArrowLeftIcon aria-hidden="true" :class="iconSizeClasses" />
              </Button>
            </div>
            <div class="flex flex-col items-center">
              <span class="text-sm">
                <span class="font-semibold">{{ current }} / {{ totalPages }}</span>
                {{ $t('dashboard.page') }}
                <span v-if="totalPages > 1">s</span>
              </span>
              <span class="text-xs lowercase text-neutral-400">
                <span class="font-semibold">{{ filterAndSortPatients.length }}</span>
                {{ $t('dashboard.result') }}
                <span v-if="filterAndSortPatients.length > 1">s</span>
                {{ $t('dashboard.of-total-of') }}
                <span class="font-semibold">{{ patientsStore.items.length }}</span>
                {{ $t('dashboard.patients') }}
              </span>
            </div>
            <div>
              <Button
                :disabled="isLastPage"
                :class="[
                  'h-9 w-9 rounded-lg px-2 py-1',
                  isLastPage ? 'cursor-not-allowed bg-gray-100 text-gray-400' : ' bg-blue-50 text-blue-500',
                ]"
                size="sm"
                iconOnly
                variant="secondary"
                v-slot="{ iconSizeClasses }"
                @click="next()"
              >
                <ArrowRightIcon aria-hidden="true" :class="iconSizeClasses" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, onUpdated, reactive, ref, computed, onUnmounted } from 'vue'
import { DotsVerticalIcon, ArrowLeftIcon, ArrowRightIcon } from '@heroicons/vue/solid'
import { MapIcon, UsersIcon, UserIcon } from '@heroicons/vue/outline'
import { useRouter } from 'vue-router'
import { usePatientsStore } from '@/stores/patients'
import { useLoggedUserStore } from '@/stores/loggedUser'
import { useI18n } from 'vue3-i18n'

const { t } = useI18n()
const loggedUserStore = useLoggedUserStore()
const patientsStore = usePatientsStore()
const router = useRouter()

const patientQuery = ref('')
const current = ref(1)
const pageSize = ref(props.pageSize)
const isLastPage = computed(() => current.value + 1 >= totalPages.value + 1)
const isFirstPage = computed(() => current.value == 1)
const indexStart = computed(() => (current.value - 1) * pageSize.value)
const indexEnd = computed(() => indexStart.value + pageSize.value)

const filteredPatients = computed(() => {
  return patientsStore.items.filter((patient) => {
    return patient.name.toLowerCase().includes(patientQuery.value.toLowerCase())
  })
})

import { useStorage } from '@vueuse/core'
const state = useStorage('app-store', { token: '' })
const handleClick = ({ id }) => {
  state.value.patientLastViewed = id
}

const handlePatientDetails = (patient) => {
  vaccineModalIndex.value = patient.id
  patientsStore.item = patient
}
const filterAndSortPatients = computed(() => {
  return filteredPatients.value.sort((a, b) => {
    // Comparar prioridades
    // if (a.priority !== b.priority) {
    //   // Se a prioridade de a for maior que a de b, a vem primeiro (ordem decrescente)
    //   return b.priority - a.priority;
    // }
    // // Se as prioridades são iguais, compare a equipe
    // if (a.team !== b.team) {
    //   // Ordene alfabeticamente (ordem crescente)
    //   return a.team.localeCompare(b.team);
    // }
    // // Se a equipe é a mesma, compare a área
    // // Ordene alfabeticamente (ordem crescente)
    // return a.area.localeCompare(b.area);
  })
})

const handleClickOutside = (event) => {
  if (!event.target.closest('.mt-4')) {
    showList.value = false
  }
}

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

const getClassByPriority = (priority) => {
  switch (priority) {
    case 'ALTA':
      return 'bg-red-100 text-red-900'
    case 'MÉDIA':
      return 'bg-yellow-100 text-yellow-900'
    case 'BAIXA':
      return 'bg-blue-100 text-blue-900'
    default:
      return ''
  }
}
const showList = ref(false)
const items = computed(() => [
  t('manager.all-group'),
  t('manager.pragnant-group'),
  t('manager.puerp-group'),
  t('manager.newborn-group'),
  t('manager.firstchild-group'),
  t('manager.secondchild-group'),
  t('manager.thirdchild-group'),
  t('manager.teenager-group'),
])

const colors = ref(['bg-red-500', 'bg-blue-500', 'bg-green-500', 'bg-yellow-500'])

const vaccineModalIndex = ref(null)
const priority = ref('ALTA') // Pode ser 'ALTA', 'MÉDIA' ou 'BAIXA'

const searchHandler = (event) => {
  patientQuery.value = event
  current.value = 1
}
const totalPages = computed(() => Math.ceil(filterAndSortPatients.value.length / pageSize.value))
const paginated = computed(() => filterAndSortPatients.value.slice(indexStart.value, indexEnd.value))

function prev() {
  if (isFirstPage.value) {
    return
  }
  current.value--
}
function next() {
  if (isLastPage.value) {
    return
  }
  current.value++
}

const props = defineProps({
  pageSize: {
    type: Number,
    default: 10,
  },
})
</script>
<style>
@media (max-width: {{ breakpoints.md }}) {
  /* Apply mobile-specific styles here */
  .grid-cols-1 {
    grid-template-columns: 1fr;
  }

  .md\:grid-cols-1 {
    grid-template-columns: 1fr;
  }
}
</style>
