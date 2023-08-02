<template>
  <div>
    <p class="mb-4 text-xl font-semibold text-gray-700">
      {{ $t('manager.vaccination-map') }}
    </p>
    <div class="!z-20 h-[106px] w-full rounded-t-2xl border !bg-gray-50 drop-shadow-lg">
      <div>
        <!-- People with vaccines delayed -->
        <div class="flex flex-col items-center justify-between space-y-5 md:flex-row md:space-x-5 md:space-y-0">
          <div class="flex items-center space-x-5">
            <div class="flex items-center space-x-2 p-7">
              <form @submit.prevent="searchAddress">
                <label for="default-search" class="sr-only">Procurar</label>
                <div class="relative flex items-center">
                  <svg
                    class="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 transform text-gray-500"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    ></path>
                  </svg>
                  <div>
                    <Input
                      :placeholder="$t('manager.search-map')"
                      v-model="geoCoderQuery"
                      class="w-full rounded-lg border py-2 pl-10 pr-3"
                    />
                  </div>
                </div>
              </form>
            </div>

            <!-- User List and Alerts -->
            <div class="flex items-center space-x-10">
              <div ref="dropdown" class="relative hidden">
                <button
                  @click="showList = !showList"
                  class="relative flex flex-col items-center rounded-md px-4 py-2 text-gray-500"
                >
                  <UsersIcon title="{{ $t('manager.population') }}" class="h-6 w-6 text-gray-500" />
                  <span class="text-sm">{{ $t('manager.population') }}</span>
                </button>
                <ul v-if="showList" class="absolute z-10 w-40 rounded-md bg-white shadow-md">
                  <li
                    v-for="item in items"
                    :class="{ 'font-bold': item === selectedItem }"
                    class="w-full cursor-pointer px-4 py-2 font-normal capitalize hover:bg-gray-100"
                    :key="item"
                  >
                    {{ item }}
                  </li>
                </ul>
              </div>

              <div class="flex flex-col items-center rounded-md px-4 py-2 text-gray-500">
                <Switch
                  v-model="onlyAlerts"
                  :class="onlyAlerts ? 'bg-green-500' : 'bg-gray-200'"
                  class="relative inline-flex h-5 w-12 items-center rounded-full"
                >
                  <span
                    :class="onlyAlerts ? 'translate-x-6' : 'translate-x-0'"
                    class="inline-block h-6 w-6 transform rounded-full border border-gray-300 bg-white shadow transition"
                  ></span>
                </Switch>
                <span class="pt-2 text-sm">{{ $t('manager.alerts') }}</span>
              </div>
              <div class="hidden flex flex-col items-center rounded-md px-4 py-2 text-gray-300 cursor-not-allowed">
                <TableIcon class="w-8 h-8"/>
                <span>{{ $t('manager.visualization') }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div ref="mapContainer" class="map-container"></div>
      <Marker
        v-for="marker in filteredMarkers"
        :key="marker.id"
        :marker="marker"
        :is-open="marker.id == props.patientCursor"
        @update:position="updateMarkerPosition"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, onUnmounted, provide, computed, watch, watchEffect } from 'vue'
import { useI18n } from 'vue3-i18n'
import { HandIcon, PencilIcon, SaveIcon } from '@heroicons/vue/solid'
import { MapIcon, TableIcon, UsersIcon, XIcon } from '@heroicons/vue/outline'
import { useMapStore } from '@/stores/map'
import { useLoggedUserStore } from '@/stores/loggedUser'
import { Switch } from '@headlessui/vue'
const { t } = useI18n()

const loggedUserStore = useLoggedUserStore()
const polygons = ref([])
const mapContainer = ref(null)
const map = ref(null)
const geocoder = ref(null)
const mapStore = useMapStore()
const isMapView = ref(true)
const showList = ref(false)
const dropdown = ref(null)
const onlyAlerts = ref(false)

const emit = defineEmits(['update:markers-in-view', 'update:onlyAlerts', 'geoCoderReady', 'centralize-on-location'])

const props = defineProps({
  center: {
    type: Object,
    default: null,
  },
  zoom: {
    type: Number,
    default: 5,
  },
  markers: {
    type: Array,
    default: [],
  },
  patientCursor: {
    type: String,
    default: '0',
  },
  areaCursor: {
    type: String,
    default: '0',
  },
})

