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
                      class="w-full rounded-lg border py-2 pl-10 pr-3 focus:outline-none focus:ring focus:ring-green-500 focus:ring-offset-white"
                    />
                  </div>
                  <div v-if="isMapView">
                    <Input
                      :placeholder="$t('manager.search-map')"
                      v-model="geoCoderQuery"
                      class="w-full rounded-lg border py-2 pl-10 pr-3 focus:outline-none focus:ring focus:ring-green-500 focus:ring-offset-white"
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
                  v-if="node_env == 'development'"
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
                <button @click="toggleView" class="flex flex-col items-center" v-if="node_env == 'development'">
                  <TableIcon v-if="isMapView" class="h-8 w-9 text-gray-500" />
                  <MapIcon v-else class="h-7 w-10 text-gray-500" />
                  <span class="text-sm text-gray-500">{{ $t('manager.visualization') }}</span>
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
                  editable: false,
                  zIndex: 1,
                }"
              />
              <InfoWindow
                v-if="currentInfoWindowIndex === polygonIndex"
                @closeclick="closeInfoWindowHandler(polygonIndex)"
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
                  @saved="updatePolygon"
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
                >
                  <InfoWindow
                    v-if="isCursorOnMarker(marker)"
                    @closeclick="patientCursorLocal = null"
                    :ref="
                      (el) => {
                        markerInfoWindows[marker.id] = el
                      }
                    "
                  >
                    <div id="content">
                      <div id="bodyContent" class="h-auto w-96 p-1">
                        <div class="rounded-lg p-6">
                          <header class="mb-4">
                            <h2 class="text-xl font-semibold capitalize" v-if="marker">
                              {{ marker && marker.name.toLowerCase() }}
                            </h2>
                            <p class="text-sm text-gray-500">ID: {{ marker.id }}</p>
                            <hr class="my-3 w-full border border-dashed" />
                          </header>

                          <div class="mb-4">
                            <div class="flex justify-between">
                              <span
                                class="mr-2 inline-block rounded-full bg-gray-100 px-3 py-1 text-sm lowercase text-black"
                              >
                                {{ formatAge(marker.age_in_days) }}
                              </span>
                              <p class="text-sm">
                                <span
                                  :class="{
                                    'bg-red-100 text-red-800': marker.number_of_alerts_by_protocol > 0,
                                    'bg-gray-100 text-gray-500': marker.number_of_alerts_by_protocol === 0,
                                  }"
                                  class="mr-2 inline-block rounded-full px-3 py-1 text-sm text-black"
                                >
                                  {{ marker.number_of_alerts_by_protocol }} alerta por protocolo
                                </span>
                              </p>
                            </div>
                            <div v-if="0 !== marker.alerts.length" class="inline-block pb-3 pt-2">
                              <p class="pt-1 text-sm font-medium text-gray-600">Vacinas em atraso:</p>
                              <span
                                v-for="alert in marker.alerts"
                                :key="alert.id"
                                class="mr-2 mt-1 inline-block rounded-full bg-red-100 px-3 py-1 text-xs text-red-900"
                              >
                                {{ alert }}
                              </span>
                            </div>
                          </div>

                          <div class="mb-2 flex">
                            <p class="pr-1 text-sm font-medium text-gray-600">Birthdate:</p>
                            <p class="text-sm">
                              {{ format(new Date(marker.birth_date), 'dd/MM/yyyy') }}
                            </p>
                          </div>

                          <div class="flex">
                            <p class="pr-1 text-sm font-medium text-gray-600">Address:</p>
                            <p class="text-sm">
                              {{ marker.address.formatted_address }}
                            </p>
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
                          <Button
                            type="button"
                            variant="success"
                            class="mx-2 gap-2 bg-white focus:outline-none"
                            @click="isModalOpen = true"
                            v-slot="{ iconSizeClasses }"
                          >
                            <PencilIcon aria-hidden="true" :class="iconSizeClasses" />
                            <span>Editar</span>
                          </Button>
                        </div>
                      </div>
                    </div>

                    <Dialog
                      as="div"
                      class="fixed inset-0 z-10 overflow-y-auto"
                      :open="isModalOpen"
                      @close="isModalOpen = false"
                    >
                      <div class="flex min-h-screen items-center justify-center">
                        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
                        <!-- Overlay -->

                        <!-- This is the modal -->
                        <div class="relative mx-auto max-w-xl space-y-4 rounded-xl bg-white p-6 shadow drop-shadow">
                          <div class="flex items-center justify-between">
                            <Dialog-title as="h3" class="mx-auto text-xl font-medium leading-6 text-gray-700"
                              >Editar Informações</Dialog-title
                            >
                            <button
                              @click="isModalOpen = false"
                              class="mb-2 rounded p-0.5 hover:bg-gray-100 focus:outline-none"
                            >
                              <XIcon class="h-6 w-6 text-gray-500 hover:text-green-500" />
                            </button>
                          </div>
                          <hr class="my-3 w-full border border-dashed" />
                          <!-- Form fields -->
                          <form @submit.prevent="handleSubmit" class="py-5">
                            <div class="grid grid-cols-2 gap-4">
                              <!-- Personal Data -->
                              <div class="space-y-3">
                                <h4 class="pb-6 text-center text-sm font-semibold text-gray-600">Dados pessoais</h4>

                                <label for="name" class="block text-sm font-medium text-gray-700">Nome</label>
                                <Input
                                  placeholder="name"
                                  id="name"
                                  type="text"
                                  class="w-full border-gray-300 focus:border-lime-300"
                                  v-model="editForm.name"
                                  required
                                />

                                <label for="birthDate" class="block text-sm font-medium text-gray-700"
                                  >Data de Nascimento</label
                                >
                                <Input
                                  id="birthDate"
                                  type="date"
                                  class="w-full border-gray-300 focus:border-lime-300"
                                  v-model="editForm.birthDate"
                                  required
                                />

                                <label for="age" class="block text-sm font-medium text-gray-700">Idade</label>
                                <Input
                                  placeholder="age"
                                  id="age"
                                  type="number"
                                  class="w-full border-gray-300 focus:border-lime-300"
                                  v-model="editForm.age"
                                  required
                                />

                                <label for="address" class="block text-sm font-medium text-gray-700">Endereço</label>
                                <Input
                                  placeholder="address"
                                  id="address"
                                  type="text"
                                  class="w-full border-gray-300 focus:border-lime-300"
                                  v-model="editForm.address"
                                  required
                                />

                                <label for="cpf" class="block text-sm font-medium text-gray-700">CPF</label>
                                <Input
                                  placeholder="document"
                                  id="document"
                                  type="text"
                                  class="w-full border-gray-300 focus:border-lime-300"
                                  v-model="editForm.cpf"
                                  required
                                />
                              </div>

                              <!-- Clinical Data -->
                              <div class="space-y-3">
                                <h4 class="pb-6 text-center text-sm font-semibold text-gray-600">Dados clínicos</h4>

                                <label for="healthUnit" class="block text-sm font-medium text-gray-700"
                                  >Unidade de saúde</label
                                >
                                <Input
                                  placeholder="Unidade de saúde"
                                  id="healthUnit"
                                  type="text"
                                  class="w-full border-gray-300 focus:border-lime-300"
                                  v-model="editForm.healthUnit"
                                  required
                                />

                                <label for="cns" class="block text-sm font-medium text-gray-700">CNS</label>
                                <Input
                                  placeholder="cns"
                                  id="CNS"
                                  type="text"
                                  class="w-full border-gray-300 focus:border-lime-300"
                                  v-model="editForm.cns"
                                  required
                                />

                                <div class="flex">
                                  <div class="flex-1 pr-3">
                                    <label for="codeFile" class="block text-sm font-medium text-gray-700"
                                      >Cód ficha</label
                                    >
                                    <Input
                                      placeholder="Cód ficha"
                                      id="codeFile"
                                      type="text"
                                      class="w-full border-gray-300 focus:border-lime-300"
                                      v-model="editForm.codeFile"
                                      required
                                    />
                                  </div>
                                  <div class="flex-1">
                                    <label for="fileDate" class="block text-sm font-medium text-gray-700"
                                      >Data ficha</label
                                    >
                                    <Input
                                      placeholder="Data ficha"
                                      id="fileDate"
                                      type="date"
                                      class="w-full border-gray-300 focus:border-lime-300"
                                      v-model="editForm.fileDate"
                                      required
                                    />
                                  </div>
                                </div>

                                <label for="professional" class="block text-sm font-medium text-gray-700"
                                  >Profissional</label
                                >
                                <Input
                                  placeholder="profissional"
                                  id="professional"
                                  type="text"
                                  class="w-full border-gray-300 focus:border-lime-300"
                                  v-model="editForm.professional"
                                  required
                                />

                                <div class="flex space-x-2">
                                  <div class="flex-1">
                                    <label for="vaccine" class="block text-sm font-medium text-gray-700">Vacina</label>
                                    <Input
                                      placeholder="vaccine"
                                      id="vaccine"
                                      type="text"
                                      class="w-full border-gray-300 focus:border-lime-300"
                                      v-model="editForm.vaccine"
                                      required
                                    />
                                  </div>
                                  <div class="flex-1">
                                    <label for="dose" class="block text-sm font-medium text-gray-700">Dose</label>
                                    <Input
                                      placeholder="dose"
                                      id="dose"
                                      type="text"
                                      class="w-full border-gray-300 focus:border-lime-300"
                                      v-model="editForm.dose"
                                      required
                                    />
                                  </div>
                                </div>
                              </div>
                            </div>

                            <!-- Buttons -->
                            <div class="flex justify-end pt-10">
                              <Button type="button" variant="success-outline" class="mr-3" @click="isModalOpen = false">
                                Cancelar
                              </Button>
                              <Button type="submit" variant="success"> Salvar </Button>
                            </div>
                          </form>
                        </div>
                      </div>
                    </Dialog>
                  </InfoWindow>
                </Marker>
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
import {
  defineComponent,
  reactive,
  computed,
  onBeforeUpdate,
  onMounted,
  watch,
  ref,
  onUnmounted,
  onBeforeUnmount,
} from 'vue'
import { GoogleMap, Marker, CustomMarker, MarkerCluster, InfoWindow, Polygon } from 'vue3-google-map'
import { useGeolocation } from '@/composables/useGeolocation'
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
import { useI18n } from 'vue3-i18n'
import RegionForm from '@/components/atoms/RegionForm.vue'

