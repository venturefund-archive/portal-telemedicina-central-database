<template>
  <!-- empty, because markers are not represented by DOM elements -->
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, inject, defineEmits } from 'vue'
import { usePatientsStore } from '@/stores/patients'
import { useMapStore } from '@/stores/map'
const mapStore = useMapStore()
const patientsStore = usePatientsStore()

const emit = defineEmits(['update:position'])

const props = defineProps({
  marker: Object,
})

const map = inject('map')
const geocoder = inject('geocoder')

let googleMarker = null

onMounted(() => {
  googleMarker = new google.maps.Marker({
    position: { lat: props.marker.address.latitude, lng: props.marker.address.longitude },
    map: map.value,
    draggable: false,
    icon: {
      url: props.marker.alerts.length > 0 ? 'marker-alert.svg' : 'marker.svg',
    },
  })

  googleMarker.addListener('click', () => {
    const infowindow = new google.maps.InfoWindow({
      content: getMarkerContent(props.marker, googleMarker.getDraggable()),
    })

    googleMarker.infowindow = infowindow
    infowindow.open(map.value, googleMarker)

    infowindow.addListener('domready', () => {
      const moveButton = document.querySelector(`#marker${props.marker.id}`)
      moveButton.addEventListener('click', () => {
        toggleMarkerMovement(googleMarker, props.marker)
      })
    })

    infowindow.addListener('closeclick', () => {
      if (googleMarker.getDraggable()) {
        toggleMarkerMovement(googleMarker, props.marker)
      }
    })
  })

  googleMarker.addListener('dragend', async (event) => {

    const latitude = event.latLng.lat()
    const longitude = event.latLng.lng()

    geocoder.value.geocode({ location: googleMarker.getPosition().toJSON() }, async (results, status) => {
    if (status === 'OK') {
      if (results[0]) {

        const updatedMarker = {
          address: [
            {
              id: 1,
              latitude,
              longitude,
              line: [results[0].formatted_address],
            },
          ],
        }
        emit('update:position', {payload: results[0].formatted_address, marker: props.marker})
        await mapStore.updateMarker(props.marker.id, updatedMarker)
        googleMarker.setDraggable(false)
        googleMarker.setIcon(props.marker.alerts.length > 0 ? 'marker-alert.svg' : 'marker.svg')
        googleMarker.infowindow.setContent(getMarkerContent(props.marker, false))
      } else {
        console.log('No results found')
      }
    } else {
      console.log('Geocoder failed due to: ' + status)
    }
  })


  })
})

watch(
  () => props.marker.position,
  () => {
    if (googleMarker) {
      googleMarker.setPosition(new google.maps.LatLng(props.marker.position.lat, props.marker.position.lng))
    }
  }
)

onUnmounted(() => {
  if (googleMarker) {
    googleMarker.setMap(null)
    googleMarker = null
  }
})

const getMarkerContent = (person, isMarkerMovable) => `
  <p>ID: ${person.id}</p>
  <p>Address: ${JSON.stringify(person.address.line)}</p>
  <p>Age: ${person.age_in_days}</p>
  <button id="marker${person.id}">${isMarkerMovable ? 'Cancel' : 'Move Marker'}</button>
`

const toggleMarkerMovement = (marker, person) => {
  if (marker.getDraggable()) {
    marker.setIcon(props.marker.alerts.length > 0 ? 'marker-alert.svg' : 'marker.svg')
    marker.setDraggable(false)
  } else {
    marker.setDraggable(true)
    marker.setIcon('marker-editing.svg')
    marker.infowindow.setContent(getMarkerContent(person, true))
  }
}
</script>
