<template>
  <section class="grid grid-cols-1 gap-6 place-content-center w-full pt-5 md:pt-0 lg:pt-0 mx-auto">
    <p class="text-xl mt-5 font-semibold text-gray-700">{{ $t('dashboard.total-alerts-per-patient') }}</p>
    <div class="grid grid-cols-1 gap-6" v-if="paginated">
      <BaseCard class=" bg-[#F2F2F2] rounded-xl" @update:query="patientQuery = $event">

        <div class="mt-5 flex items-center justify-between hover:bg-gray-100 hover:rounded px-2 py-1" v-for="(patient, index) in paginated" :key="index">
          <div class="flex items-center gap-2 flex-auto">
            <span class="hidden text-xs text-gray-500 align-baseline">{{ indexStart + ++index }}.</span>
            <img class="h-10 w-10 p-1 rounded-md object-cover rounded-full bg-neutral-200" src="/avatar.png" />
            <div>
              <h5 class=" font-medium capitalize">
                <router-link :to="{ name: 'PatientDetails', params: { id: patient.id } }" class="hover:underline">{{
                  patient.name.join().toLowerCase() }}</router-link>
              </h5>
            </div>
            <hr class="text-white divide-dotted border"/>
          </div>
          <span class="flex-none pr-14 font-normal text-neutral-500 ">{{ patient.number_of_alerts_by_protocol }}</span>
        </div>

        <div class="flex justify-between pt-3 pb-2 pt-16">
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
      </BaseCard>
    </div>
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
</script>
