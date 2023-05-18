<template>
  <div>
    <p class="mb-4 text-xl font-semibold text-gray-700">{{ $t('manager.patients-delayed') }}</p>
    <div class="border-1 float-right w-full rounded-2xl border border-gray-200 bg-white p-4 shadow">
      <div class="flex justify-between">
        <div class="flex">
          <button
            class="border-1 rounded-l-md border border-gray-300 bg-transparent py-2 px-4 text-sm hover:border-green-500 hover:text-green-500"
          >
            CPFS
          </button>
          <button
            class="border-1 rounded-r-md border border-gray-300 bg-transparent py-2 px-4 text-sm hover:border-green-500 hover:text-green-500"
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
              @click=""
            >
              {{ item }}
            </li>
          </ul>
        </div>
      </div>

      <div class="grid grid-cols-1 gap-2 py-5" v-if="paginated">
        <div @update:query="patientQuery = $event">
          <div
            class="mt-4 flex items-center justify-between border-b-2 border-gray-200 px-2 py-1 hover:rounded hover:bg-gray-100"
            v-for="(patient, index) in paginated"
            :key="index"
          >
            <div class="flex flex-auto items-center gap-2">
              <span class="hidden align-baseline text-xs text-gray-500">{{ indexStart + ++index }}.</span>
              <div>
                <router-link :to="{ name: 'PatientDetails', params: { id: patient.id } }">
                  <p class="text-lg font-semibold capitalize">{{ patient.name.toLowerCase() }}</p>
                </router-link>
                <span class="text-sm text-gray-500"> Street xxx, district xxx </span>
              </div>
            </div>
            <div>
              <div v-if="patient.number_of_alerts_by_protocol != false">
                <!-- <span class="flex-none pr-14">{{ patient.number_of_alerts_by_protocol }}</span> -->
              </div>
              <button
                class="border-1 cursor-pointer rounded border border-green-500 py-2 px-4 text-sm font-normal text-green-500 hover:bg-green-500 hover:text-white"
              >
                {{ $t('manager.details') }}
              </button>
            </div>
          </div>

          <div class="flex justify-between p-4">
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
              <span class="text-sm" v-if="0 != totalPages">
                <span class="font-semibold">{{ current }} / {{ totalPages }}</span> {{ $t('dashboard.page')
                }}<span v-if="totalPages > 1">s</span></span
              >
              <span v-else>{{ $t('dashboard.no-results-found') }}</span>
              <span class="text-xs lowercase text-neutral-400">
                <span class="font-semibold">{{ filteredPatients.length }}</span> {{ $t('dashboard.result')
                }}<span v-if="filteredPatients.length > 1">s</span> {{ $t('dashboard.of-total-of') }}
                <span class="font-semibold">{{ patientsStore.items.length }}</span> {{ $t('dashboard.patients') }}</span
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
  </div>
</template>

<script setup>
import { defineComponent, reactive, computed, onBeforeUpdate, onMounted, watch, ref, onUnmounted } from 'vue'
import {
  HandIcon,
  PencilIcon,
  UsersIcon,
  ArrowLeftIcon,
  ArrowRightIcon,
  DownloadIcon,
  ShareIcon,
} from '@heroicons/vue/solid'
import { useRouter } from 'vue-router'
import { usePatientsStore } from '@/stores/patients'
import { useLoggedUserStore } from '@/stores/loggedUser'
const loggedUserStore = useLoggedUserStore()
const patientsStore = usePatientsStore()
const router = useRouter()

const patientQuery = ref('')
const current = ref(1)
const pageSize = ref(9)
const isLastPage = computed(() => current.value + 1 >= totalPages.value + 1)
const isFirstPage = computed(() => current.value == 1)
const indexStart = computed(() => (current.value - 1) * pageSize.value)
const indexEnd = computed(() => indexStart.value + pageSize.value)
const filteredPatients = computed(() => {
  return patientsStore.items.filter((patient) => {
    return patient.name.toLowerCase().includes(patientQuery.value.toLowerCase())
  })
})
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
  id: {
    type: String,
    default: '',
  },
})

onMounted(async () => {
  await patientsStore.fetchPatients()
})

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