const node_env = ref(import.meta.env.NODE_ENV)
// const dataAtual = new Date();

// const idadeEmAnos = differenceInYears(dataAtual, dataNascimento);
// const idadeEmMeses = differenceInMonths(dataAtual, dataNascimento);
// const idadeEmDiasRestantes = differenceInDays(dataAtual, dataNascimento);

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

const { t } = useI18n()
const enabled = ref(false)

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

const showList = ref(false)
const dropdown = ref(null)

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
  name: '',
  birthDate: '',
  healthUnit: '',
  cns: '',
  codeFile: '',
  fileDate: '',
  professional: '',
  vaccine: '',
  dose: '',
  processing: false,
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

const isMapView = ref(true)

const toggleView = () => {
  isMapView.value = !isMapView.value
}
const handleOutsideClick = (event) => {
  if (!dropdown.value.contains(event.target)) {
    showList.value = false
  }
}

function onItemClick(item) {
  selectedItem.value = item
  console.log(`Item clicado: ${item}`)
}

const geoCoderQuery = ref(
  loggedUserStore.item.client.city.charAt(0).toUpperCase() + loggedUserStore.item.client.city.slice(1)
)
const currentCenter = ref(undefined)
const showEmptyResult = ref(false)
const searchAddress = () => {
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

const isModalOpen = ref(false)
// const isOpen = ref(true) // You can control this variable to show or hide the modal

const addressQuery = ref([])
const infoWindowsOpened = ref([])

const googleLabels = ref([])

const updatePolygon = async ({ localPolygon, polygonIndex }) => {
  try {
    console.log(localPolygon)
    console.log(polygonIndex)
    if (0 === localPolygon.id) {
      await microregionsStore.createMicroRegion(localPolygon)
      polygons.value.push(microregionsStore.item)
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
        editable: false,
      },
    })

    // Set the drawing manager to draw on the map instance
    drawingManager.value.setMap(mapRef.value.map)

    // Adiciona um ouvinte de evento para quando o usuário termina de desenhar um polígono
    google.maps.event.addListener(drawingManager.value, 'overlaycomplete', (event) => {
      if (event.type === google.maps.drawing.OverlayType.POLYGON) {
        const newPolygon = event.overlay
        googlePolygons.value.push(newPolygon)

        // Adiciona um ouvinte de clique ao novo polígono
        google.maps.event.addListener(newPolygon, 'click', (clickEvent) => {
          // Encontrar o índice do novo polígono na matriz googlePolygons
          const polygonIndex = googlePolygons.value.indexOf(newPolygon)

          // Verifica se o clique ocorreu dentro deste polígono
          if (google.maps.geometry.poly.containsLocation(clickEvent.latLng, newPolygon)) {
            showInfoWindow(polygonIndex)
          }
        })

        // Mostrar a janela de informações imediatamente após o polígono ser desenhado
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
        editable: false,
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
  document.addEventListener('click', handleOutsideClick)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleOutsideClick)
})

const markerInfoWindows = ref([])
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

// const patientCursorLocalWhileMoving = ref(null)
function moveMarker(event, index) {
  // patientCursorLocalWhileMoving.value = patientCursorLocal.value
  // patientCursorLocal.value = null
  movingPatientId.value = index
  console.log(markerInfoWindows.value[index])
}

async function handleMarkerDrag(event, patientId) {
  console.log('dragend', event.latLng.lat(), event.latLng.lng())

  const latitude = event.latLng.lat()
  const longitude = event.latLng.lng()

  // markerInfoWindows[movingPatientId.value].value.open()
  // patientCursorLocal.value = patientCursorLocalWhileMoving.value

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

const closeInfoWindowHandler = (polygonIndex) => {
  if (polygons.value.length == polygonIndex) {
    googlePolygons.value[polygonIndex].setMap(null)
    googlePolygons.value.splice(polygonIndex, 1)
    googleLabels.value[polygonIndex].setLabel('')
    googleLabels.value.splice(polygonIndex, 1)
  }
  showInfoWindow(null)
}

const deletePolygon = async (polygonIndex) => {
  console.log(polygons.value.length)
  console.log(polygonIndex)
  console.log(polygons.value[polygonIndex])
  if (polygons.value.length - 1 == polygonIndex) {
    googlePolygons.value[polygonIndex].setMap(null)
    googlePolygons.value.splice(polygonIndex, 1)
    googleLabels.value[polygonIndex].setLabel('')
    googleLabels.value.splice(polygonIndex, 1)
    showInfoWindow(null)
    return
  }
  const confirmed = confirm('Tem certeza que deseja excluir este polígono?')
  if (confirmed) {
    await microregionsStore.deleteMicroRegion(polygons.value[polygonIndex].id)

    polygons.value.splice(polygonIndex, 1)
    googlePolygons.value.splice(polygonIndex, 1)

    showInfoWindow(null)
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