const markersInView = ref(props.markers || [])
const getMarkersInView = () => {
  const mapBounds = map.value.getBounds()
  markersInView.value = filteredMarkers.value.filter((marker) => {
    return mapBounds.contains({ lat: marker.address.latitude, lng: marker.address.longitude })
  })
  emit('update:markers-in-view', markersInView.value)
}

watch(onlyAlerts, (newOnlyAlerts, oldValue) => {
  emit('update:onlyAlerts', newOnlyAlerts)
})

watch(
  () => props.center,
  async (center) => {
    if (map.value) {
      if (map.value.getZoom() == props.zoom) {
        map.value.setZoom(map.value.getZoom() - 0.5)
      }
      setTimeout(() => {
        map.value.setZoom(props.zoom)
        map.value.panTo(center)
      }, 250)
    }
  }
)
watch(
  () => props.patientCursor,
  async (patientCursor) => {
    if (map.value && 0 != patientCursor) {
      // console.log('Tracking patient id: '+ patientCursor)
      const index = props.markers.findIndex((marker) => marker.id === patientCursor)
      const patient = props.markers[index]
      emit('centralize-on-location', { ...patient.address, newPatientCursor: patient.id })
    }
  }
)
watch(
  () => props.areaCursor,
  async (areaCursor) => {
    if (map.value && mapStore.polygons.length > 0 && 0 != areaCursor) {
      // console.log('Tracking area areaCursor: ' + areaCursor)
      const index = mapStore.polygons.findIndex((polygon) => {
        return polygon.id == areaCursor
      })
      if(-1 != index) {
        const polygon = mapStore.polygons[index]
        const googlePolygon = getPolygonCenter(new google.maps.Polygon({
          paths: polygon.coordinates,
        }))
        const latitude = googlePolygon.lat()
        const longitude = googlePolygon.lng()
        emit('centralize-on-location', { latitude, longitude, newAreaCursor: `${polygon.id}` })
      }else{
        console.log('area not found')
      }
    }
  }
)

const toggleView = () => {
  isMapView.value = !isMapView.value
}

const handleOutsideClick = (event) => {
  if (!dropdown.value.contains(event.target)) {
    showList.value = false
  }
}

onBeforeUnmount(() => {
  document.removeEventListener('click', handleOutsideClick)
})

const items = computed(() => [
  t('manager.all-group'),
  t('manager.pragnant-group'),
  t('manager.puerp-group'),
  t('manager.newborn-group'),
  t('manager.firstchild-group'),
  t('manager.secondchild-group'),
  t('manager.thirdchild-group'),
  t('manager.teenager-group'),
])
provide('map', map)
provide('geocoder', geocoder)

const geoCoderQuery = ref(
  loggedUserStore.item.client && loggedUserStore.item.client.city
    ? loggedUserStore.item.client.city.charAt(0).toUpperCase() + loggedUserStore.item.client.city.slice(1)
    : 'São Paulo'
)

const showEmptyResult = ref(false)
const searchAddress = () => {
  geocodeAddress(geoCoderQuery.value)
}
const geocodeAddress = (query) => {
  geocoder.value.geocode({ address: query }, function (results, status) {
    if (status === 'OK') {
      if (map.value) {
        map.value.setCenter(results[0].geometry.location)
      }
      // showEmptyResult.value = false
      //const marker = new google.maps.Marker({
      //  map: resultsMap,
      //  position: results[0].geometry.location
      //})
      return results[0].geometry.location
    } else {
      // showEmptyResult.value = true
    }
  })
}

onUnmounted(() => {
  // polygonData.polygon.setMap(null);
  // polygonData.infoWindow.close();
  // if (polygonData.label) {
  //   polygonData.label.setMap(null);
  // }
  polygons.value = []
})

onMounted(async () => {
  document.addEventListener('click', handleOutsideClick)
  await initializeMap()
})

