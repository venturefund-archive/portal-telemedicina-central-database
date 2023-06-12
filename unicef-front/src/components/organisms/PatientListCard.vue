<template>
  <div class="flex h-full flex-col">
    <p class="mb-4 text-xl font-semibold text-gray-700">{{ $t('manager.patients-delayed') }}</p>

    <div
      class="border-1 float-right flex h-full w-full flex-col justify-between rounded-2xl border border-gray-200 bg-white p-4"
    >
      <!-- List contents here -->
      <BaseCard class="px-1" @update:query="handleMarkerChange">
        <div class="-mt-10 flex hidden pb-10">
          <button
            class="border-1 rounded-l-md border border-gray-300 py-2 px-4 text-sm hover:text-green-500"
            :class="{
              'border-green-500 bg-green-500 text-white hover:cursor-default hover:!text-white': mode == 'cpfs',
            }"
            @click="mode = 'cpfs'"
          >
            CPFS
          </button>
          <button
            class="border-1 rounded-r-md border border-gray-300 py-2 px-4 text-sm hover:text-green-500"
            :class="{
              'border-green-500 bg-green-500 text-white hover:cursor-default hover:!text-white': mode != 'cpfs',
            }"
            @click="mode = 'bairro'"
          >
            {{ $t('manager.district') }}
          </button>

          <button
            @click="showList = !showList"
            class="z-5 bg-primary relative flex flex-col items-center rounded-md py-2 px-4 text-gray-500"
          >
            <UsersIcon title="População" class="h-6 w-6 text-green-500" />
          </button>
          <ul v-if="showList" class="absolute z-20 mt-12 ml-40 rounded-md bg-white shadow-md">
            <li
              v-for="item in items"
              :class="{ 'font-bold': item === selectedItem }"
              class="cursor-pointer py-2 px-4 font-normal hover:bg-gray-100"
              :key="item"
            >
              {{ item }}
            </li>
          </ul>
        </div>
        <div class="flex h-96 justify-center" v-if="patientsStore.isLoading && 0 == paginated.length">
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
        <div class="flex h-full flex-col items-center justify-center" v-else-if="false == patientsStore.isLoading && 0 == paginated.length">
          <div class="flex justify-center">
            <EmptyResultPhoto />
          </div>
          <span class="flex justify-center font-semibold">{{ $t('manager.no-results') }}</span>
          <span class="flex justify-center text-gray-500">{{ $t('manager.no-results-description') }}. </span>
        </div>
        <div
          v-else
          class="flex items-center justify-between border-b border-gray-200 px-2 pb-1 pt-4 hover:rounded hover:bg-gray-100"
          v-for="(patient, index) in paginated"
          :key="index"
        >
          <div class="flex flex-auto items-center gap-2">
            <span class="hidden align-baseline text-xs text-gray-500">{{ indexStart + ++index }}.</span>
            <div>
              <p
                @click="
                  $emit('centralize-on-location', { ...patient.address, markerIndex: index })
                "
                class="text-lg font-semibold capitalize hover:cursor-pointer hover:underline"
              >
                {{ patient.name.toLowerCase() }}
              </p>

              <span class="text-sm text-gray-500"> {{ patient.address }} </span>
            </div>
          </div>
          <div>
            <div v-if="patient.number_of_alerts_by_protocol != false">
              <!-- <span class="flex-none pr-14">{{ patient.number_of_alerts_by_protocol }}</span> -->
            </div>

            <a
              :href="`/patients/${patient.id}`"
              class="border-1 cursor-pointer rounded border border-green-500 py-2 px-4 text-sm font-normal uppercase tracking-wide text-green-500 hover:bg-green-500 hover:text-white hover:no-underline"
              @click.prevent="vaccineModalIndex = patient.id; patientsStore.item = patient"
              >{{ $t('manager.details') }}</a
            >
            <VaccineTableModal
              v-if="patient.id === vaccineModalIndex"
              :patient="patientsStore.item"
              :is-open="patient.id === vaccineModalIndex"
              @on-close="vaccineModalIndex = null"
            />
          </div>
        </div>
      </BaseCard>

      <div class="py-5" v-if="paginated">
        <!-- Pagination contents here -->
        <div class="flex justify-between p-4" v-if="0 != totalPages">
          <!-- Pagination contents here -->
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
              <span class="font-semibold">{{ current }} / {{ totalPages }}</span> {{ $t('dashboard.page')
              }}<span v-if="totalPages > 1">s</span></span
            >
            <span class="text-xs lowercase text-neutral-400">
              <span class="font-semibold">{{ filteredPatients.length }}</span> {{ $t('dashboard.result')
              }}<span v-if="filteredPatients.length > 1">s</span> {{ $t('dashboard.of-total-of') }}
              <span class="font-semibold">{{ patients.length }}</span> {{ $t('dashboard.patients') }}</span
            >
          </div>

          <div>
            <Button
              :disabled="isLastPage"
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
</template>

<script setup>
import {
  defineComponent,
  reactive,
  computed,
  onBeforeUpdate,
  onMounted,
  watch,
  ref,
  onUnmounted,
  defineExpose,
} from 'vue'
import {
  HandIcon,
  PencilIcon,
  UsersIcon,
  ArrowLeftIcon,
  ArrowRightIcon,
  DownloadIcon,
  ShareIcon,
} from '@heroicons/vue/solid'
import { usePatientsStore } from '@/stores/patients'
const patientsStore = usePatientsStore()

const mode = ref('cpfs')
const patientQuery = ref('')
const current = ref(1)
const pageSize = ref(9)
const isLastPage = computed(() => current.value + 1 >= totalPages.value + 1)
const isFirstPage = computed(() => current.value == 1)
const indexStart = computed(() => (current.value - 1) * pageSize.value)
const indexEnd = computed(() => indexStart.value + pageSize.value)
const filteredPatients = computed(() => {
  return filteredPatientsQuery.value.filter(
    (patient) => !props.onlyAlerts || (props.onlyAlerts && 0 !== patient.alerts.length)
  )
})
const filteredPatientsQuery = computed(() => {
  return props.patients.filter((patient) => {
    return patient.name.toLowerCase().includes(patientQuery.value.toLowerCase())
  })
})
const handleMarkerChange = (event) => {
  patientQuery.value = event
}

const totalPages = computed(() => Math.ceil(filteredPatients.value.length / pageSize.value))
const paginated = computed(() => filteredPatients.value.slice(indexStart.value, indexEnd.value))

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
  patients: {
    type: Array,
    default: [],
  },
  onlyAlerts: {
    type: Boolean,
    default: false,
  },
})
const vaccineModalIndex = ref(null)
// const openVaccineModal = (patientId) => {
//   vaccineModalIndex.va
// }

const handleClickOutside = (event) => {
  if (!event.target.closest('.mt-4')) {
    showList.value = false
  }
}

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

function onItemClick(item) {
  selectedItem.value = item
  console.log(`Item clicado: ${item}`)
}

const showList = ref(false)
const items = [
  'Todos',
  'Gestantes',
  'Puérperas',
  'Recém-nascidos',
  'Primeira infância',
  'Segunda infância',
  'Terceira Infância',
  'Adolescência',
]
</script>

<style>
.container {
  padding: 5px;
}

.list {
  background-color: white;
  border-radius: 5px;
  padding: 5px;
}

.list-item {
  cursor: pointer;
}

.edit-panel {
  position: fixed;
  left: 50%;
  top: 0;
  width: 380px;
  margin: 150px 0 0 -190px; /* Apply negative top and left margins to center the element */
}
</style>
