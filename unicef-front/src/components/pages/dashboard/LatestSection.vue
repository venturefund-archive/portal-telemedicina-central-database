<template>
  <section class="grid grid-cols-1 gap-6 lg:grid-cols-2">
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-1" v-if="paginated">
      <BaseCard title="Total de alertas por paciente" :actions="[{ title: 'View', to: '#' }]">

        <div class="mt-4 flex items-center justify-between" v-for="(patient, index) in paginated" :key="index">
          <div class="flex items-center gap-2 flex-auto">
            <span class="hidden text-xs text-gray-500 align-baseline">{{ indexStart + ++index }}.</span>
            <img class="h-10 w-10 p-1 rounded-md object-cover rounded-full bg-neutral-200" src="/avatar.png" />
            <div>
              <h5 class="text-sm text-gray-600 dark:text-gray-300">
                <router-link :to="{ name: 'PatientDetails', params: { id: patient.id } }" class="hover:underline">{{
                  patient.name.join() }}</router-link>
              </h5>
            </div>
          </div>
          <span class="flex-none pr-14">{{ patient.number_of_alerts_by_protocol }}</span>
        </div>

        <div class="flex justify-between pt-10">
          <div>
            <Button :disabled="isFirstPage" size="sm" iconOnly variant="secondary" v-slot="{ iconSizeClasses }"
              @click="prev">
              <ArrowLeftIcon aria-hidden="true" :class="iconSizeClasses" />
            </Button>
          </div>
          <div class="flex flex-col items-center">
            <span class="text-sm"> <span class="font-semibold">{{ current }} / {{ patientsStore.items.length / pageSize
            }}</span> páginas</span>
            <span class="text-xs text-neutral-400 py-2"><span class="font-semibold">{{ patientsStore.items.length
            }}</span> pacientes com alertas</span>
          </div>

          <div>
            <Button :disabled="isLastPage" size="sm" iconOnly variant="secondary" v-slot="{ iconSizeClasses }"
              @click="next()">
              <ArrowRightIcon aria-hidden="true" :class="iconSizeClasses" />
            </Button>
          </div>
        </div>
      </BaseCard>
    </div>

    <BaseCard title="Escala do dia">
      <div class="mt-4 flex items-center justify-between" v-for="i in 4" :key="i">
        <div class="flex items-center gap-2">
          <div>
            <h5 class="text-sm text-gray-600 dark:text-gray-300">10:30</h5>
            <p class="text-sm text-gray-400 dark:text-gray-500">20 Mar 2020</p>
          </div>
        </div>
      </div>
    </BaseCard>
  </section>
</template>

<script setup>
import { onMounted, onUpdated, reactive, ref, computed } from 'vue'
import { DotsVerticalIcon, ArrowLeftIcon, ArrowRightIcon } from '@heroicons/vue/solid'
import { useRouter } from 'vue-router'
import { usePatientsStore } from '@/stores/patients'
import { useLoggedUserStore } from '@/stores/loggedUser'
const loggedUserStore = useLoggedUserStore()
const patientsStore = usePatientsStore()
const router = useRouter()

const patientQuery = ref('')
const current = ref(1)
const pageSize = ref(5)
const isLastPage = computed(() => (current.value + 1 >= (patientsStore.items.length / pageSize.value) + 1))
const isFirstPage = computed(() => (current.value == 1))
const indexStart = computed(() => (current.value - 1) * pageSize.value)
const indexEnd = computed(() => indexStart.value + pageSize.value)
const filteredPatients = computed(() => {
  return patientsStore.items.filter((patient) => {
    return patient.name.join().toLowerCase().includes(patientQuery.value.toLowerCase())
  })
})
const paginated = computed(() => filteredPatients.value.slice(indexStart.value, indexEnd.value))

function prev() {
  if (isFirstPage.value) {
    return
  }
  current.value--
}
function next() {
  console.log(current.value)
  console.log((patientsStore.items.length / pageSize.value))
  console.log(indexEnd.value)

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
</script>
