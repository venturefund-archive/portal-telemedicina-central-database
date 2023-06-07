import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useStorage } from '@vueuse/core'
import axios from 'axios'
import { errorToast } from '@/toast'

export const useMicroRegionsStore = defineStore('microregions', () => {
  const items = ref([])
  const item = ref(null)
  const state = useStorage('app-store', { token: '' })

  async function searchMicroRegions() {
    return await fetchMicroRegions()
  }

  async function fetchMicroRegions() {
    const state = useStorage('app-store', { token: '' })
    try {
      const response = await axios.get(import.meta.env.VITE_API_URL + '/api/microregion/', {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      items.value = response.data.features.map((polygon) => {
        return {
          id: polygon.id,
          name: polygon.properties.name,
          coordinates: polygon.geometry.coordinates[0].map((coordinate) => {
            return { lat: coordinate[1], lng: coordinate[0] }
          }),
        }
      })
      polygonNames.value = response.data.features.map((polygon) => polygon.properties.name)
    } catch (err) {
      console.log(err.response)
      err.response && errorToast({ text: err.response.data.detail })
    }
    return items.value
  }

  async function fetchMicroRegion(id) {
    const state = useStorage('app-store', { token: '' })
    try {
      const response = await axios.get(import.meta.env.VITE_API_URL + `/api/microregion/${id}/`, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      this.item = response.data
    } catch (err) {
      errorToast({ text: err.message })
    }
  }

  function formatCoordinates(coordinates) {
    // Clone as coordenadas para evitar a modificação do array original
    const formattedCoordinates = [...coordinates]

    // Verifica se o polígono já está fechado
    const firstPoint = formattedCoordinates[0]
    const lastPoint = formattedCoordinates[formattedCoordinates.length - 1]

    // Se o polígono não estiver fechado, adicione o primeiro ponto ao final
    if (firstPoint[0] !== lastPoint[0] || firstPoint[1] !== lastPoint[1]) {
      formattedCoordinates.push(firstPoint)
    }

    return formattedCoordinates
  }
  async function createMicroRegion(data) {
    const state = useStorage('app-store', { token: '' })
    try {
      const payload = {
        name: data.name,
        polygon: {
          type: 'Polygon',
          coordinates: [formatCoordinates(data.coordinates)],
        },
        client: 1,
      }
      const response = await axios.post(import.meta.env.VITE_API_URL + `/api/microregion/`, payload, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      this.item = response.data
      return this.item
    } catch (err) {
      errorToast({ text: err.message })
    }
  }
  async function updateMicroRegion(id, data) {
    const state = useStorage('app-store', { token: '' })
    try {
      const response = await axios.patch(import.meta.env.VITE_API_URL + `/api/microregion/${id}/`, data, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      this.item = response.data
      return this.item
    } catch (err) {
      errorToast({ text: err.message })
    }
  }

  return {
    items,
    item,
    fetchMicroRegions,
    searchMicroRegions,
    fetchMicroRegion,
    createMicroRegion,
    updateMicroRegion,
  }
})
