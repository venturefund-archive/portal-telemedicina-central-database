<template>
  <div>
  <p class="text-lg mb-4 font-semibold text-gray-700">{{ $t('manager.patients-delayed') }}</p>
    <div class="border border-1 border-gray-200 rounded w-full  shadow p-4 rounded float-right">
  <div class="flex items-center">
    <div class="flex">
  <button class="border border-1 border-gray-300  hover:border-green-500 hover:text-green-500 py-2 px-4 rounded-l-md bg-transparent text-sm">CPFS</button>
  <button class="border border-1 border-gray-300  hover:border-green-500 hover:text-green-500 py-2 px-4 rounded-r-md bg-transparent text-sm">{{ $t('manager.district') }}</button>
</div>


    <div class="mt-4 md:mt-0 flex items-center">
      <button @click="showList = !showList" class="relative z-10 flex flex-col items-center px-4 py-2 text-gray-500 bg-primary rounded-md">
        <UsersIcon title="População" class="h-6 w-6 text-green-500"/>
      </button>
      <ul v-if="showList" class="absolute z-20 rounded-md shadow-md bg-white mt-96">
        <li v-for="item in items" :class="{ 'font-bold': item === selectedItem }" class="px-4 py-2 font-normal cursor-pointer hover:bg-gray-100" :key="item" @click="">
          {{ item }}
        </li>
      </ul>
    </div>
  </div>

  <div class="grid grid-cols-1 gap-2" v-if="paginated">
      <div @update:query="patientQuery = $event">

        <div class="mt-4 flex items-center justify-between hover:bg-gray-100 hover:rounded px-2 py-1 border-b-2 border-gray-200" v-for="(patient, index) in paginated" :key="index">          <div class="flex items-center gap-2 flex-auto">
            <span class="hidden text-xs text-gray-500 align-baseline">{{ indexStart + ++index }}.</span>
            <div>
              <div>
                <p class="text-lg font-semibold capitalize">{{patient.name.join().toLowerCase() }}</p>
              </div>
              <span class="text-gray-500 text-sm"> Street xxx, district xxx </span>
            </div>
          </div>
          <div>
            <div v-if="patient.number_of_alerts_by_protocol != false">
          <!-- <span class="flex-none pr-14">{{ patient.number_of_alerts_by_protocol }}</span> -->
        </div>
        <button class="border border-1 border-green-500 rounded text-green-500 hover:bg-green-500 hover:text-white py-2 px-2 text-sm rounded cursor-pointer">{{ $t('manager.details') }}</button>

        </div>
        </div>

        <div class="flex justify-between pt-10 pb-2">
          <div>
            <Button :disabled="isFirstPage" size="sm" iconOnly variant="secondary" v-slot="{ iconSizeClasses }"
              @click="prev">
              <ArrowLeftIcon aria-hidden="true" :class="iconSizeClasses" />
            </Button>
          </div>
          <div class="flex flex-col items-center">
            <span class="text-sm" v-if="0 != totalPages">
              <span class="font-semibold">{{ current }} / {{ totalPages }}</span> {{ $t('dashboard.page') }}<span v-if="totalPages > 1">s</span></span>
            <span v-else>{{ $t('dashboard.no-results-found') }}</span>
            <span class="text-xs text-neutral-400 lowercase">
              <span class="font-semibold">{{ filteredPatients.length }}</span> {{ $t('dashboard.result') }}<span v-if="filteredPatients.length > 1">s</span> {{ $t('dashboard.of-total-of') }} <span class="font-semibold">{{ patientsStore.items.length
            }}</span> {{ $t('dashboard.patients') }}</span>
          </div>

          <div>
            <Button :disabled="isLastPage" size="sm" iconOnly variant="secondary" v-slot="{ iconSizeClasses }"
              @click="next()">
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
import { HandIcon, PencilIcon, UsersIcon, ArrowLeftIcon, ArrowRightIcon } from '@heroicons/vue/solid'
import { useRouter } from 'vue-router'
import { usePatientsStore } from '@/stores/patients'
import { useLoggedUserStore } from '@/stores/loggedUser'
const loggedUserStore = useLoggedUserStore()
const patientsStore = usePatientsStore()
const router = useRouter()

const patientQuery = ref('')
const current = ref(1)
const pageSize = ref(9)
const isLastPage = computed(() => (current.value + 1 >= totalPages.value + 1))
const isFirstPage = computed(() => (current.value == 1))
const indexStart = computed(() => (current.value - 1) * pageSize.value)
const indexEnd = computed(() => indexStart.value + pageSize.value)
const filteredPatients = computed(() => {
  return patientsStore.items.filter((patient) => {
    return patient.name.join().toLowerCase().includes(patientQuery.value.toLowerCase())
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
    showList.value = false;
  }
};

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
})

function onItemClick(item) {
  selectedItem.value = item;
  console.log(`Item clicado: ${item}`)
}

const showList = ref(false);
const items = ['Todos', 'Gestantes','Puérperas', 'Recém-nascidos', 'Primeira infância', 'Segunda infância', 'Terceira Infância','Adolescência'];


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

@media (min-width: 768px) {
  .w-1\\/2 {
    width: 50%;
  }
}
</style>
