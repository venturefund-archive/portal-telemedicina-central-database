<template>
  <PageWrapper title="Detalhes do patiente">
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
const loggedUserStore = useLoggedUserStore()
const patientsStore = usePatientsStore()
const vaccinesStore = useVaccinesStore()
const router = useRouter()

const props = defineProps({
  id: {
    type: String,
    default: '0',
  },
})

watch(
  () => props.id,
  async (id) => {
    if (props.id != 0) {
      loggedUserStore.isLoading = true
      const [vaccineResponse, patientResponse] = await Promise.all([
        patientsStore.fetchPatient(props.id),
        vaccinesStore.fetchVaccines()
      ])
      loggedUserStore.isLoading = false
    }
  },
  { immediate: true }
)
</script>
