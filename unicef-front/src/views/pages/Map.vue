<template>
  <PageWrapper title="Mapa do Gestor">
    <div class="pb-10">
    <Notification />
  </div>
    <div class="pl-10">
    <ListCard/>
  </div>
    <MapGoogle />
  </PageWrapper>
</template>

<script setup>
import { onMounted } from 'vue'
import MapGoogle from '@/components/organisms/MapGoogle.vue'
import { usePatientsStore } from '@/stores/patients'
const patientsStore = usePatientsStore()

const props = defineProps({
  id: {
    type: String,
    default: '4623',
  },
})

onMounted(async () => {
  if (props.id && props.id != 0) {
    await patientsStore.fetchPatient(props.id)
  }
})
</script>
