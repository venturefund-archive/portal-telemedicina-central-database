<template>
  <div>
    <p class="text-lg mb-4 font-semibold text-gray-700">Mapa vacinal</p>
  <div>
     <!-- People with vaccines delayed -->
    <div class="bg-gray-50 rounded shadow-xl grid grid-cols-1 md:grid-cols-5 gap-2 items-center w-full  p-2">
  <div class="col-span-3 px-3">
    <form @submit.prevent="searchAddress" class="flex items-center w-full">
      <label for="default-search" class="sr-only text-sm font-medium text-gray-900">Procurar</label>
      <div class="relative flex items-center w-full">
        <svg class="h-5 w-5 text-gray-500 absolute left-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
        <input :placeholder="$t('manager.search-map')" v-model="geocoderQuery" class="bg-white py-3 px-10 mr-1 w-full rounded-md border border-2 shadow-sm" />      </div>
    </form>
  </div>

  <div class="mt-4 md:mt-0">
    <button @click="showList = !showList" class="relative z-10 flex flex-col items-center py-2 text-gray-500 rounded-md">
      <UsersIcon title="População" class="h-6 w-6 text-green-500"/>
      <span class="py-1 text-sm">{{ $t('manager.population') }}</span>
    </button>
    <ul v-if="showList" class="absolute z-20 rounded-md shadow-md bg-white" style="margin-top: -0.5rem;">
      <li v-for="item in items" :class="{ 'font-bold': item === selectedItem }" class="px-4 py-2 font-normal cursor-pointer hover:bg-gray-100" :key="item" @click="onItemClick(item)">
        {{ item }}
      </li>
    </ul>
  </div>

  <div class="mt-4 md:mt-0">
    <div class="inline-block align-middle mr-2 select-none transition duration-200 ease-in relative w-10">
      <input type="checkbox" name="toggle" id="toggle" class="absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer toggle-checkbox" v-model="onlyAlerts" />
      <label for="toggle" class="block h-6 rounded-full bg-gray-300 cursor-pointer toggle-label"></label>
    </div>
    <label for="toggle" class="text-gray-500 text-sm">{{ $t('manager.alerts') }}</label>
  </div>
</div>
 <!-- Map content -->
  <div class="flex justify-start shadow">
    <GoogleMap :api-key="GOOGLE_MAP_API_KEY" style="width: 100%; height: 780px" id="map" :center="center" :zoom="14" :libraries="['drawing']"
      ref="mapRef">
      <template #default="{ ready, api, map, mapTilesLoaded }">
        <!-- First pattern: Here you have access to the API and map instance.
          "ready" is a boolean that indicates when the Google Maps script
          has been loaded and the api and map instance are ready to be used -->
        <MarkerCluster>
          <div
            v-for="(location, i) in locations"

            :key="i">
            <Marker v-if="onlyAlerts && location.alert == false || !onlyAlerts"
                    :ref="el => { markers[i] = el }"
                    :options="{ position: location, draggable: isDraggable(i), icon: ( location.alert ) ? customMarkerIcon : customMarkerIcon2 }"
                    @dragend="handleMarkerDrag($event, i)">


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
                        <div class="flex flex-col justify-between p-5 bg-white rounded-2xl">
                          <p class="font-semibold text-xl tracking-wider py-3">qwe</p>
                          <hr class="border border-1 border-dashed border-gray-300"/>
                          <!-- <ProfileCard v-if="patientsStore.item" :id="patientsStore.item.id" class="my-3" /> -->
                          <div class="flex justify-between py-5">
                            <p class=" text-sm font-normal text-black rounded-full bg-gray-100 px-3 py-1 justify-center">
                               3 months
                              </p>
                            <p class="text-sm bg-red-100 font-normal rounded-full text-red-900 px-3 py-1">
                              vaccine with delay: BCG
                            </p>
                          </div>
                          <div class="font-normal">
                            <p>
                               Document: xxxx
                              </p>
                              <p>
                                 Birthdate: xx/xx/xx
                              </p>
                            <p>
                              Address: xxxxx
                            </p>
                          </div>
                          <span class="text-sm text-gray-400 mt-5 flex justify-end">Última alteração: 08/02/2023</span>
                        </div>

                        <div class="flex justify-evenly py-3">
                          <Button type="submit" variant="success-outline"
                                  @click="moveMarker($event, i)"
                                  class="mx-2 gap-2 focus:outline-none"
                                  :disabled="editForm.processing"
                                  v-slot="{ iconSizeClasses }">
                            <HandIcon aria-hidden="true" :class="iconSizeClasses" />
                            <span>Mover</span>
                          </Button>
                          <PopoverButton :focus="false" :class="{ 'relative z-30': open }">
                            <Button type="submit" variant="success"
                                    class="mx-2 gap-2 focus:outline-none bg-white"
                                    :disabled="editForm.processing"
                                    v-slot="{ iconSizeClasses }">
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
  <div class="py-10">
  <Button type="submit" variant="success-outline"
                                  @click="savePolygons"
                                  class="focus:outline-none">
                            <SaveIcon class="w-5 h-5" />
                            <span>{{ $t('manager.save') }}</span>
                          </Button>
                        </div>
