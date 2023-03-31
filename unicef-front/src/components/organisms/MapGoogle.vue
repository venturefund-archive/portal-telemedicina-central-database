<template>
  <div>
     <!-- People with vaccines delayed -->
    <div class="bg-white rounded shadow-md grid grid-cols-1 md:grid-cols-5 gap-5 items-center w-full md:w-1/2 p-1">
  <div class="col-span-3">
    <form @submit.prevent="searchAddress" class="flex items-center w-full">
      <label for="default-search" class="sr-only text-sm font-medium text-gray-900">Procurar</label>
      <div class="relative flex items-center w-full p-2">
        <svg class="h-5 w-5 text-gray-500 dark:text-gray-400 absolute left-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
        <input placeholder="Pesquisar no mapa" v-model="geocoderQuery" class="bg-neutral-100 py-3 px-7 mr-1 w-full rounded-md focus:ring-blue-500 focus:border-blue-500" />      </div>
    </form>
  </div>

  <div class="mt-4 md:mt-0">
    <button @click="showList = !showList" class="relative z-10 flex flex-col items-center px-4 py-2 text-gray-500 bg-primary rounded-md">
      <UsersIcon title="População" class="h-8 w-8 text-blue-500"/>
      <span class="mt-1">População</span>
    </button>
    <ul v-if="showList" class="absolute z-20 rounded-md shadow-md bg-white" style="margin-top: -0.5rem;">
      <li v-for="item in items" :class="{ 'font-bold': item === selectedItem }" class="px-4 py-2 font-normal cursor-pointer hover:bg-gray-100" :key="item" @click="onItemClick(item)">
        {{ item }}
      </li>
    </ul>
  </div>

  <div class="mt-4 md:mt-0">
    <div class="inline-block align-middle mr-2 select-none transition duration-200 ease-in relative w-10">
      <input type="checkbox" name="toggle" id="toggle" class="absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer toggle-checkbox" v-model="isActive" />
      <label for="toggle" class="block h-6 rounded-full bg-gray-300 cursor-pointer toggle-label" :class="{'bg-red-500': isActive, 'border-red-500': isActive}"></label>
    </div>
    <label for="toggle" class="text-gray-500">Alertas</label>
  </div>
</div>
  <div class="flex justify-start shadow md:w-1/2">
    <GoogleMap :api-key="GOOGLE_MAP_API_KEY" style="width: 100%; height: 700px" id="map" :center="center" :zoom="14" :libraries="['drawing']"
      ref="mapRef">
      <template #default="{ ready, api, map, mapTilesLoaded }">
        <!-- First pattern: Here you have access to the API and map instance.
          "ready" is a boolean that indicates when the Google Maps script
          has been loaded and the api and map instance are ready to be used -->

          <Polygon :options="rectangle"/>

        <CustomMarker v-if="userLocation" :options="{
                                  anchorPoint: 'LEFT_CENTER',
                                  position: userLocation,
                                }">👩 User Position</CustomMarker>
        <MarkerCluster>
          <Marker v-for="(location, i) in locations" :key="i" :ref="el => { markers[i] = el }" :options="{ position: location, draggable: isDraggable(i), icon: customMarkerIcon }" @dragend="handleMarkerDrag($event, i)">
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

                              <h3 class="pb-3">Editando Paciênte #42</h3>
                              <form @submit.prevent="">
                                <div class="grid gap-6">

                                  <div class="space-y-1">
                                    <Label for="name" value="Paciênte" />

                                      <Input
                                        id="name"
                                        type="text"
                                        placeholder="Paciênte"
                                        class="block w-full"
                                        v-model="editForm.name"
                                        required
                                        autofocus
                                        autocapitalize="on"
                                        autocorrect="off"
                                      />
                                  </div>

                                  <div class="space-y-1">
                                    <Label for="profissional" value="Profissional" />

                                      <Input
                                        id="profissional"
                                        type="text"
                                        placeholder="Profissional"
                                        class="block w-full"
                                        v-model="editForm.profissional"
                                        required
                                        autofocus
                                        autocapitalize="on"
                                        autocorrect="off"
                                      />
                                  </div>

                                  <div class="space-y-1">
                                    <Label for="city" value="Cidade" />

                                      <Input
                                        id="city"
                                        type="text"
                                        placeholder="Cidade"
                                        class="block w-full"
                                        v-model="editForm.city"
                                        required
                                        autofocus
                                        autocapitalize="on"
                                        autocorrect="off"
                                      />
                                  </div>

                                  <div class="space-y-1">
                                    <Label for="state" value="Bairro" />

                                      <Input
                                        id="state"
                                        type="text"
                                        placeholder="Bairro"
                                        class="block w-full"
                                        v-model="editForm.cidade"
                                        required
                                        autofocus
                                        autocapitalize="on"
                                        autocorrect="off"
                                      />
                                  </div>

                                  <div class="space-y-1">
                                    <Label for="number" value="Número" />

                                      <Input
                                        id="number"
                                        type="text"
                                        placeholder="Número"
                                        class="block w-full"
                                        v-model="editForm.cidade"
                                        required
                                        autofocus
                                        autocapitalize="on"
                                        autocorrect="off"
                                      />
                                  </div>

                                  <div class="space-y-1">
                                    <Label for="dose" value="Dose" />

                                      <Input
                                        id="dose"
                                        type="text"
                                        placeholder="Dose"
                                        class="block w-full"
                                        v-model="editForm.cidade"
                                        required
                                        autofocus
                                        autocapitalize="on"
                                        autocorrect="off"
                                      />
                                  </div>

                                  <div class="space-y-1">
                                    <Label for="vaccine" value="Vacina" />

                                      <Input
                                        id="vaccine"
                                        type="text"
                                        placeholder="Vacina"
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
                    <div id="siteNotice"></div>
                    <h1 id="firstHeading" class="firstHeading"></h1>
                    <div id="bodyContent" class="p-1">
                      <div class="flex flex-col justify-between p-5 bg-gray-200 rounded-2xl">
                        <h1 class="font-bold text-lg tracking-wider">Fulano Exemplo</h1>
                        <ProfileCard v-if="patientsStore.item" :id="patientsStore.item.id" class="my-3" />
                        <div>
                          <p class="text-sm text-gray-400">
                            Paciênte
                            Profissional
                            Dose
                            Vacina
                            Cidade
                            Bairro
                            Número
                          </p>
                        </div>
                        <span class="text-sm text-gray-400 italic mt-5 flex justify-end">Publicado 08/10/2022</span>
                      </div>

                      <div class="flex justify-evenly py-3">
                        <Button type="submit" variant="info"
                                @click="moveMarker($event, i)"
                                class="mx-2 gap-2 focus:outline-none"
                                :disabled="editForm.processing"
                                v-slot="{ iconSizeClasses }">
                          <HandIcon aria-hidden="true" :class="iconSizeClasses" />
                          <span>Mover</span>
                        </Button>
                        <PopoverButton :focus="false" :class="{ 'relative z-30': open }">
                          <Button type="submit" variant="warning"
                                  class="mx-2 gap-2 focus:outline-none"
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
        </MarkerCluster>
      </template>
    </GoogleMap>
  </div>

