<template>
  <PageWrapper>
    <div class="pb-10">
      <div class="flex items-baseline justify-center py-10">
        <div class="mr-4 md:flex-1">
          <MapGoogle
            :patients="markers"
            @update:markers-in-view="updateMarkersFiltered"
            :center="currentCenter"
            :zoom="currentZoom"
          />
        </div>
        <div class="md:w-1/3">
          <div class="m-3">
            <PatientListCard
              :patients="filteredMarkers"
              @update:markers-in-search="updateMarkersFiltered"
              @centralize-on-location="updateCenterInView"
            />
          </div>
        </div>
      </div>
    </div>
  </PageWrapper>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import MapGoogle from '@/components/organisms/MapGoogle.vue'
import PatientListCard from '@/components/organisms/PatientListCard.vue'
import { usePatientsStore } from '@/stores/patients'
const patientsStore = usePatientsStore()

const markers = ref([])
const filteredMarkers = ref([])
onMounted(async () => {
  await patientsStore.fetchPatients()
  markers.value = filteredMarkers.value = patientsStore.items
})

const currentCenter = ref(undefined)
const currentZoom = ref(undefined)

// Função para atualizar os marcadores em vista
const updateMarkersFiltered = (newMarkers) => {
  filteredMarkers.value = newMarkers
}
// Função para atualizar o centro em vista
const updateCenterInView = (newCenter) => {
  currentCenter.value = newCenter
  currentZoom.value = 9
}
</script>
