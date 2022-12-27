<template>
  <PageWrapper title="Patient Details">
    <div v-if="patientsStore.item && props.id" :key="forceRerender">
      <ProfileCard :id="id" />
      <VaccinesList />
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

const forceRerender = ref(0)

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
      forceRerender.value++
    }
  },
  { immediate: true }
)
</script>