</div>
</template>

<script setup>
import { defineComponent, reactive, computed, onBeforeUpdate, onMounted, watch, ref, onUnmounted } from 'vue'
import { GoogleMap, Marker, CustomMarker, MarkerCluster, InfoWindow, Polygon } from 'vue3-google-map'
import { useGeolocation } from '@/composables/useGeolocation'
import { Popover, PopoverButton, PopoverPanel, PopoverOverlay } from '@headlessui/vue'
import { HandIcon, PencilIcon, UsersIcon, BellIcon, XIcon } from '@heroicons/vue/solid'
import { useRouter } from 'vue-router'
import { usePatientsStore } from '@/stores/patients'
import { useStorage } from '@vueuse/core'
const patientsStore = usePatientsStore()
const router = useRouter()
const mapRef = ref(null)
const geocoder = ref(null)
const map = ref(null)
const isActive = ref(false)
const polygon1 = ref(null)
const selectedItem = ref(null)
const drawingManager = ref(null)
const movingIndex = ref(null)
const center = ref({ lat: -22.748950, lng: -50.572530 })
const isModalOpen = ref(false)
const searchQuery = ref('')
const GOOGLE_MAP_API_KEY = ref(import.meta.env.VITE_GOOGLE_MAP_API_KEY)
const customMarkerIcon = ref({
  url: 'https://cdn4.iconfinder.com/data/icons/small-n-flat/24/user-alt-512.png',
  scaledSize: {
    width: 40,
    height: 40
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

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

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

const geocoderQuery = ref('')
const searchAddress = () => {
  //center.value = { lat: -22.749940, lng: -50.576540 }

  geocodeAddress(geocoder.value, map.value)
}

const query = ref('')
center.value = { lat: -22.749940, lng: -50.576540 }

const locations = reactive([
  { lat: -22.748950, lng: -50.572530 },
  { lat: -22.745940, lng: -50.572340 },
  { lat: -22.760056, lng: -50.558621 },
  { lat: -22.757021, lng: -50.579959 },
  { lat: -22.756089, lng: -50.562418 },
  { lat: -22.73381, lng: -50.591306 },
  { lat: -22.757763, lng: -50.560793 },
  { lat: -22.757763, lng: -50.560793 },
  { lat: -22.764058, lng: -50.585821 },
  { lat: -22.760445, lng: -50.557518 },
  { lat: -22.74422, lng: -50.590802 },
  { lat: -22.768082, lng: -50.591269 },
  { lat: -22.759996, lng: -50.563568 },
  { lat: -22.761008, lng: -50.558037 },
  { lat: -22.751903, lng: -50.565151 },
  { lat: -22.741797, lng: -50.580932 },
  { lat: -22.755052, lng: -50.563009 },
  { lat: -22.734258, lng: -50.557362 },
  { lat: -22.73349, lng: -50.562948 },
  { lat: -22.741799, lng: -50.579565 },
])
const markers = ref([])
onBeforeUpdate(() => {
  markers.value = []
})

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

  // // Set the drawing manager to draw on the map instance
  drawingManager.value.setMap(mapRef.value.map)

  // // Add an event listener for when the user finishes drawing a polygon
  google.maps.event.addListener(drawingManager.value, 'overlaycomplete', (event) => {
    if (event.type === google.maps.drawing.OverlayType.POLYGON) {
      // Set the polygon1 ref to the newly-drawn polygon
      polygon1.value = event.overlay

      // Get the coordinates of the polygon vertices
      const polygonCoords = []
      const path = event.overlay.getPath()
      for (let i = 0; i < path.getLength(); i++) {
        const latLng = path.getAt(i)
        polygonCoords.push({ lat: latLng.lat(), lng: latLng.lng() })
      }

      // Save the polygon coordinates in JSON format
      const polygonData = { polygon: polygonCoords }

      // we can use ajax or fetch here to save the polygon data on server
      // for now using localstore
      const state = useStorage('app-store', { polygons: [] })
      if(undefined == state.value.polygons) {
        state.value.polygons = []
      }
      state.value.polygons.push(polygonData)
    }
  })

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
  @apply: right-0 border-blue-400;
  right: 0;
  border-color: blue;
}
.toggle-checkbox:checked + .toggle-label {
  @apply: bg-blue-400;
  background-color: blue;
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
