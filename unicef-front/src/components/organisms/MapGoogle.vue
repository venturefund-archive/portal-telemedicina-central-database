<template>
  <div>
    <p class="mb-4 text-xl font-semibold text-gray-700">
      {{ isTableView ? $t('manager.table-view-text') : $t('manager.vaccination-map') }}
    </p>

    <div class="!z-50 h-[106px] w-full rounded-t-2xl border !bg-gray-50 drop-shadow-lg drop-shadow-lg">
      <div>
        <!-- People with vaccines delayed -->
        <div class="flex flex-col items-center justify-between space-y-5 p-5 md:flex-row md:space-y-0 md:space-x-5">
          <div class="flex items-center space-x-5">
            <div v-if="isTableView">
              <div class="flex">
                <input
                  type="date"
                  class="rounded-lg border border-gray-300 shadow focus:outline-none focus:ring focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-white"
                />
              </div>
            </div>
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
                  <div v-if="isTableView">
                    <Input
                      :placeholder="$t('manager.search')"
                      v-model="asd"
                      class="w-full rounded-lg border py-2 pl-10 pr-3 focus:outline-none focus:ring focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-white"
                    />
                  </div>
                  <div v-if="!isTableView">
                    <Input
                      :placeholder="$t('manager.search-map')"
                      v-model="geoCoderQuery"
                      class="w-full rounded-lg border py-2 pl-10 pr-3 focus:outline-none focus:ring focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-white"
                    />
                  </div>
                </div>
              </form>
            </div>

            <!-- User List and Alerts -->
            <div class="flex items-center space-x-10">
              <div>
                <button
                  @click="showList = !showList"
                  class="relative flex flex-col items-center rounded-md py-2 px-4 text-gray-500"
                >
                  <UsersIcon title="{{ $t('manager.population') }}" class="h-6 w-6 text-green-500" />
                  <span class="text-sm">{{ $t('manager.population') }}</span>
                </button>
                <ul v-if="showList" class="absolute z-50 -ml-8 rounded-md bg-white shadow-md">
                  <li
                    v-for="item in items"
                    :class="{ 'font-bold': item === selectedItem }"
                    class="cursor-pointer py-2 px-4 font-normal hover:bg-gray-100"
                    :key="item"
                  >
                    {{ item }}
                  </li>
                </ul>
              </div>

              <div v-if="!isTableView" class="flex flex-col items-center rounded-md py-2 px-4 text-gray-500">
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

              <div class="flex cursor-pointer items-center space-x-10">
                <button @click="toggleView" class="flex flex-col items-center">
                  <TableIcon v-if="!isTableView" class="h-8 w-9 text-gray-500" />
                  <MapIcon v-else class="h-7 w-10 text-gray-500" />
                  <span class="text-sm text-gray-500">Visualização</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Save Button -->
      <!-- <Button
            v-if="!isTableView"
            @click="savePolygons"
            class="border-gray-400 bg-transparent hover:bg-green-500 p-2 text-gray-400 shadow-md hover:border-green-500 hover:text-white"
          >
            <SaveIcon class="h-5 w-5" />
            <span class="text-sm">{{ $t('manager.save') }}</span>
          </Button> -->

      <!-- Toggle View Button -->

      <TableList v-show="isTableView" />
      <!-- Map content -->
      <div
        class="border-1 -z-10 flex justify-start border bg-white drop-shadow-lg"
        v-show="!isTableView && !showEmptyResult"
      >
        <GoogleMap
          :api-key="GOOGLE_MAP_API_KEY"
          style="width: 100%; height: 790px"
          id="map"
          :center="props.center"
          :zoom="props.zoom"
          :libraries="['drawing']"
          @idle="getMarkersInView"
          ref="mapRef"
        >
          <template #default="{ ready, api, map, mapTilesLoaded }"
            ><p v-if="!mapTilesLoaded">Loading</p>
            <!-- First pattern: Here you have access to the API and map instance.
          "ready" is a boolean that indicates when the Google Maps script
          has been loaded and the api and map instance are ready to be used -->
            <div v-for="(polygon, polygonIndex) in polygons" :key="polygonIndex">
              <Polygon
                ref="itemRefs"
                :options="{
                  paths: polygon.getPath(),
                  fillColor: '#FFA901',
                  strokeColor: '#4FA9DD',
                  fillOpacity: 0.5,
                  strokeWeight: 1,
                  clickable: false,
                  editable: true,
                  zIndex: 1,
                }"
              />
              <InfoWindow
                v-if="currentInfoWindowIndex === polygonIndex"
                ref="infoWindow"
                :options="{
                  position: calculatePolygonCenter(polygon.getPath()),
                }"
              >
                <MapInfoWindow
                  @delete="deletePolygon(polygonIndex)"
                  :polygonIndex="polygonIndex"
                  @saved="updateLabel"
                />
              </InfoWindow>
            </div>
            <MarkerCluster>
              <div v-for="(marker, i) in props.patients" :key="i">
                <Marker
                  v-if="(onlyAlerts && 0 != marker.alerts.length) || !onlyAlerts"
                  :ref="
                    (el) => {
                      markers[i] = el
                    }
                  "
                  :options="{
                    position: patientLocation(marker),
                    draggable: isDraggable(i),
                    icon: isDraggable(i)
                      ? markerIconEditing
                      : 0 !== marker.alerts.length
                      ? markerIconAlert
                      : markerIconNormal,
                    // opacity: isDraggable(i) ? 1 : 0.5
                  }"
                  @dragend="handleMarkerDrag($event, i)"
                >
                  <Teleport to=".notification-space">
                    <Popover v-slot="{ open }" class="">
                      <transition
                        enter-active-class="transition duration-200 ease-out"
                        enter-from-class="translate-y-1 opacity-0"
                        enter-to-class="translate-y-0 opacity-100"
                        leave-active-class="transition duration-150 ease-in"
                        leave-from-class="translate-y-0 opacity-100"
                        leave-to-class="translate-y-1 opacity-0"
                      >
                        <div>
                          <PopoverOverlay class="fixed inset-0 z-10 bg-black opacity-30" />
                          <PopoverPanel class="edit-panel z-20 mt-3 transform-gpu px-4">
                            <div class="overflow-hidden rounded-lg shadow-lg">
                              <div class="min-w-96 text-lg font-normal">
                                <div class="relative bg-neutral-50 p-4">
                                  <div class="">
                                    <h3 class="pb-3">Editing Patient #42</h3>
                                    <form @submit.prevent="">
                                      <div class="grid gap-6">
                                        <div class="space-y-1">
                                          <Label for="name" value="Name" />

                                          <Input
                                            id="name"
                                            type="text"
                                            placeholder="Name"
                                            class="block w-full"
                                            v-model="editForm.name"
                                            required
                                            autofocus
                                            autocapitalize="on"
                                            autocorrect="off"
                                          />
                                        </div>

                                        <div class="space-y-1">
                                          <Label for="document" value="Document" />

                                          <Input
                                            id="document"
                                            type="text"
                                            placeholder="xxxxx"
                                            class="block w-full"
                                            v-model="editForm.cidade"
                                            required
                                            autofocus
                                            autocapitalize="on"
                                            autocorrect="off"
                                          />
                                        </div>

                                        <div class="space-y-1">
                                          <Label for="address" value="Address" />

                                          <Input
                                            id="address"
                                            type="text"
                                            placeholder="Address"
                                            class="block w-full"
                                            v-model="editForm.cidade"
                                            required
                                            autofocus
                                            autocapitalize="on"
                                            autocorrect="off"
                                          />
                                        </div>

                                        <div>
                                          <Button
                                            type="submit"
                                            class="w-full justify-center gap-2"
                                            :disabled="editForm.processing"
                                            v-slot="{ iconSizeClasses }"
                                          >
                                            <span>Salvar</span>
                                          </Button>
                                        </div>
                                      </div>
                                    </form>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </PopoverPanel>
                        </div>
                      </transition>
                      <InfoWindow>
                        <div id="content">
                          <div id="bodyContent" class="p-1">
                            <div class="flex flex-col justify-between rounded-2xl bg-white p-5">
                              <!-- <pre>{{ marker }}</pre> -->
                              <router-link v-if="marker" :to="{ name: 'PatientDetails', params: { id: marker.id } }">
                                <p class="py-3 text-xl font-semibold capitalize">
                                  {{ marker && marker.name.toLowerCase() }}
                                </p>
                              </router-link>
                              <hr class="border-1 border border-dashed border-gray-300" />
                              <!-- <span>{{ marker && marker.number_of_alerts_by_protocol > 0 ?
                                'Com alertas' : 'Sem alertas' }}</span> -->
                              <div class="flex justify-between py-5">
                                <p
                                  class="justify-center rounded-full bg-gray-100 px-3 py-1 text-sm font-normal text-black"
                                >
                                  3 months
                                </p>
                                <p class="rounded-full bg-red-100 px-3 py-1 text-sm font-normal text-red-900">
                                  vaccine with delay: BCG
                                </p>
                              </div>
                              <div class="font-normal">
                                <p>Document: xxxx</p>
                                <p>Birthdate: xx/xx/xx</p>
                                <p>Address: xxxxx</p>
                              </div>
                              <span class="mt-5 flex justify-end text-sm text-gray-400"
                                >Última alteração: 08/02/2023</span
                              >
                            </div>

                            <div class="flex justify-evenly py-3">
                              <Button
                                type="submit"
                                variant="success-outline"
                                @click="moveMarker($event, i)"
                                class="mx-2 gap-2 focus:outline-none"
                                :disabled="editForm.processing"
                                v-slot="{ iconSizeClasses }"
                              >
                                <HandIcon aria-hidden="true" :class="iconSizeClasses" />
                                <span>Mover</span>
                              </Button>
                              <PopoverButton :focus="false" :class="{ 'relative z-30': open }">
                                <Button
                                  type="submit"
                                  variant="success"
                                  class="mx-2 gap-2 bg-white focus:outline-none"
                                  :disabled="editForm.processing"
                                  v-slot="{ iconSizeClasses }"
                                >
                                  <PencilIcon aria-hidden="true" :class="iconSizeClasses" />
                                  <span>Editar</span>
                                </Button>
                              </PopoverButton>
                            </div>
                          </div>
                        </div>
                      </InfoWindow>
                    </Popover>
                  </Teleport>
                </Marker>
              </div>
            </MarkerCluster>
          </template>
        </GoogleMap>
      </div>
      <div
        v-if="showEmptyResult"
        class="shadow-b-md shadow-l-md shadow-r-md flex flex-col rounded rounded-b-2xl border border-gray-200 bg-white py-60 shadow"
        style="min-height: 793px"
      >
        <div class="flex justify-center">
          <EmptyResultPhoto />
        </div>
        <span class="flex justify-center font-semibold">{{ $t('manager.no-results') }}</span>
        <span class="flex justify-center text-gray-500">{{ $t('manager.no-results-description') }}. </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineComponent, reactive, computed, onBeforeUpdate, onMounted, watch, ref, onUnmounted, createApp } from 'vue'
