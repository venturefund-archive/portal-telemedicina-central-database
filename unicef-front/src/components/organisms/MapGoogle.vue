<template>
  <div>
    <p class="mb-4 text-xl font-semibold text-gray-700">
      {{ !isMapView ? $t('manager.table-view-text') : $t('manager.vaccination-map') }}
    </p>

    <div class="!z-50 h-[106px] w-full rounded-t-2xl border !bg-gray-50 drop-shadow-lg drop-shadow-lg">
      <div>
        <!-- People with vaccines delayed -->
        <div class="flex flex-col items-center justify-between space-y-5 p-5 md:flex-row md:space-y-0 md:space-x-5">
          <div class="flex items-center space-x-5">
            <div v-if="!isMapView">
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
                  <div v-if="!isMapView">
                    <Input
                      :placeholder="$t('manager.search')"
                      v-model="addressQuery"
                      class="w-full rounded-lg border py-2 pl-10 pr-3 focus:outline-none focus:ring focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-white"
                    />
                  </div>
                  <div v-if="isMapView">
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
              <div ref="dropdown" class="relative">
    <button
      @click="showList = !showList"
      class="relative flex flex-col items-center rounded-md py-2 px-4 text-gray-500"
    >
      <UsersIcon title="{{ $t('manager.population') }}" class="h-6 w-6 text-green-500" />
      <span class="text-sm">{{ $t('manager.population') }}</span>
    </button>
    <ul
      v-if="showList"
      class="absolute z-10 rounded-md bg-white shadow-md w-40"
    >
      <li
        v-for="item in items"
        :class="{ 'font-bold': item === selectedItem }"
        class="cursor-pointer py-2 px-4 font-normal hover:bg-gray-100 w-full"
        :key="item"
      >
        {{ item }}
      </li>
    </ul>
  </div>

              <div v-if="isMapView" class="flex flex-col items-center rounded-md py-2 px-4 text-gray-500">
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
                  <TableIcon v-if="isMapView" class="h-8 w-9 text-gray-500" />
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
            v-if="!isMapView"
            @click=""
            class="border-gray-400 bg-transparent hover:bg-green-500 p-2 text-gray-400 shadow-md hover:border-green-500 hover:text-white"
          >
            <SaveIcon class="h-5 w-5" />
            <span class="text-sm">{{ $t('manager.save') }}</span>
          </Button> -->

      <!-- Toggle View Button -->
      <TableList v-show="!isMapView" />
      <!-- Map content -->
      <div class="border-1 -z-10 flex justify-start border bg-white drop-shadow-lg" v-if="isMapView">
        <GoogleMap
          :api-key="GOOGLE_MAP_API_KEY"
          style="width: 100%; height: 790px"
          id="map"
          :center="currentCenter"
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
            <div v-for="(polygon, polygonIndex) in googlePolygons" :key="polygonIndex">
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
                <RegionForm
                  @delete="deletePolygon(polygonIndex)"
                  :polygon="polygons[polygonIndex]"
                  :googlePolygon="polygon"
                  :polygonIndex="polygonIndex"
                  @saved="updateLabel"
                />
              </InfoWindow>
            </div>
            <MarkerCluster>
              <div v-for="marker in patients" :key="marker.id">
                <Marker
                  v-if="(onlyAlerts && 0 != marker.alerts.length) || !onlyAlerts"
                  :ref="
                    (el) => {
                      markers[marker.id] = el
                    }
                  "
                  :options="{
                    position: patientLocation(marker),
                    draggable: isDraggable(marker.id),
                    icon: isDraggable(marker.id)
                      ? markerIconEditing
                      : 0 !== marker.alerts.length
                      ? markerIconAlert
                      : markerIconNormal,
                    // opacity: isDraggable(i) ? 1 : 0.5
                  }"
                  @dragend="handleMarkerDrag($event, marker.id)"
                  @click="patientCursorLocal = marker.id"
                />

                <Teleport to=".notification-space">
                  <Popover v-slot="{ open }" class="">
                    <TransitionRoot as="template" :show="open">
                      <Dialog as="div" static class="fixed inset-0 z-10 overflow-y-auto" :show="open">
                        <div
                          class="flex min-h-screen items-end justify-center px-4 pt-4 pb-20 text-center sm:block sm:p-0"
                        >
                          <TransitionChild as="template" enter="ease-out duration-300" leave="ease-in duration-200">
                            <DialogOverlay class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
                          </TransitionChild>

                          <TransitionChild as="template" enter="ease-out duration-300" leave="ease-in duration-200">
                            <DialogPanel class="edit-panel z-20 mt-3 transform-gpu">
                              <div class="relative space-y-4 overflow-hidden rounded-lg bg-neutral-50 p-4 shadow-lg">
                                <div class="flex justify-between border-b border-dotted border-gray-400 pb-3">
                                  <DialogTitle as="h3" class="mx-auto text-center font-bold text-gray-800">
                                    Editar informação do paciente
                                  </DialogTitle>
                                  <XIcon class="h-6 w-6 cursor-pointer hover:text-green-500" />
                                </div>
                                <form
                                  @submit.prevent="submitForm"
                                  class="space-y-6"
                                  aria-label="Formulário de Registro"
                                >
                                  <div class="flex">
                                    <legend class="sr-only">Dados pessoais e clínicos</legend>

                                    <!-- Dados Pessoais -->
                                    <div class="w-[312px] space-y-3 px-2">
                                      <h4 class="text-sm font-semibold text-gray-600">Dados pessoais</h4>

                                      <div class="space-y-1">
                                        <label for="name" class="sr-only">Nome</label>
                                        <Input
                                          id="name"
                                          type="text"
                                          placeholder="Nome"
                                          class="block w-full border-gray-300 border-gray-300"
                                          v-model="editForm.name"
                                          required
                                          autofocus
                                          autocapitalize="on"
                                          autocorrect="off"
                                          aria-label="Nome"
                                        />
                                      </div>

                                      <div class="space-y-1">
                                        <label for="birthDate" class="sr-only">Data de Nascimento</label>
                                        <Input
                                          id="birthDate"
                                          type="date"
                                          placeholder="Data de Nascimento"
                                          class="block w-full border-gray-300"
                                          v-model="editForm.birthDate"
                                          required
                                          aria-label="Data de Nascimento"
                                        />
                                      </div>

                                      <div class="space-y-1">
                                        <label for="age" class="sr-only">Idade</label>
                                        <Input
                                          id="age"
                                          type="number"
                                          placeholder="Idade"
                                          class="block w-full border-gray-300"
                                          v-model="editForm.age"
                                          required
                                          aria-label="Idade"
                                        />
                                      </div>

                                      <div class="space-y-1">
                                        <label for="address" class="sr-only">Endereço</label>
                                        <Input
                                          id="address"
                                          type="text"
                                          placeholder="Endereço"
                                          class="block w-full border-gray-300"
                                          v-model="editForm.address"
                                          required
                                          aria-label="Endereço"
                                        />
                                      </div>

                                      <div class="space-y-1">
                                        <label for="cpf" class="sr-only">CPF</label>
                                        <Input
                                          id="cpf"
                                          type="text"
                                          placeholder="CPF"
                                          class="block w-full border-gray-300"
                                          v-model="editForm.cpf"
                                          required
                                          maxlength="11"
                                          aria-label="CPF"
                                        />
                                      </div>
                                    </div>

                                    <!-- Dados Clínicos -->
                                    <div class="w-[312px] space-y-3 px-2">
                                      <h4 class="text-sm font-semibold text-gray-600">Dados clínicos</h4>

                                      <div class="space-y-1">
                                        <label for="healthUnit" class="sr-only">Unidade de saúde</label>
                                        <Input
                                          id="healthUnit"
                                          type="text"
                                          placeholder="Unidade de saúde"
                                          class="block w-full border-gray-300"
                                          v-model="editForm.healthUnit"
                                          required
                                          aria-label="Unidade de saúde"
                                        />
                                      </div>

                                      <div class="space-y-1">
                                        <label for="cns" class="sr-only">CNS</label>
                                        <Input
                                          id="cns"
                                          type="text"
                                          placeholder="CNS"
                                          class="block w-full border-gray-300"
                                          v-model="editForm.cns"
                                          required
                                          aria-label="CNS"
                                        />
                                      </div>

                                      <div class="flex space-x-2">
                                        <div class="flex-1">
                                          <label for="codeFile" class="sr-only">Cód ficha</label>
                                          <Input
                                            id="codeFile"
                                            type="text"
                                            placeholder="Cód ficha"
                                            class="block w-full border-gray-300"
                                            v-model="editForm.codeFile"
                                            required
                                            aria-label="Cód ficha"
                                          />
                                        </div>
                                        <div class="flex-1">
                                          <label for="fileDate" class="sr-only">Data ficha</label>
                                          <Input
                                            id="fileDate"
                                            type="date"
                                            placeholder="Data ficha"
                                            class="block w-full border-gray-300"
                                            v-model="editForm.fileDate"
                                            required
                                            aria-label="Data ficha"
                                          />
                                        </div>
                                      </div>

                                      <div class="space-y-1">
                                        <label for="professional" class="sr-only">Profissional</label>
                                        <Input
                                          id="professional"
                                          type="text"
                                          placeholder="Profissional"
                                          class="block w-full border-gray-300"
                                          v-model="editForm.professional"
                                          required
                                          aria-label="Profissional"
                                        />
                                      </div>

                                      <div class="flex space-x-2">
                                        <div class="flex-1">
                                          <label for="vaccine" class="sr-only">Vacina</label>
                                          <Input
                                            id="vaccine"
                                            type="text"
                                            placeholder="Vacina"
                                            class="block w-full border-gray-300"
                                            v-model="editForm.vaccine"
                                            required
                                            aria-label="Vacina"
                                          />
                                        </div>
                                        <div class="flex-1">
                                          <label for="dose" class="sr-only">Dose</label>
                                          <Input
                                            id="dose"
                                            type="text"
                                            placeholder="Dose"
                                            class="block w-full border-gray-300"
                                            v-model="editForm.dose"
                                            required
                                            aria-label="Dose"
                                          />
                                        </div>
                                      </div>
                                    </div>
                                  </div>
                                  <div class="mt-6 flex justify-end">
                                    <div>
                                      <Button
                                        type="submit"
                                        variant="success-outline"
                                        class="w-full justify-center gap-2"
                                        :disabled="editForm.processing"
                                        aria-label="Cancelar"
                                        @click="open = !open"
                                      >
                                        <span>Cancelar</span>
                                      </Button>
                                    </div>
                                    <div class="px-2">
                                      <Button
                                        type="submit"
                                        variant="success"
                                        class="w-full justify-center gap-3"
                                        :disabled="editForm.processing"
                                        aria-label="Salvar"
                                      >
                                        <span>Salvar</span>
                                      </Button>
                                    </div>
                                  </div>
                                </form>
                              </div>
                            </DialogPanel>
                          </TransitionChild>
                        </div>
                      </Dialog>
                    </TransitionRoot>
                    <InfoWindow
                      v-if="isCursorOnMarker(marker)"
                      :options="{
                        position: patientLocation(marker, true),
                      }"
                      @closeclick="patientCursorLocal = null"
                    >
                      <div id="content">
                        <div id="bodyContent" class="h-auto w-96 p-1">
                          <div class="flex flex-col justify-between rounded-2xl bg-white p-5">
                            <div class="py-3">
                              <router-link v-if="marker" :to="{ name: 'PatientDetails', params: { id: marker.id } }">
                                <p class="text-xl font-semibold capitalize">
                                  {{ marker && marker.name.toLowerCase() }}
                                </p>
                              </router-link>
                              <p class="text-xs text-gray-500">ID: {{ marker.id }}</p>
                            </div>
                            <hr class="border-1 border border-dotted border-gray-300" />
                            <div class="flex justify-between py-5">
                              <p
                                class="justify-center rounded-full bg-gray-50 px-1 py-1 text-sm font-normal text-black"
                              >
                                3 months
                              </p>
                              <p
                                v-if="0 !== marker.alerts.length"
                                class="rounded-full bg-red-100 px-1 py-1 text-sm font-normal text-red-900"
                              >
                                vaccine with delay: {{ marker.alerts.join(', ') }}
                              </p>
                            </div>
                            <div class="mb-1 rounded-2xl border border-transparent px-3 py-2 font-normal text-gray-500">
                              <div class="text-sm font-semibold">
                                <p class="text-sm">
                                  Alertas por protocolo:
                                  <span
                                    :class="{
                                      'rounded-full !bg-red-100 py-1 px-2 text-red-800 ':
                                        marker.number_of_alerts_by_protocol > 0,
                                    }"
                                    class="rounded-full bg-gray-50 py-1 px-2 font-normal"
                                  >
                                    {{ marker.number_of_alerts_by_protocol }} alertas
                                  </span>
                                </p>
                                <p class="text-sm font-semibold">
                                  Birthdate:
                                  <span class="font-normal">{{
                                    format(new Date(marker.birth_date), 'dd/MM/yyyy')
                                  }}</span>
                                </p>
                                <p class="text-sm font-semibold">
                                  Address: <span class="font-normal">{{ marker.address.formatted_address }}</span>
                                </p>
                              </div>
                            </div>
                          </div>

                          <div class="flex justify-evenly py-3">
                            <Button
                              type="submit"
                              variant="success-outline"
                              @click="moveMarker($event, marker.id)"
                              class="mx-2 gap-2 focus:outline-none"
                              :disabled="editForm.processing"
                              v-slot="{ iconSizeClasses }"
                            >
                              <HandIcon aria-hidden="true" :class="iconSizeClasses" />
                              <span>Mover</span>
                            </Button>
                            <PopoverButton :class="{ 'relative z-30': open }">
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
              </div>
            </MarkerCluster>
          </template>
        </GoogleMap>

        <div
          v-if="showEmptyResult && geoCoderQuery"
          class="shadow-b-md shadow-l-md shadow-r-md absolute flex w-full flex-col rounded rounded-b-2xl border border-gray-200 bg-white py-60 shadow"
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
  </div>
