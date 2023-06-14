<template>
  <PageWrapper>
    <div class="pb-10">
      <div class="flex items-baseline justify-center py-10">
        <div class="mr-4 md:flex-1">
          <MapGoogle
            :patients="markers"
            @update:markers-in-view="updateMarkersFiltered"
            @update:onlyAlerts="updateOnlyAlerts"
            @dragend="handleMarkerDrag"
            @geoCoderReady="handleGeoCoderReady"
            :center="currentCenter"
            :zoom="currentZoom"
            :patientCursor="patientCursor"
          />
        </div>
        <div class="m-3 h-[59rem] md:w-1/3">
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
import MapGoogle from '@/components/organisms/MapGoogle.vue'
import PatientListCard from '@/components/organisms/PatientListCard.vue'
const patientsStore = usePatientsStore()
const vaccinesStore = useVaccinesStore()
const router = useRouter()
const dosesStore = useDosesStore()

const props = defineProps({
  id: {
    type: String,
    default: '0',
  },
})

watch(
  () => props.id,
  async (id) => {
    0 != props.id && (await patientsStore.fetchPatient(props.id))
  },
  { immediate: true }
)

const markers = ref([])
const onlyAlerts = ref(undefined)
const filteredMarkers = ref([])

onMounted(async () => {
  await patientsStore.fetchPatients()
  markers.value = filteredMarkers.value = patientsStore.items
})
const geoCoder = ref(null)
const handleGeoCoderReady = (geoCoder2) => {
  geoCoder.value = geoCoder2
}
watch(filteredMarkers, (newMarkers, oldMarkers) => {
  if (!geoCoder.value) {
    return
  }
  filteredMarkers.value.slice(0, 9).map((patient, k) => {
    geoCoder.value.geocode(
      { location: { lat: patient.address.latitude, lng: patient.address.longitude } },
      function (results, status) {
        if (status === 'OK') {
          const address = results[0].formatted_address
          filteredMarkers.value[k].address.formatted_address = address
        } else {
          showEmptyResult.value = true
        }
      }
    )
  })
})

const currentCenter = ref(undefined)
const currentZoom = ref(16)

const updateMarkersFiltered = (newMarkers) => {
  filteredMarkers.value = newMarkers
}

const patientCursor = ref(null)
const updateCenterInView = ({ latitude, longitude, newPatientCursor }) => {
  console.log({ latitude, longitude, newPatientCursor })
  currentCenter.value = { lat: latitude, lng: longitude }
  currentZoom.value = 19
  patientCursor.value = newPatientCursor
}

const updateOnlyAlerts = (newOnlyAlerts) => {
  onlyAlerts.value = newOnlyAlerts
}

const handleMarkerDrag = ({ patientId, latitude, longitude }) => {
  markers.value.find((p) => patientId == p.id).address.latitude = latitude
  markers.value.find((p) => patientId == p.id).address.longitude = longitude
}
</script>