import { GoogleMap, Marker, CustomMarker, MarkerCluster, InfoWindow, Polygon } from 'vue3-google-map'
import { useGeolocation } from '@/composables/useGeolocation'
import { Popover, PopoverButton, PopoverPanel, PopoverOverlay } from '@headlessui/vue'
import { HandIcon, PencilIcon, SaveIcon } from '@heroicons/vue/solid'
import { MapIcon, TableIcon, UsersIcon } from '@heroicons/vue/outline'
import { useRouter } from 'vue-router'
import { usePatientsStore } from '@/stores/patients'
import { useStorage } from '@vueuse/core'
import { Switch } from '@headlessui/vue'

const enabled = ref(false)

import MapInfoWindow from '@/components/atoms/MapInfoWindow.vue'

const itemRefs = ref([])

const GOOGLE_MAP_API_KEY = ref(import.meta.env.VITE_GOOGLE_MAP_API_KEY)
const patientsStore = usePatientsStore()
const router = useRouter()
const map = ref(null)
const mapRef = ref(null)
const geoCoder = ref(null)
const onlyAlerts = ref(false)
const selectedItem = ref(null)
const drawingManager = ref(null)
const movingIndex = ref(null)

const props = defineProps({
  center: {
    type: Object,
    default: { lat: -22.74895, lng: -50.57253 },
  },
  zoom: {
    type: Number,
    default: 5,
  },
  patients: {
    type: Array,
    default: [],
  },
  combinedFilteredMarkers: {
    type: Array,
    default: [],
  },
})

