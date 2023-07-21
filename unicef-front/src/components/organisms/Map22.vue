<template>
  <div>
    <div class="!z-50 h-[106px] w-full rounded-t-2xl border !bg-gray-50 drop-shadow-lg drop-shadow-lg">
      <div>
        <!-- People with vaccines delayed -->
        <div class="flex flex-col items-center justify-between space-y-5 p-5 md:flex-row md:space-y-0 md:space-x-5">
          <div class="flex items-center space-x-5">
            <div class="flex items-center space-x-2">
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
                      class="w-full rounded-lg border py-2 pl-10 pr-3 focus:outline-none"
                    />
                  </div>
                </div>
              </form>
            </div>

            <!-- User List and Alerts -->
            <div class="flex items-center space-x-10">
              <div ref="dropdown" class="relative">
                <button
                  @click="showList = !showList"
                  class="relative flex flex-col items-center rounded-md py-2 px-4 text-gray-500"
                >
                  <UsersIcon title="{{ $t('manager.population') }}" class="h-6 w-6 text-green-500" />
                  <span class="text-sm">{{ $t('manager.population') }}</span>
                </button>
                <ul v-if="showList" class="absolute z-10 w-40 rounded-md bg-white shadow-md">
                  <li
                    v-for="item in items"
                    :class="{ 'font-bold': item === selectedItem }"
                    class="w-full cursor-pointer py-2 px-4 font-normal capitalize hover:bg-gray-100"
                    :key="item"
                  >
                    {{ item }}
                  </li>
                </ul>
              </div>

              <div class="flex flex-col items-center rounded-md py-2 px-4 text-gray-500">
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
            </div>
          </div>
        </div>
      </div>
      <div ref="mapContainer" class="map-container"></div>
      <Marker
        v-for="marker in filteredMarkers"
        :key="marker.id"
        :marker="marker"
        @update:position="updateMarkerPosition"
      />
      <!-- <Polygon
      v-for="polygon in polygons"
      :key="polygon.id"
      :polygon="polygon"
      @update:position="updatePolygonPosition(polygon)"
    /> -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, onUnmounted, provide, computed, watch } from 'vue'
import { useI18n } from 'vue3-i18n'
import { HandIcon, PencilIcon, SaveIcon } from '@heroicons/vue/solid'
import { MapIcon, TableIcon, UsersIcon, XIcon } from '@heroicons/vue/outline'
import { usePatientsStore } from '@/stores/patients'
const patientsStore = usePatientsStore()
import { useMapStore } from '@/stores/map'
import { useLoggedUserStore } from '@/stores/loggedUser'
import { Switch } from '@headlessui/vue'
const { t } = useI18n()

const loggedUserStore = useLoggedUserStore()
const markers = ref([])
const polygons = ref([])
const mapContainer = ref(null)
const map = ref(null)
const geocoder = ref(null)
const mapStore = useMapStore()
const isMapView = ref(true)
const showList = ref(false)
const dropdown = ref(null)
const onlyAlerts = ref(false)

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
const currentCenter = ref(undefined)
const showEmptyResult = ref(false)
const searchAddress = () => {
  geocodeAddress()
}
const geocodeAddress = () => {
  geocoder.value.geocode({ address: geoCoderQuery.value }, function (results, status) {
    if (status === 'OK') {
      if(map.value){
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
  await loadPolygons()
})

const loadPolygons = async () => {
  try {
    const loadedPolygons = await mapStore.fetchPolygons()
    loadedPolygons.forEach((polygonData) => {
      const polygonObj = createLoadedPolygon(polygonData)
      polygons.value.push(polygonObj)
    })
  } catch (error) {
    console.error('Erro ao carregar polígonos:', error)
  }
}

const createLoadedPolygon = (polygonData) => {
  const polygon = new google.maps.Polygon({
    paths: polygonData.coordinates,
    map: map.value,
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: '#FF0000',
    fillOpacity: 0.35,
  })

  const infoWindow = new google.maps.InfoWindow()
  const nameInput = document.createElement('input')
  const saveButton = document.createElement('button')
  const deleteButton = document.createElement('button')

  nameInput.type = 'text'
  nameInput.value = polygonData.name
  saveButton.textContent = 'Save'
  deleteButton.textContent = 'Delete'

  const content = document.createElement('div')
  content.appendChild(nameInput)
  content.appendChild(saveButton)
  content.appendChild(deleteButton)

  const polygonObj = {
    polygon,
    infoWindow,
    name: polygonData.name,
    label: null,
  }

  // Click event listener
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

  infoWindow.setContent(content)

  // Add label
  updatePolygonLabel(polygonObj)

  return polygonObj
}

const initializeMap = async () => {
  geocoder.value = new google.maps.Geocoder()
  map.value = new google.maps.Map(mapContainer.value, {
    zoom: 14,
    center: geocodeAddress()
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

  await patientsStore.fetchPatients()
  // await patientsStore.fetchPatientsRecursive()
  markers.value = patientsStore.items
}

// const maxMarkersToProcess = 30
const filteredMarkers = computed(() => {
  return markers.value.filter((marker, index) => {
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
  marker.address.line = payload
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
  const nameInput = document.createElement('input')
  const saveButton = document.createElement('button')
  const deleteButton = document.createElement('button')

  nameInput.type = 'text'
  saveButton.textContent = 'Save'
  deleteButton.textContent = 'Delete'

  const content = document.createElement('div')
  content.appendChild(nameInput)
  content.appendChild(saveButton)
  content.appendChild(deleteButton)

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

  infoWindow.setContent(content)

  // Open infoWindow when polygon is created
  // Abra infoWindow quando o polígono for criado apenas se openImmediately for true
  if (openImmediately) {
    infoWindow.setPosition(polygon.getPath().getAt(0))
    infoWindow.open(map.value)
  }
  nameInput.value = polygonData.name

  // Add polygon click event listener
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
    try {
      console.log(polygonData)
      await mapStore.deletePolygon(polygonData.id)

      const polygon = polygonData.polygon
      polygon.setMap(null)
      polygonData.infoWindow.close()
      if (polygonData.label) {
        polygonData.label.setMap(null)
      }
      polygons.value.splice(index, 1)
    } catch (err) {
      console.log(err)
      errorToast({ text: err.message })
    }
  }
}
</script>

<style scoped>
.map-container {
  height: 500px;
  width: 100%;
}
</style>