</template>

<script setup>
import { defineComponent, reactive, computed, onBeforeUpdate, onMounted, watch, ref, onUnmounted,onBeforeUnmount } from 'vue'
import { GoogleMap, Marker, CustomMarker, MarkerCluster, InfoWindow, Polygon } from 'vue3-google-map'
import { useGeolocation } from '@/composables/useGeolocation'
import { parseISO, formatRelative, formatDuration, add, setDefaultOptions, differenceInMonths, format } from 'date-fns'
import { Popover, PopoverButton, PopoverPanel, PopoverOverlay } from '@headlessui/vue'
import { TransitionRoot, TransitionChild, Dialog, DialogOverlay, DialogPanel, DialogTitle } from '@headlessui/vue'

import { HandIcon, PencilIcon, SaveIcon } from '@heroicons/vue/solid'
import { MapIcon, TableIcon, UsersIcon, XIcon } from '@heroicons/vue/outline'
import { useRouter } from 'vue-router'
import { usePatientsStore } from '@/stores/patients'
import { useMicroRegionsStore } from '@/stores/microregions'
import { useStorage } from '@vueuse/core'
import { Switch } from '@headlessui/vue'
import { useLoggedUserStore } from '@/stores/loggedUser'

const enabled = ref(false)

import RegionForm from '@/components/atoms/RegionForm.vue'