const showList = ref(false)
const markerIconNormal = ref({
  url: 'marker-normal.png',
  scaledSize: {
    width: 40,
    height: 50,
  },
})
const markerIconEditing = ref({
  url: 'marker-editing.png',
  scaledSize: {
    width: 40,
    height: 50,
  },
})
const markerIconDisabled = ref({
  url: 'marker-disabled.png',
  scaledSize: {
    width: 40,
    height: 50,
  },
})
const markerIconAlert = ref({
  url: 'marker-alert.png',
  scaledSize: {
    width: 40,
    height: 50,
  },
})

const editForm = reactive({
  username: '',
  email: '',
  password1: '',
  password2: '',
  terms: false,
  processing: false,
})
const items = [
  'Todos',
  'Gestantes',
  'Puérperas',
  'Recém-nascidos',
  'Primeira infância',
  'Segunda infância',
  'Terceira Infância',
  'Adolescência',
]
const isTableView = ref(false)

const toggleView = () => {
  isTableView.value = !isTableView.value
}
const handleClickOutside = (event) => {
  if (!event.target.closest('.mt-4')) {
    // showList.value = false
  }
}

function onItemClick(item) {
  selectedItem.value = item
  console.log(`Item clicado: ${item}`)
}

const polygons = ref([])
// const customPolygons = (key) => {
//   return {
//     paths: polygons.value[key].polygon || [],
//     strokeColor: '#FF0000',
//     strokeOpacity: 0.8,
//     strokeWeight: 2,
//     fillColor: '#FF0000',
//     fillOpacity: 0.35,
//     editable: true
//   }
// }

