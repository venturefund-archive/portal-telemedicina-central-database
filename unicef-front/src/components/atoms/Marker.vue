<template>
  <!-- empty, because markers are not represented by DOM elements -->
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, inject, defineEmits, provide } from 'vue'
import { usePatientsStore } from '@/stores/patients'
import { useMapStore } from '@/stores/map'
import { HandIcon, PencilIcon, SaveIcon } from '@heroicons/vue/solid'
import { MapIcon, TableIcon, UsersIcon, XIcon } from '@heroicons/vue/outline'
import { useI18n } from 'vue3-i18n'
import {
  parseISO,
  formatRelative,
  formatDuration,
  add,
  setDefaultOptions,
  differenceInMonths,
  format,
  differenceInYears,
  differenceInDays,
} from 'date-fns'

const mapStore = useMapStore()
const patientsStore = usePatientsStore()
const { t } = useI18n()
const emit = defineEmits(['update:position'])

const props = defineProps({
  marker: Object,
  isOpen: Boolean,
})

watch(
  () => props.isOpen,
  (newValue) => {
    if (newValue) {
      const infowindow = new google.maps.InfoWindow({
        content: getMarkerContent(props.marker, googleMarker.getDraggable()),
      })

      googleMarker.infowindow = infowindow
      infowindow.open(map.value, googleMarker)
      currentInfoWindow = infowindow // Atualiza o InfoWindow aberto atualmente

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
    } else if (currentInfoWindow) {
      currentInfoWindow.close()
      currentInfoWindow = null
    }
  },
)

const map = inject('map')
const geocoder = inject('geocoder')

let googleMarker = null

let currentInfoWindow = null // Variável para manter o controle do InfoWindow aberto atualmente

onMounted(() => {
  googleMarker = new google.maps.Marker({
    position: { lat: props.marker.address.latitude, lng: props.marker.address.longitude },
    map: map.value,
    draggable: false,
    icon: {
      url: props.marker.alerts.length > 0 ? '/marker-alert.svg' : '/marker.svg',
    },
  })

  googleMarker.addListener('click', () => {
    // Fecha o InfoWindow anterior, se existir
    if (currentInfoWindow) {
      currentInfoWindow.close()
    }

    const infowindow = new google.maps.InfoWindow({
      content: getMarkerContent(props.marker, googleMarker.getDraggable()),
    })

    googleMarker.infowindow = infowindow
    infowindow.open(map.value, googleMarker)
    currentInfoWindow = infowindow // Atualiza o InfoWindow aberto atualmente

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
          emit('update:position', { payload: results[0].formatted_address, marker: props.marker })
          await mapStore.updateMarker(props.marker.id, updatedMarker)
          googleMarker.setDraggable(false)
          googleMarker.setIcon(props.marker.alerts.length > 0 ? '/marker-alert.svg' : '/marker.svg')
          googleMarker.infowindow.setContent(getMarkerContent(props.marker, false))
          // currentInfoWindow.close();
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
  <div id="content" class="min-w-96 w-96">
    <div id="bodyContent" class="w-auto">
      <div class="rounded-lg px-3">
        <header class="sticky top-0 bg-white pb-2">
          <div>
          <h2 class="text-xl font-semibold capitalize">${person.name.toLowerCase()}</h2>

          <p class="text-sm text-gray-500">
            ID: ${person.id}
          </p>
          <hr class="my-2 w-full border border-dashed" />
        </header>

        <div class="">

          <div class="flex justify-between pb-2">
            <span class="mr-2 inline-block rounded-full bg-gray-100 px-3 py-1 text-sm lowercase text-black">
              ${formatAge(person.age_in_days)}
            </span>
            <p class="text-sm">
              <span
                class="mr-2 inline-block rounded-full px-3 py-1 text-sm"
                style="background-color: ${person.number_of_alerts_by_protocol > 0 ? '#f87171' : '#f3f4f6'}; color: ${
  person.number_of_alerts_by_protocol > 0 ? 'white' : 'black'
}">${person.number_of_alerts_by_protocol}
${person.number_of_alerts_by_protocol === 1 ? t('manager.alert-protocol') : t('manager.alerts-protocol')}</span>
            </p>
          </div>

          ${
            (0 !== person.alerts.length &&
              `
          <div class="inline-block pb-2">
              <p class="pt-1 text-sm font-medium text-gray-600">${t('manager.vaccine-delay')}:</p>
              ${person.alerts
                .map(
                  (alert) => `
                <span
                  class="mr-2 mt-1 inline-block rounded-full bg-red-100 px-3 py-1 text-xs text-red-900"
                >
                  ${alert}
                  </span>
                  `
                )
                .join('')}
                  </div>
                  </div>
            `) ||
            ''
          }

          <div class="pt-1 flex">
            <p class="pr-1 text-sm font-medium text-gray-600"> ${t('manager.birthdate')}:</p>
            <p class="text-sm">
              ${format(new Date(person.birth_date), 'dd/MM/yyyy')}
            </p>
          </div>
          ${
            (person.address.formatted_address &&
              `
          <div class="flex flex-col py-2">
            <p class="pr-1 text-sm font-medium text-gray-600"> ${t('manager.address')}: </p>
            <p class="text-sm">
              ${person.address.formatted_address}
            </p>
          </div>`) || ''}
        </div>
      </div>

      <div class="sticky bottom-0 bg-white pt-2 pb-1">
      <div class="flex justify-evenly">
        <button
          type="button"
          class="mx-2 gap-2 focus:outline-none text-base font-semibold py-2 bg-white rounded-md border text-green-500 hover:text-white border-green-500 hover:bg-green-500 px-6"
          id="marker${person.id}"
        >
          ${isMarkerMovable ? t('manager.cancel') : t('manager.move')}
        </button>

        <button
          disabled="true"
          type="button"
          class="mx-2 gap-2 focus:outline-none text-base font-semibold py-2 bg-white rounded-md border disabled:border-gray-400 disabled:text-gray-400 disabled:opacity-75 disabled:cursor-not-allowed  disabled:hover:bg-white text-green-500 hover:text-white border-green-500 hover:bg-green-500 px-6"
          id="marker${person.id}"
        >
        ${t('manager.edit')}
        </button>
      </div>
      </div>
    </div>
  </div>
`

function formatAge(age_in_days) {
  const today = new Date()
  // Criamos uma nova data baseada na quantidade de dias recebidos
  const birthDate = new Date(today - age_in_days * 24 * 60 * 60 * 1000)

  const years = differenceInYears(today, birthDate)
  const months = differenceInMonths(today, birthDate) % 12
  const days = differenceInDays(today, birthDate) % 30 // Aproximando meses a 30 dias

  // Formatação de acordo com os critérios estabelecidos
  if (years === 1) {
    return `1 ${t('patient-details.year')}`
  } else if (years > 1) {
    return `${years} ${t('patient-details.years')}`
  } else if (months === 1) {
    return `1 ${t('patient-details.month')}`
  } else if (months > 1) {
    return `${months} ${t('patient-details.months')}`
  } else if (days === 1) {
    return `1 ${t('patient-details.day')}`
  } else {
    return `${days} ${t('patient-details.days')}`
  }
}

const toggleMarkerMovement = (marker, person) => {
  if (marker.getDraggable()) {
    marker.setIcon(props.marker.alerts.length > 0 ? '/marker-alert.svg' : '/marker.svg')
    marker.setDraggable(false)
  } else {
    marker.setDraggable(true)
    marker.setIcon('/marker-editing.svg')
    marker.infowindow.setContent(getMarkerContent(person, true))
  }
}
</script>