const createLoadedPolygon = (polygonData) => {
  const polygon = new google.maps.Polygon({
    paths: polygonData.coordinates,
    map: map.value,
    strokeColor: '#166534',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: '#fb923c',
    fillOpacity: 0.35,
  })

  const infoWindow = new google.maps.InfoWindow()

  const tempDiv = document.createElement('div')
  tempDiv.innerHTML = `
  <div class="flex flex-col">
      <div class="sticky top-0 bg-white">
        <h3 class="font-bold text-lg text-center text-gray-700">${t('manager.edit-info')}</h3>
        <hr class="mb-4 mt-1 w-full border border-dashed" />
      </div>
      <input type="text" placeholder="${t('manager.region-name')}" class="border border-gray-200 focus:ring-0 focus:border focus:border-green-500 bg-white h-10 px-5 pr-16 rounded-lg text-sm mb-4">
      <div class="flex justify-between">
        <button id="deleteButton"class="mx-2 gap-2 focus:outline-none text-base font-semibold py-2 bg-white rounded-md border text-red-500 hover:text-white border-red-500 hover:bg-red-500 px-6">${t(
          'manager.delete'
        )}</button>
        <button id="saveButton" class="mx-2 gap-2 focus:outline-none text-base font-semibold py-2 hover:bg-green-600 rounded-md border text-white  border-green-500 bg-green-500 px-6">${t(
          'manager.save'
        )}</button>
      </div>
    </div>
  `

  const nameInput = tempDiv.querySelector('input')
  const saveButton = tempDiv.querySelector('#saveButton')
  const deleteButton = tempDiv.querySelector('#deleteButton')

  const polygonObj = {
    polygon,
    infoWindow,
    name: polygonData.name,
    label: null,
  }

  google.maps.event.addListener(polygon, 'click', () => {
    infoWindow.setPosition(getPolygonCenter(polygon))
    infoWindow.open(map.value)
  })

  saveButton.addEventListener('click', async () => {
    polygonObj.name = nameInput.value
    updatePolygonLabel(polygonObj)
    await mapStore.updatePolygon(polygonData.id, {
      name: polygonObj.name,
      coordinates: polygon
        .getPath()
        .getArray()
        .map((latLng) => {
          return [latLng.lng(), latLng.lat()]
        }),
    })
    infoWindow.close()
  })

  deleteButton.addEventListener('click', () => {
    polygonObj.id = polygonData.id
    deletePolygon(polygonObj)
  })

  infoWindow.setContent(tempDiv)

  updatePolygonLabel(polygonObj)

  return polygonObj
}

const initializeMap = async () => {
  geocoder.value = new google.maps.Geocoder()
  emit('geoCoderReady', geocoder.value)
  map.value = new google.maps.Map(mapContainer.value, {
    zoom: props.zoom,
    center: geocodeAddress(geoCoderQuery.value),
  })
  map.value.addListener('idle', () => {
    if(map.value.getBounds()){
      getMarkersInView()
    }
  })

  const drawingManager = new google.maps.drawing.DrawingManager({
    drawingMode: null,
    drawingControl: true,
    drawingControlOptions: {
      position: google.maps.ControlPosition.TOP_CENTER,
      drawingModes: [google.maps.drawing.OverlayType.POLYGON],
    },
    polygonOptions: {
      editable: false,
      draggable: false,
    },
  })
  drawingManager.setMap(map.value)

  google.maps.event.addListener(drawingManager, 'overlaycomplete', (event) => {
    const polygon = event.overlay
    createPolygonInfoWindow(polygon)
    drawingManager.setDrawingMode(null)
  })

  await mapStore.fetchPolygons()
  mapStore.polygons.forEach((polygonData) => {
    const polygonObj = createLoadedPolygon(polygonData)
    polygons.value.push(polygonObj)
  })
}

// const maxMarkersToProcess = 30
const filteredMarkers = computed(() => {
  return props.markers.filter((marker, index) => {
    // if (index >= maxMarkersToProcess) {
    //   return false
    // }
    const hasLatitude = marker.address && marker.address.latitude
    const hasAlerts = marker.alerts && marker.alerts.length > 0

    // Quando onlyAlerts.value for true, considerar apenas pacientes que possuem latitude e alerts.
    // Quando onlyAlerts.value for false, considerar apenas pacientes que possuem latitude.
    return onlyAlerts.value ? hasLatitude && hasAlerts : hasLatitude
  })
})