const geoCoderQuery = ref('')
const showEmptyResult = ref(false)
const searchAddress = () => {
  //center.value = { lat: -22.749940, lng: -50.576540 }

  geocodeAddress(geoCoder.value, map.value)
}
const query = ref('')

function loadPolygons() {
  const state = useStorage('app-store', { polygons: [] })
  if (undefined == state.value.polygons) {
    state.value.polygons = []
  }
  if (state.value.polygons) {
    // asd.value = state.value.polygons
    state.value.polygons.forEach(function (polygonCoordinates, index) {
      // const polygon = new google.maps.Polygon({
      //   paths: polygonCoordinates,
      //   fillColor: '#FFA901',
      //   strokeColor: '#4FA9DD',
      //   fillOpacity: 0.5,
      //   strokeWeight: 1,
      //   clickable: false,
      //   editable: true,
      //   zIndex: 1,
      // })

      // // Detecta o evento de clique no mapa
      // google.maps.event.addListener(map.value, 'click', (event) => {
      //   // Verifica se o ponto do clique está dentro dos limites do polígono
      //   if (google.maps.geometry.poly.containsLocation(event.latLng, polygon)) {
      //     if (infoWindowsOpened.value.includes(index)) {
      //       return
      //     }
      //     //MapInfoWindow.emits = ['asd'];
      //     // var app = createApp(MapInfoWindow, { content: 'Seu conteúdo aqui' })
      //     // app.component('MapInfoWindow', MapInfoWindow);
      //     // const content = document.createElement('div')
      //     // console.log(MapInfoWindow)
      //     // app.mount(content, { asd: MapInfoWindow.emits.asd })

      //     const content = '<div id="asd"></div>'
      //     let infoWindow = new google.maps.InfoWindow({
      //       content: content,
      //       pixelOffset: new google.maps.Size(0, -30),
      //     })
      //     infoWindow.setPosition(center)
      //     infoWindow.addListener('closeclick', () => {
      //       infoWindowsOpened.value.splice(infoWindowsOpened.value.indexOf(index))
      //     })

      //     infoWindow.open(map.value)
      //     infoWindowsOpened.value.push(index)
      //   }
      // })

      polygons.value.push(polygon)
      // polygon.setMap(mapRef.value.map)
    })
  }
}

