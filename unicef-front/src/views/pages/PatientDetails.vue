<template>
  <PageWrapper>
    <div v-if="patientsStore.item && props.id">
      <VaccinesList :id="id" :no-menubar="props.noMenubar" />
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
  noMenubar: {
    type: Boolean,
    default: false,
  },
})

const state = useStorage('app-store', { token: '' })
watch(
  () => props.id,
  async (newId) => {
    loggedUserStore.isLoading = true
    console.log('newId', newId)
    console.log('props.id', props.id)

    const id = props.id ? props.id : state.value.patientLastViewed
    console.log('id', id)
    const patientResponse = await patientsStore.fetchPatient(id)
    if (0 == vaccinesStore.items.length) {
      const vaccineResponse = await vaccinesStore.fetchVaccines()
    }
    await dosesStore.fetchDoses()
    loggedUserStore.isLoading = false
  },
  { immediate: true }
)
</script>
