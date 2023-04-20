<template>
  <PageWrapper>
    <div class="pb-10">
  <div class="flex flex-col md:flex-row justify-center items-baseline pt-10">
    <div class="md:flex-1" style="margin-left: 10px;">
      <MapGoogle />
    </div>
    <div class="md:w-1/3">
      <div class="m-3">
        <ListCard />
      </div>
    </div>
  </div>
</div>

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
