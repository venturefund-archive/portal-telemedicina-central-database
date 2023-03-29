<template>
  <PageWrapper :title="$t('patient-details.patient-details-title')">
    <div v-if="patientsStore.item && props.id">
      <VaccinesList :id="id" />
    </div>
  </PageWrapper>
</template>

<script setup>
import { onMounted, onUpdated, reactive, ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'
import { watch, computed } from 'vue'
import { usePatientsStore } from '@/stores/patients'
import { useVaccinesStore } from '@/stores/vaccines'
import { useLoggedUserStore } from '@/stores/loggedUser'
import { useDosesStore } from '@/stores/doses'
const loggedUserStore = useLoggedUserStore()
const patientsStore = usePatientsStore()
const vaccinesStore = useVaccinesStore()
const router = useRouter()
const dosesStore = useDosesStore()

const props = defineProps({
  id: {
    type: String,
    default: '1',
  },
})

watch(
  () => props.id,
  async (id) => {
    loggedUserStore.isLoading = true
    const patientResponse = await patientsStore.fetchPatient(props.id)
    if (0 == vaccinesStore.items.length) {
      const vaccineResponse = await vaccinesStore.fetchVaccines()
    }
    await dosesStore.fetchDoses()
    loggedUserStore.isLoading = false
  },
  { immediate: true }
)
</script>