const currentInfoWindowIndex = ref(null)
const calculatePolygonCenter = (coords) => {
  const bounds = new google.maps.LatLngBounds()
  coords.forEach((coord) => {
    bounds.extend(coord)
  })
  return bounds.getCenter()
}
const showInfoWindow = (index) => {
  currentInfoWindowIndex.value = index
}
const getCenterOfPolygon = computed(() => (index) => {
  // let bounds = new google.maps.LatLngBounds()
  // console.log(polygon)
  // polygon.getPath().forEach((latLng) => bounds.extend(latLng))
  // map.value.fitBounds(bounds)

  // return bounds.getCenter()

  const polygon = this.$refs.itemRefs[index]
  const bounds = polygon.getBounds()
  const center = bounds.getCenter()
  const infoWindow = this.$refs.infoWindow
  infoWindow.setPosition(center)
})

function serializeOne(polygon) {
  const polygonCoordinates = []
  const vertices = polygon.getPath()
  vertices.forEach(function (vertex) {
    polygonCoordinates.push({
      lat: vertex.lat(),
      lng: vertex.lng(),
    })
  })
  return polygonCoordinates
}
function serialize() {
  const polygonCoordinates = []
  polygons.value.forEach(function (polygon) {
    polygonCoordinates.push(serializeOne(polygon))
  })
  return polygonCoordinates
}

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

function savePolygons() {
  const savedPolygons = []
  if (!polygons.value) {
    return
  }

  state.value.polygons = serialize()
}

const asd = ref([])
const infoWindowsOpened = ref([])

const polygonLabels = ref([])

const updateLabel = ({ polygonName, polygonIndex }) => {
  polygonLabels.value[polygonIndex].setLabel(polygonName)
  currentInfoWindowIndex.value = null
}

const state = useStorage('app-store', { polygons: [], polygonNames: [], markers: [] })
state.value.polygonNames = state.value.polygonNames || []
state.value.polygons = state.value.polygons || []

// state.value.markers = state.value.markers || [
//   { lat: -4.27079, lng: -41.78667, alert: false },
//   { lat: -4.26778, lng: -41.78648, alert: false },
//   { lat: -4.281896, lng: -41.772761, alert: false },
//   { lat: -4.278861, lng: -41.794099, alert: true },
//   { lat: -4.277929, lng: -41.776558, alert: true },
//   { lat: -4.25565, lng: -41.805445, alert: true },
//   { lat: -4.279603, lng: -41.775932, alert: true },
//   { lat: -4.279603, lng: -41.775932, alert: true },
//   { lat: -4.285898, lng: -41.800961, alert: true },
//   { lat: -4.282285, lng: -41.772658, alert: true },
//   { lat: -4.26606, lng: -41.806942, alert: true },
//   { lat: -4.289922, lng: -41.807408, alert: true },
//   { lat: -4.281836, lng: -41.779707, alert: true },
//   { lat: -4.282848, lng: -41.774176, alert: true },
//   { lat: -4.273743, lng: -41.78129, alert: true },
//   { lat: -4.263637, lng: -41.797071, alert: true },
//   { lat: -4.276892, lng: -41.779148, alert: true },
//   { lat: -4.256098, lng: -41.773501, alert: true },
//   { lat: -4.25533, lng: -41.779087, alert: true },
//   { lat: -4.263637, lng: -41.795704, alert: true },
// ]

