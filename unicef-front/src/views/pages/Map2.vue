<template>
  <PageWrapper>
    <div class="pb-10">
      <div class="flex items-baseline justify-center py-10">
        <div class="mr-4 md:flex-1">
          <Map22
            :markers="markers"
            @update:markers-in-view="updateMarkersFiltered"
            @update:onlyAlerts="updateOnlyAlerts"
            @geoCoderReady="handleGeoCoderReady"
            :center="currentCenter"
            :zoom="currentZoom"
            :patientCursor="patientCursor"
          />
        </div>
        <div class="m-3 md:w-1/3">
          <PatientListCard
            :patients="filteredMarkers"
            :onlyAlerts="onlyAlerts"
            @centralize-on-location="updateCenterInView"
          />
        </div>
      </div>
    </div>
  </PageWrapper>
</template>

<script setup>
import { onMounted, onUpdated, reactive, ref, inject, watch, onRenderTracked } from 'vue'
import Map22 from '@/components/organisms/Map22.vue'
import { usePatientsStore } from '@/stores/patients'
const patientsStore = usePatientsStore()
const currentCenter = ref(undefined)
const currentZoom = ref(16)

const markers = ref([])
const onlyAlerts = ref(undefined)
const filteredMarkers = ref([])

const isLoading = ref(false)
onMounted(async () => {
  isLoading.value = true
  if (patientsStore.items.length == 0) {
    await patientsStore.fetchPatients()
    await patientsStore.fetchPatientsRecursive()
  }
  markers.value = filteredMarkers.value = patientsStore.items
})
const geocoder = ref(null)
const handleGeoCoderReady = (geocoderLocal) => {
  geocoder.value = geocoderLocal
}
const updateMarkersFiltered = (newMarkers) => {
  // @TODO: Find a better place to calculate geocode
  newMarkers.map((newMarker, index) => {
    if(!newMarkers[index].address.formatted_address){
      console.log('processando geocode..')
      geocoder.value.geocode({ location: { lat: newMarker.address.latitude, lng: newMarker.address.longitude } }, async (results, status) => {
        if (status === 'OK') {
          if (results[0]) {
            newMarkers[index].address.formatted_address = results[0].formatted_address
          } else {
            console.log('No results found')
          }
        } else {
          console.log('Geocoder failed due to: ' + status)
        }
      })
    }else{
      //console.log('cache..')
    }
  })
  filteredMarkers.value = newMarkers
}

const updateOnlyAlerts = (newOnlyAlerts) => {
  onlyAlerts.value = newOnlyAlerts
}
const patientCursor = ref(null)
const updateCenterInView = async ({ latitude, longitude, newPatientCursor }) => {
  // console.log({ latitude, longitude, newPatientCursor })
  currentCenter.value = { lat: latitude, lng: longitude }
  currentZoom.value = 18
  patientCursor.value = newPatientCursor
}
</script>
