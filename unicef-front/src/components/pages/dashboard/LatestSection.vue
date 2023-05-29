<template>
  <section class="mx-auto grid w-full grid-cols-1 place-content-center gap-6 pt-5 md:pt-0 lg:pt-0">
    <p class="mt-5 mt-16 text-xl font-semibold text-gray-700">{{ $t('dashboard.total-alerts-per-patient') }}</p>
    <div class="grid grid-cols-1 gap-6" v-if="paginated">
      <BaseCard class="flex flex-col rounded-xl bg-[#F2F2F2] px-5 shadow-md" @update:query="patientQuery = $event">
        <div
          class="flex items-center justify-between border-b border-white px-2 py-4 hover:rounded hover:bg-gray-100"
          v-for="(patient, index) in paginated"
          :key="index"
        >
          <div class="flex flex-auto items-center gap-2">
            <span class="hidden align-baseline text-xs text-gray-500">{{ indexStart + ++index }}.</span>
            <img class="h-10 w-10 rounded-md rounded-full bg-neutral-200 object-cover p-1" src="/avatar.png" />
            <div>
              <h5 class="font-medium capitalize">
                <router-link :to="{ name: 'PatientDetails', params: { id: patient.id } }" class="hover:underline">{{
                  patient.name.toLowerCase()
                }}</router-link>
              </h5>
            </div>
            <hr class="divide-dotted border text-white" />
          </div>
          <span class="flex-none pr-14 font-normal text-neutral-500">{{ patient.number_of_alerts_by_protocol }}</span>
        </div>

        <div class="flex justify-between pt-3 pb-2 pt-16">
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
</script>
