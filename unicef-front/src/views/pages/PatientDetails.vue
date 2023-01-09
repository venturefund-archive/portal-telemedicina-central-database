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
const patientsStore = usePatientsStore()

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
      await patientsStore.fetchPatient(props.id)
    }
  },
  { immediate: true }
)
</script>