</div>
</div>
</template>

<script setup>
import { defineComponent, reactive, computed, onBeforeUpdate, onMounted, watch, ref, onUnmounted } from 'vue'
import { GoogleMap, Marker, CustomMarker, MarkerCluster, InfoWindow, Polygon } from 'vue3-google-map'
import { useGeolocation } from '@/composables/useGeolocation'
import { Popover, PopoverButton, PopoverPanel, PopoverOverlay } from '@headlessui/vue'
import { HandIcon, PencilIcon, UsersIcon, SaveIcon, XIcon } from '@heroicons/vue/solid'
import { useRouter } from 'vue-router'
import { usePatientsStore } from '@/stores/patients'
import { useStorage } from '@vueuse/core'
const patientsStore = usePatientsStore()
const router = useRouter()
const mapRef = ref(null)
const geocoder = ref(null)
const map = ref(null)
const onlyAlerts = ref(false)
const polygonTemp = ref(null)
const selectedItem = ref(null)
const drawingManager = ref(null)
const movingIndex = ref(null)
const center = ref({ lat: -22.748950, lng: -50.572530 })
const isModalOpen = ref(false)
const searchQuery = ref('')
const GOOGLE_MAP_API_KEY = ref(import.meta.env.VITE_GOOGLE_MAP_API_KEY)
const customMarkerIcon = ref({
  url: 'public/marker1.png',
  scaledSize: {
    width: 40,
    height:50
  },
})
const customMarkerIcon2 = ref({
  url: 'public/marker2.png',
  scaledSize: {
    width: 40,
    height: 50
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

const showList = ref(false);
const items = ['Todos', 'Gestantes','Puérperas', 'Recém-nascidos', 'Primeira infância', 'Segunda infância', 'Terceira Infância','Adolescência'];

const handleClickOutside = (event) => {
  if (!event.target.closest('.mt-4')) {
    showList.value = false;
  }
};

onMounted(async () => {
  await patientsStore.fetchPatients()
  document.addEventListener('click', handleClickOutside);
})



onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
})


function onItemClick(item) {
  selectedItem.value = item;
  console.log(`Item clicado: ${item}`)
}

const customClusterIcon = ref({
  url: 'https://i.ibb.co/sQWvRnX/ssss.png',
  scaledSize: {
    width: 50,
    height: 50
  }
})

const rectangle = ref({
  paths: [],
  strokeColor: '#FF0000',
  strokeOpacity: 0.8,
  strokeWeight: 2,
  fillColor: '#FF0000',
  fillOpacity: 0.35,
  editable: true
})
const polygons = ref([])
const customPolygons = (key) => {
  return {
    paths: polygons.value[key].polygon || [],
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: '#FF0000',
    fillOpacity: 0.35,
    editable: true
  }
}

const geocoderQuery = ref('')
const searchAddress = () => {
  //center.value = { lat: -22.749940, lng: -50.576540 }

  geocodeAddress(geocoder.value, map.value)
}

const query = ref('')
center.value = { lat: -22.749940, lng: -50.576540 }

const locations = reactive([
  { lat: -22.748950, lng: -50.572530, alert: false },
  { lat: -22.745940, lng: -50.572340, alert: true },
  { lat: -22.760056, lng: -50.558621, alert: true },
  { lat: -22.757021, lng: -50.579959, alert: true },
  { lat: -22.756089, lng: -50.562418, alert: true },
  { lat: -22.73381, lng: -50.591306, alert: true },
  { lat: -22.757763, lng: -50.560793, alert: true },
  { lat: -22.757763, lng: -50.560793, alert: true },
  { lat: -22.764058, lng: -50.585821, alert: false },
  { lat: -22.760445, lng: -50.557518, alert: true },
  { lat: -22.74422, lng: -50.590802, alert: true },
  { lat: -22.768082, lng: -50.591269, alert: true },
  { lat: -22.759996, lng: -50.563568, alert: true },
  { lat: -22.761008, lng: -50.558037, alert: true },
  { lat: -22.751903, lng: -50.565151, alert: true },
  { lat: -22.741797, lng: -50.580932, alert: true },
  { lat: -22.755052, lng: -50.563009, alert: false },
  { lat: -22.734258, lng: -50.557362, alert: true },
  { lat: -22.73349, lng: -50.562948, alert: true },
  { lat: -22.741799, lng: -50.579565, alert: true },
])
const markers = ref([])
onBeforeUpdate(() => {
  markers.value = []
})
function savePolygons() {
  const savedPolygons = []
  polygons.value.forEach(function(polygon) {
    const vertices = polygon.getPath()
    const polygonCoordinates = []
    vertices.forEach(function(vertex) {
      polygonCoordinates.push({
        lat: vertex.lat(),
        lng: vertex.lng()
      })
    })
    savedPolygons.push(polygonCoordinates)
  })
  const state = useStorage('app-store', { polygons: [] })
  if (undefined == state.value.polygons) {
    state.value.polygons = []
  }
  state.value.polygons = savedPolygons
}
function loadPolygons() {
  const state = useStorage('app-store', { polygons: [] })
  if(undefined == state.value.polygons) {
    state.value.polygons = []
  }
  if (state.value.polygons) {
    state.value.polygons.forEach(function(polygonCoordinates) {
      const polygon = new google.maps.Polygon({
        paths: polygonCoordinates,
        fillColor: '#ffff00',
        fillOpacity: 0.5,
        strokeWeight: 2,
        clickable: false,
        editable: true,
        zIndex: 1
      })
      polygon.setMap(mapRef.value.map)
      polygons.value.push(polygon)
    })
  }
}

// Third pattern: watc'h for "ready" then do something with the API or map instance
watch(() => mapRef.value?.ready, (ready) => {
  if (!ready) return
  map.value = mapRef.value.map
  geocoder.value = new mapRef.value.api.Geocoder()

  // do something with the api using `mapRef.value.api`
  // or with the map instance using `mapRef.value.map`
  // const mapp = new google.maps.Map(document.getElementById('map'))
  //console.log(mapRef.value.map)

  drawingManager.value = new google.maps.drawing.DrawingManager({
      drawingMode: google.maps.drawing.OverlayType.POLYGON,
      drawingControl: true,
      drawingControlOptions: {
        position: google.maps.ControlPosition.TOP_CENTER,
        drawingModes: ['polygon']
      },
      polygonOptions: rectangle.value
  })

  // Set the drawing manager to draw on the map instance
  drawingManager.value.setMap(mapRef.value.map)


  const state = useStorage('app-store', { polygons: [] })
  if(undefined == state.value.polygons) {
    state.value.polygons = []
  }
  let polygonData = state.value.polygons
console.log(polygonData.value)

  // Add an event listener for when the user finishes drawing a polygon
  google.maps.event.addListener(drawingManager.value, 'overlaycomplete', (event) => {
    if (event.type === google.maps.drawing.OverlayType.POLYGON) {
      const polygon = event.overlay
      polygons.value.push(polygon)

      google.maps.event.addListener(polygon, 'click', function(event) {
        // destaca o polígono
        polygon.setOptions({
          fillColor: '#FFFF00', // altera a cor do preenchimento para amarelo
          strokeColor: '#FF0000' // altera a cor da borda para vermelho
        });
        var paths = polygon.getPaths();
        var confirmed = confirm('Tem certeza que deseja excluir todos os pontos do polígono?');
        if (confirmed) {
          paths.forEach(function(path) {
            path.forEach(function(point) {
              var marker = point.marker;
              if (marker) {
                marker.setMap(null);
              }
            });
          });
          polygon.setPaths([]);
          savePolygons()
        } else {
          // o usuário cancelou a exclusão, restaure as cores do polígono
          polygon.setOptions({
            fillColor: '#0000FF', // altera a cor do preenchimento para azul
            strokeColor: '#FF0000' // altera a cor da borda para vermelho
          });
        }
      });

    }
  })

  // Carrega polígonos salvos do localStorage ao inicializar o mapa
  loadPolygons()
})

const geocodeAddress = (geocoder, resultsMap) => {
  geocoder.geocode({ 'address': geocoderQuery.value }, function (results, status) {
    if (status === 'OK') {
      resultsMap.setCenter(results[0].geometry.location)
      //const marker = new google.maps.Marker({
      //  map: resultsMap,
      //  position: results[0].geometry.location
      //})
    } else {
      alert('Geocode was not successful for the following reason: ' + status)
    }
  })
}
const isDraggable = computed(() => index => index == movingIndex.value)
const patients = computed(() => {
  if(onlyAlerts.value){
    return patientsStore.items.filter(p => (p.number_of_alerts_by_protocol > 0))
  }
  return patientsStore.items
})

function moveMarker(event, index) {
  movingIndex.value = index
}

function handleMarkerDrag(event, index) {
  console.log('dragend', event.latLng.lat(), event.latLng.lng())
  console.log(markers.value[index])
  markers.value[index].setPosition({
    lat: event.latLng.lat(),
    lng: event.latLng.lng()
  })
}

const { coords } = useGeolocation()
const userLocation = computed(() => ({
  lat: coords.value.latitude,
  lng: coords.value.longitude
}))
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
  margin: 150px 0 0 -190px; /* Apply negative top and left margins to center the element */
}

.toggle-checkbox:checked {
  @apply: right-0 border-green-400;
  right: 0;
  border-color: green;
}
.toggle-checkbox:checked + .toggle-label {
  @apply: bg-green-400;
  background-color: green;
}

@media (min-width: 768px) {
  .w-1\\/2 {
    width: 50%;
  }
}

.slide-in-enter-active,
  .slide-in-leave-active {
    transition: all 0.3s ease;
  }

  .slide-in-enter,
  .slide-in-leave-to {
    transform: translateX(100%);
  }

div:first-of-type > div.gmnoprint[role=menubar] {
  scale: 200%;
}
</style>