// Third pattern: watch for "ready" then do something with the API or map instance
watch(
  () => mapRef.value?.ready,
  (ready) => {
    if (!ready) return
    map.value = mapRef.value.map
    geoCoder.value = new mapRef.value.api.Geocoder()

    // do something with the api using `mapRef.value.api`
    // or with the map instance using `mapRef.value.map`

    drawingManager.value = new google.maps.drawing.DrawingManager({
      drawingMode: null,
      drawingControl: true,
      drawingControlOptions: {
        position: google.maps.ControlPosition.TOP_CENTER,
        drawingModes: ['polygon'],
      },
      polygonOptions: {
        paths: [],
        fillColor: '#009334',
        strokeColor: '#009334',
        strokeOpacity: 0.8,
        strokeWeight: 3,
        fillOpacity: 0.35,
        editable: true,
      },
    })

    // Set the drawing manager to draw on the map instance
    drawingManager.value.setMap(mapRef.value.map)

    // Add an event listener for when the user finishes drawing a polygon
    google.maps.event.addListener(drawingManager.value, 'overlaycomplete', (event) => {
      if (event.type === google.maps.drawing.OverlayType.POLYGON) {
        const polygon = event.overlay
        //console.log(state.value.polygons)
        polygons.value.push(polygon)
        savePolygons()
        showInfoWindow(polygons.value.length - 1)
      }
    })

    google.maps.event.addListener(map.value, 'click', (event) => {
      // Verifica se o clique ocorreu dentro de algum polígono
      polygons.value.forEach((polygon, polygonIndex) => {
        if (google.maps.geometry.poly.containsLocation(event.latLng, polygon)) {
          showInfoWindow(polygonIndex)
        }
      })
    })

    // Carrega polígonos salvos do localStorage ao inicializar o mapa
    // loadPolygons()
    state.value.polygons.forEach(function (polygonCoordinates, index) {
      const polygon = new google.maps.Polygon({
        paths: polygonCoordinates,
        fillColor: '#FFA901',
        strokeColor: '#4FA9DD',
        fillOpacity: 0.5,
        strokeWeight: 1,
        clickable: false,
        editable: true,
        zIndex: 1,
      })

      polygon.getPath().forEach(function (latLng, index) {
        const polygonIndex = polygons.value.length
        const vertices = polygon.getPath()
        google.maps.event.addListener(vertices, 'set_at', function (event) {
          // console.log('A vértice ' + index + ' do polígono foi movida pa
          const polygonCoordinates = []
          vertices.forEach(function (vertex) {
            polygonCoordinates.push({
              lat: vertex.lat(),
              lng: vertex.lng(),
            })
          })
          // state.value.polygons[polygonIndex] = polygonCoordinates
          polygonCoordinates.forEach(function (p, k) {
            state.value.polygons[polygonIndex][k] = { ...p, ...state.value.polygons[polygonIndex][k].alert }
          })
        })
      })

      polygons.value.push(polygon)

      let bounds = new google.maps.LatLngBounds()
      polygon.getPath().forEach((latLng) => bounds.extend(latLng))
      map.value.fitBounds(bounds)

      let center = bounds.getCenter()
      // polygon name text label
      polygonLabels.value.push(
        new google.maps.Marker({
          position: center,
          label: {
            text: `${state.value.polygonNames[index]}`,
            color: 'black',
            fontWeight: 'bold',
          },
          icon: {
            path: google.maps.SymbolPath.CIRCLE,
            fillColor: 'transparent',
            fillOpacity: 0,
            strokeColor: 'transparent',
            strokeWeight: 0,
            scale: 0,
          },
          map: map.value,
        })
      )
    })
  }
)

const geocodeAddress = (geoCoder, resultsMap) => {
  geoCoder.geocode({ address: geoCoderQuery.value }, function (results, status) {
    if (status === 'OK') {
      resultsMap.setCenter(results[0].geometry.location)
      showEmptyResult.value = false
      console.log(showEmptyResult.value)
      //const marker = new google.maps.Marker({
      //  map: resultsMap,
      //  position: results[0].geometry.location
      //})
    } else {
      showEmptyResult.value = true
      console.log(showEmptyResult.value)
    }
  })
}

const patientMarkers = ref([])

onMounted(async () => {
  await patientsStore.fetchPatients()
  document.addEventListener('click', handleClickOutside)

  //   state.value.markers = [
  //    { lat: -4.27079, lng: -41.78667, alert: false },
  //    { lat: -4.26778, lng: -41.78648, alert: false },
  //    { lat: -4.281896, lng: -41.772761, alert: false },
  //    { lat: -4.278861, lng: -41.794099, alert: true },
  //    { lat: -4.277929, lng: -41.776558, alert: true },
  //    { lat: -4.25565, lng: -41.805445, alert: true },
  //    { lat: -4.279603, lng: -41.775932, alert: true },
  //    { lat: -4.279603, lng: -41.775932, alert: true },
  //    { lat: -4.285898, lng: -41.800961, alert: true },
  //    { lat: -4.282285, lng: -41.772658, alert: true },
  //    { lat: -4.26606, lng: -41.806942, alert: true },
  //    { lat: -4.289922, lng: -41.807408, alert: true },
  //    { lat: -4.281836, lng: -41.779707, alert: true },
  //    { lat: -4.282848, lng: -41.774176, alert: true },
  //    { lat: -4.273743, lng: -41.78129, alert: true },
  //    { lat: -4.263637, lng: -41.797071, alert: true },
  //    { lat: -4.276892, lng: -41.779148, alert: true },
  //    { lat: -4.256098, lng: -41.773501, alert: true },
  //    { lat: -4.25533, lng: -41.779087, alert: true },
  //    { lat: -4.263637, lng: -41.795704, alert: true },
  //  ]
})

