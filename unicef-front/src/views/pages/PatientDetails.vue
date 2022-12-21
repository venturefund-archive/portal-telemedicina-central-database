<template>
  <PageWrapper title="Patient Details">
    <div v-if="patientsStore.item && props.id">
      <ProfileCard :id="id" />
      <VaccinesList />
    </div>
    <div v-else>
      <span class="flex justify-center text-neutral-500 text-lg">No Patient selected. Search for a patient...</span>
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
const patientsStore = usePatientsStore()


const props = defineProps({
  id: {
    type: String,
    default: '0',
  },
})

onMounted(async () => {
  if (props.id != 0)
    await patientsStore.fetchPatient(props.id)
})
onUpdated(async () => {
  if (props.id != 0)
    await patientsStore.fetchPatient(props.id)
})


function setIsOpen(value) {
  console.log('hit')
  isOpen.value = value
}
</script>