const updateMarkerPosition = ({ payload, marker }) => {
  marker.address.formatted_address = payload
}

const createPolygon = (polygonData) => {
  const polygon = new google.maps.Polygon({
    paths: polygonData.coordinates,
    map: map.value,
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: '#FF0000',
    fillOpacity: 0.35,
  })

  // Aqui você poderia adicionar qualquer outro código para adicionar eventos de clique, janelas de informação, etc., se necessário.

  return polygon
}

const createPolygonInfoWindow = (polygon, openImmediately = true) => {
  const infoWindow = new google.maps.InfoWindow()

  const tempDiv = document.createElement('div')
  tempDiv.innerHTML = `
    <div class="flex flex-col">
      <div class="sticky top-0 bg-white">
        <h3 class="font-bold text-lg mb-2">${t('manager.edit-info')}</h3>
        <hr class="my-3 w-full border border-dashed" />
      </div>
      <input type="text" class="border border-gray-300 bg-white h-10 px-5 pr-16 rounded-lg text-sm focus:ring-0 focus:border focus:border-green-500 mb-4">
      <div class="flex justify-between">
        <button id="deleteButton" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">${t(
          'manager.delete'
        )}</button>
        <button id="saveButton" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">${t(
          'manager.save'
        )}</button>
      </div>
    </div>
  `

  const nameInput = tempDiv.querySelector('input')
  const saveButton = tempDiv.querySelector('#saveButton')
  const deleteButton = tempDiv.querySelector('#deleteButton')

  const polygonData = {
    polygon,
    infoWindow,
    name: '',
    label: null,
  }

  saveButton.addEventListener('click', async () => {
    polygonData.name = nameInput.value
    await mapStore.createPolygon({
      name: polygonData.name,
      coordinates: polygonData.polygon
        .getPath()
        .getArray()
        .map((latLng) => {
          return [latLng.lng(), latLng.lat()]
        }),
    })
    updatePolygonLabel(polygonData)
    infoWindow.close()
  })

  deleteButton.addEventListener('click', () => {
    deletePolygon(polygonData)
  })

  infoWindow.setContent(tempDiv)

  if (openImmediately) {
    infoWindow.setPosition(polygon.getPath().getAt(0))
    infoWindow.open(map.value)
  }
  nameInput.value = polygonData.name

  google.maps.event.addListener(polygon, 'click', () => {
    infoWindow.open(map.value)
    nameInput.value = polygonData.name // set the current name in the input field
  })

  polygons.value.push(polygonData)
}

const updatePolygonLabel = (polygonData) => {
  if (polygonData.label) {
    polygonData.label.setMap(null)
  }

  const labelContent = `
    ${polygonData.name}
  `

  const label = new google.maps.Marker({
    position: getPolygonCenter(polygonData.polygon),
    map: map.value,
    icon: {
      url:
        'data:image/svg+xml;charset=UTF-8,' +
        encodeURIComponent(`
        <svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"></svg>
      `),
      labelOrigin: new google.maps.Point(0, -12),
    },
    label: {
      text: labelContent,
      color: 'black',
      fontSize: '16px',
      fontWeight: 'bold',
    },
    clickable: false,
  })

  polygonData.label = label
}

const getPolygonCenter = (polygon) => {
  const bounds = new google.maps.LatLngBounds()
  polygon.getPath().forEach((point) => {
    bounds.extend(point)
  })
  return bounds.getCenter()
}
const deletePolygon = async (polygonData) => {
  const index = polygons.value.indexOf(polygonData)
  if (index !== -1) {
    if (polygonData.id) {
      try {
        await mapStore.deletePolygon(polygonData.id)
      } catch (err) {
        console.log(err)
        errorToast({ text: err.message })
        return
      }
    }

    const polygon = polygonData.polygon
    polygon.setMap(null)
    polygonData.infoWindow.close()
    if (polygonData.label) {
      polygonData.label.setMap(null)
    }
    polygons.value.splice(index, 1)
  }
}
</script>

<style scoped>
.map-container {
  height: 780px;
  width: 100%;
}
</style>