const markers = ref([])
onBeforeUpdate(() => {
  markers.value = []
})

const isDraggable = computed(() => (index) => index == movingIndex.value)
const patients = computed(() => {
  if (onlyAlerts.value) {
    return props.patients.filter((p) => p.alert.length > 0)
  }
  return props.patients
})

function moveMarker(event, index) {
  movingIndex.value = index
}

async function handleMarkerDrag(event, index) {
  // console.log('dragend', event.latLng.lat(), event.latLng.lng())

  // const coords = {
  //   lat: event.latLng.lat(),
  //   lng: event.latLng.lng(),
  //   alert: state.value.markers[index].alert || false,
  // }

  // polygonCoordinates.forEach(function (p, k) {
  //   state.value.polygons[polygonIndex][k] = p
  // })
  // state.value.polygons[polygonIndex].forEach(function (p, k) {
  //   polygonCoordinates[k] = p
  // })
  // console.log(markers.value[index])
  // console.log(coords)
  if (index !== -1) {
    // Atualiza o item se encontrado
    patientsStore.items.splice(index, 1, {
      ...patientsStore.items[index],
      address: {
        latitude: event.latLng.lat(),
        longitude: event.latLng.lng(),
      },
    })
  }
  movingIndex.value = null
  const response = await patientsStore.movePatient(props.patients[index].id, {
    address: [
      {
        id: 1,
        latitude: event.latLng.lat(),
        longitude: event.latLng.lng(),
      },
    ],
  })

  // LocalStorage Method #1
  // markers.value[index] = coords
  // state.value.markers[index] = coords
}

const emit = defineEmits(['update:markers-in-view'])

const patientsInView = ref([])
const getMarkersInView = () => {
  const mapBounds = mapRef.value.map.getBounds()
  patientsInView.value = props.patients.filter((marker) => mapBounds.contains(patientLocation.value(marker)))
  emit('update:markers-in-view', patientsInView.value)
}

function deletePolygon(polygonIndex) {
  const confirmed = confirm('Tem certeza que deseja excluir este polígono?')
  if (confirmed) {
    polygons.value.splice(polygonIndex, 1)
    currentInfoWindowIndex.value = null
    savePolygons()
    polygonLabels.value[polygonIndex].setLabel('')
    polygonLabels.value.splice(polygonIndex, 1)
  }
}

const { coords } = useGeolocation()
const userLocation = computed(() => ({
  lat: coords.value.latitude,
  lng: coords.value.longitude,
}))
const patientLocation = computed(() => (patientMarker) => {
  // return patientMarker.address
  return { lat: patientMarker.address.latitude, lng: patientMarker.address.longitude, alert: true }
})
const dddd = computed(() => (polygonIndex) => {
  console.log('asd dddd')
})
const ddd = () => {
  console.log('asd ddd')
}

defineExpose({ patientsInView })
</script>

<style type="text/css">
.container {
  padding: 5px;
}

.list {
  background-color: white;
  border-radius: 5px;
  padding: 5px;
}

.list-item {
  cursor: pointer;
}

.edit-panel {
  position: fixed;
  left: 50%;
  top: 0;
  width: 380px;
  margin: 150px 0 0 -190px;
  /* Apply negative top and left margins to center the element */
}

.slide-in-enter-active,
.slide-in-leave-active {
  transition: all 0.3s ease;
}

.slide-in-enter,
.slide-in-leave-to {
  transform: translateX(100%);
}

div:first-of-type > div.gmnoprint[role='menubar'] {
  scale: 200%;
}
</style>