const loggedUserStore = useLoggedUserStore()
const itemRefs = ref([])

const GOOGLE_MAP_API_KEY = ref(import.meta.env.VITE_GOOGLE_MAP_API_KEY)
const patientsStore = usePatientsStore()
const microregionsStore = useMicroRegionsStore()
const router = useRouter()
const map = ref(null)
const mapRef = ref(null)
const geoCoder = ref(null)
const onlyAlerts = ref(false)
const selectedItem = ref(null)
const drawingManager = ref(null)
const movingPatientId = ref(null)

const props = defineProps({
  center: {
    type: Object,
    default: null,
  },
  zoom: {
    type: Number,
    default: 5,
  },
  patients: {
    type: Array,
    default: [],
  },
  patientCursor: {
    type: String,
    default: '0',
  },
})

const showList = ref(false);
const dropdown = ref(null);

const markerIconNormal = ref({
  url: 'marker.svg',
  fillOpacity: 0.6,
  strokeWeight: 0,
  scale: 2,
})
const markerIconEditing = ref({
  url: 'marker-editing.svg',
  fillOpacity: 0.6,
  strokeWeight: 0,
  scale: 2,
})
const markerIconDisabled = ref({
  url: 'marker-disabled.svg',
  fillOpacity: 0.6,
  strokeWeight: 0,
  scale: 2,
})
const markerIconAlert = ref({
  url: 'marker-alert.svg',
  fillOpacity: 0.6,
  strokeWeight: 0,
  scale: 2,
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
const isMapView = ref(true)

const toggleView = () => {
  isMapView.value = !isMapView.value
}
const handleOutsideClick = (event) => {
  if (!dropdown.value.contains(event.target)) {
    showList.value = false;
  }
}

function onItemClick(item) {
  selectedItem.value = item
  console.log(`Item clicado: ${item}`)
}

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

const geoCoderQuery = ref(
  loggedUserStore.item.client.city.charAt(0).toUpperCase() + loggedUserStore.item.client.city.slice(1)
)
const currentCenter = ref(undefined)
const showEmptyResult = ref(false)
const searchAddress = () => {
  //center.value = { lat: -22.749940, lng: -50.576540 }

  geocodeAddress(geoCoder.value, map.value)
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

const patientCursorLocal = ref(props.patientCursor)
const isCursorOnMarker = computed(() => (marker) => {
  // console.log(`${marker.id} === ${props.patientCursor} || ${marker.id} === ${patientCursorLocal.value}`)
  // console.log(`${(marker.id === props.patientCursor || marker.id === patientCursorLocal.value)} = ${(marker.id === props.patientCursor)} || ${(marker.id === patientCursorLocal.value)}`)
  return marker.id === props.patientCursor || marker.id === patientCursorLocal.value
})

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

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
// const isOpen = ref(true) // You can control this variable to show or hide the modal

const addressQuery = ref([])
const infoWindowsOpened = ref([])

const googleLabels = ref([])

const updateLabel = async ({ localPolygon, polygonIndex }) => {
  try {
    if (0 === localPolygon.id) {
      await microregionsStore.createMicroRegion(localPolygon)
      let bounds = new google.maps.LatLngBounds()
      googlePolygons.value[polygonIndex].getPath().forEach((latLng) => bounds.extend(latLng))
      // map.value.fitBounds(bounds) // centraliza

      let center = bounds.getCenter()
      // polygon name text label
      googleLabels.value.push(
        new google.maps.Marker({
          position: center,
          label: {
            text: `${localPolygon.name}`,
            color: 'black',
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
    } else {
      await microregionsStore.updateMicroRegion(localPolygon.id, { name: localPolygon.name })
      googleLabels.value[polygonIndex].setLabel(localPolygon.name)
      polygons.value[polygonIndex].name = localPolygon.name
    }

    currentInfoWindowIndex.value = null
  } catch (error) {
    console.log(error)
  }
}

const googlePolygons = ref([])
watch(
  () => mapRef.value?.ready,
  async (ready) => {
    if (!ready) return
    map.value = mapRef.value.map
    geoCoder.value = new mapRef.value.api.Geocoder()

    // Emitir um evento quando o geoCoder estiver pronto
    emit('geoCoderReady', geoCoder.value)

    // do something with the api using `mapRef.value.api`
    // or with the map instance using `mapRef.value.map`

    currentCenter.value = props.center ? props.center : geocodeAddress(geoCoder.value, map.value)

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
        const newPolygon = event.overlay
        googlePolygons.value.push(newPolygon)
        showInfoWindow(googlePolygons.value.length - 1)
      }
    })

    google.maps.event.addListener(map.value, 'click', (event) => {
      // Verifica se o clique ocorreu dentro de algum polígono
      googlePolygons.value.forEach((polygon, polygonIndex) => {
        if (google.maps.geometry.poly.containsLocation(event.latLng, polygon)) {
          showInfoWindow(polygonIndex)
        }
      })
    })

    await microregionsStore.fetchMicroRegions()
    polygons.value = microregionsStore.items

    // Carrega polígonos salvos da API ao inicializar o mapa
    polygons.value.map((polygon) => {
      const googlePolygon = new google.maps.Polygon({
        paths: polygon.coordinates,
        fillColor: '#FFA901',
        strokeColor: '#4FA9DD',
        fillOpacity: 0.5,
        strokeWeight: 1,
        clickable: false,
        editable: true,
        zIndex: 1,
      })
      googlePolygons.value.push(googlePolygon)

      const vertices = googlePolygon.getPath()
      // google.maps.event.addListener(vertices, 'set_at', function (event) {
      //   // console.log('A vértice ' + index + ' do polígono foi movida pa
      //   const polygonCoordinates = []
      //   vertices.forEach(function (vertex) {
      //     polygonCoordinates.push({
      //       lat: vertex.lat(),
      //       lng: vertex.lng(),
      //     })
      //   })
      //   polygonCoordinates.forEach(function (p, k) {
      //     googlePolygons.value[polygonIndex][k] = { ...p, ...googlePolygons.value[polygonIndex][k].alert }
      //   })
      // })

      let bounds = new google.maps.LatLngBounds()
      googlePolygon.getPath().forEach((latLng) => bounds.extend(latLng))
      // map.value.fitBounds(bounds) // centraliza

      let center = bounds.getCenter()
      // polygon name text label
      googleLabels.value.push(
        new google.maps.Marker({
          position: center,
          label: {
            text: `${polygon.name}`,
            color: 'black',
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
      //const marker = new google.maps.Marker({
      //  map: resultsMap,
      //  position: results[0].geometry.location
      //})
    } else {
      showEmptyResult.value = true
    }
  })
}

const polygons = ref([])

onMounted(async () => {
  await patientsStore.fetchPatients()
  document.addEventListener('click', handleOutsideClick);
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleOutsideClick);
});

const markers = ref([])
onBeforeUpdate(() => {
  markers.value = []
})

const isDraggable = computed(() => (index) => index == movingPatientId.value)

// const maxPatientsToProcess = 30
const patients = computed(() => {
  return props.patients.filter((patient, index) => {
    // if (index >= maxPatientsToProcess) {
    //   return false
    // }
    const hasLatitude = patient.address && patient.address.latitude
    const hasAlerts = patient.alerts && patient.alerts.length > 0

    // Quando onlyAlerts.value for true, considerar apenas pacientes que possuem latitude e alerts.
    // Quando onlyAlerts.value for false, considerar apenas pacientes que possuem latitude.
    return onlyAlerts.value ? hasLatitude && hasAlerts : hasLatitude
  })
})

watch(onlyAlerts, (newOnlyAlerts, oldValue) => {
  emit('update:onlyAlerts', newOnlyAlerts)
})

const patientCursorLocalWhileMoving = ref(null)
function moveMarker(event, index) {
  patientCursorLocalWhileMoving.value = patientCursorLocal.value
  patientCursorLocal.value = null
  movingPatientId.value = index
}

async function handleMarkerDrag(event, patientId) {
  console.log('dragend', event.latLng.lat(), event.latLng.lng())

  const latitude = event.latLng.lat()
  const longitude = event.latLng.lng()

  patientCursorLocal.value = patientCursorLocalWhileMoving.value

  emit('dragend', { patientId, latitude, longitude })
  movingPatientId.value = null
  await patientsStore.movePatient(patientId, {
    address: [
      {
        id: 1,
        latitude,
        longitude,
      },
    ],
  })
}

const emit = defineEmits(['update:markers-in-view', 'update:onlyAlerts', 'dragend', 'geoCoderReady'])

const patientsInView = ref([])
const getMarkersInView = () => {
  const mapBounds = mapRef.value.map.getBounds()
  patientsInView.value = patients.value.filter((marker) => mapBounds.contains(patientLocation.value(marker)))
  emit('update:markers-in-view', patientsInView.value)
}

const deletePolygon = async (polygonIndex) => {
  const confirmed = confirm('Tem certeza que deseja excluir este polígono?')
  if (confirmed) {
    await microregionsStore.deleteMicroRegion(polygons.value[polygonIndex].id)

    polygons.value.splice(polygonIndex, 1)
    googlePolygons.value.splice(polygonIndex, 1)

    currentInfoWindowIndex.value = null
    googleLabels.value[polygonIndex].setLabel('')
    googleLabels.value.splice(polygonIndex, 1)
  }
}

const { coords } = useGeolocation()
const userLocation = computed(() => ({
  lat: coords.value.latitude,
  lng: coords.value.longitude,
}))
const patientLocation = computed(() => (patientMarker, offset = false) => {
  if (offset) {
    return { lat: patientMarker.address.latitude + 0.0001, lng: patientMarker.address.longitude }
  }
  return { lat: patientMarker.address.latitude, lng: patientMarker.address.longitude }
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
  width: 650px !important;
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
