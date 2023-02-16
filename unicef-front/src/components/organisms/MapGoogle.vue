<template>
  <form @submit.prevent="searchAddress" class="w-full md:flex md:justify-center pb-5">
    <label for="default-search" class="sr-only mb-2 text-sm font-medium text-gray-900">Procurar</label>
    <div class="relative">
      <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
        <svg class="h-5 w-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
      </div>
      <div class="flex">
        <input placeholder="Pesquisar no mapa"
          class="block w-full px-5 rounded-lg border border-transparent focus:shadow-none bg-gray-50 py-4.5 pl-10 text-gray-900 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
          v-model="address" />
        <Button type="submit" class="mx-5 justify-center">Pesquisar</Button>
      </div>
    </div>
  </form>
  <div class="flex justify-center">
    <GoogleMap :api-key="GOOGLE_MAP_API_KEY" style="width: 100%; height: 700px" :center="center" :zoom="14"
      ref="mapRef">
      <template #default="{ ready, api, map, mapTilesLoaded }">
        <!-- First pattern: Here you have access to the API and map instance.
          "ready" is a boolean that indicates when the Google Maps script
          has been loaded and the api and map instance are ready to be used -->
        <CustomMarker v-if="userLocation" :options="{
                                  anchorPoint: 'LEFT_CENTER',
                                  position: userLocation,
                                }">👩 User Position</CustomMarker>
        <MarkerCluster>
          <Marker v-for="(location, i) in locations" :key="i" :ref="el => { markers[i] = el }" :options="{ position: location, draggable: isDraggable(i), icon: customMarkerIcon }" @dragend="handleMarkerDrag($event, i)">
            <span>{{ isDraggable(i) }}</span>
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
</template>

<script setup>
import { defineComponent, reactive, computed, onBeforeUpdate, onMounted, watch, ref } from 'vue'
import { GoogleMap, Marker, CustomMarker, MarkerCluster, InfoWindow } from 'vue3-google-map'
import { useGeolocation } from '@/composables/useGeolocation'
import { Popover, PopoverButton, PopoverPanel, PopoverOverlay } from '@headlessui/vue'

import { HandIcon, PencilIcon } from '@heroicons/vue/outline'
import { useRouter } from 'vue-router'
import { usePatientsStore } from '@/stores/patients'
const patientsStore = usePatientsStore()

const router = useRouter()

const editForm = reactive({
  username: '',
  email: '',
  password1: '',
  password2: '',
  terms: false,
  processing: false,
})

const mapRef = ref(null)
const center = ref(null)
const address = ref()
const geocoder = ref(null)
const map = ref(null)
const GOOGLE_MAP_API_KEY = ref(import.meta.env.VITE_GOOGLE_MAP_API_KEY)
const customMarkerIcon = ref({
  url: 'https://cdn4.iconfinder.com/data/icons/small-n-flat/24/user-alt-512.png',
  scaledSize: {
    width: 40,
    height: 40
  },
})
const customClusterIcon = ref({
  url: 'https://i.ibb.co/sQWvRnX/ssss.png',
  scaledSize: {
    width: 50,
    height: 50
  }
})
const movingIndex = ref(null)

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

// Third pattern: watch for "ready" then do something with the API or map instance
watch(() => mapRef.value?.ready, (ready) => {
  if (!ready) return
  map.value = mapRef.value.map
  geocoder.value = new mapRef.value.api.Geocoder()

  // do something with the api using `mapRef.value.api`
  // or with the map instance using `mapRef.value.map`
})

const geocodeAddress = (geocoder, resultsMap) => {
  geocoder.geocode({ 'address': address.value }, function (results, status) {
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
.edit-panel {
  position: fixed;
  left: 50%;
  top: 0;
  width: 380px;
  margin: 150px 0 0 -190px; /* Apply negative top and left margins to center the element */
}
</style>
