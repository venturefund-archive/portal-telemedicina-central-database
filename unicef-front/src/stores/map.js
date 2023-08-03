import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useStorage } from '@vueuse/core'
import axios from 'axios'
import { errorToast } from '@/toast'

export const useMapStore = defineStore('map', () => {
  const polygons = ref([])
  const newPolygon = ref(null)
  const markers = ref([])
  const state = useStorage('app-store', { token: '' })

  async function fetchPolygons() {
    try {
      const response = await axios.get(import.meta.env.VITE_API_URL + '/api/microregion/', {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      polygons.value = response.data.features.map((polygon) => {
        return {
          id: polygon.id,
          name: polygon.properties.name,
          coordinates: polygon.geometry.coordinates[0].map((coordinate) => {
            return { lat: coordinate[1], lng: coordinate[0] }
          }),
        }
      })
    } catch (err) {
      console.log(err)
      err.response && errorToast({ text: err.response.data.detail })
    }
    return polygons.value
  }

  async function fetchPolygon(id) {
    try {
      const response = await axios.get(import.meta.env.VITE_API_URL + `/api/microregion/${id}/`, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      newPolygon.value = response.data
    } catch (err) {
      console.log(err)
      errorToast({ text: err.message })
    }
  }

  function formatCoordinates(coordinates) {
    const formattedCoordinates = [...coordinates]
    const firstPoint = formattedCoordinates[0]
    const lastPoint = formattedCoordinates[formattedCoordinates.length - 1]
    if (firstPoint[0] !== lastPoint[0] || firstPoint[1] !== lastPoint[1]) {
      formattedCoordinates.push(firstPoint)
    }
    return formattedCoordinates
  }

  async function createPolygon(data) {
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
      const polygon = response.data
      newPolygon.value = {
        id: polygon.id,
        name: polygon.properties.name,
        coordinates: polygon.geometry.coordinates[0].map((coordinate) => {
          return { lat: coordinate[1], lng: coordinate[0] }
        }),
      }
      return newPolygon.value
    } catch (err) {
      console.log(err)
      errorToast({ text: err.message })
    }
  }

  async function updatePolygon(id, data) {
    try {
      const response = await axios.patch(import.meta.env.VITE_API_URL + `/api/microregion/${id}/`, data, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      newPolygon.value = response.data
      return newPolygon.value
    } catch (err) {
      console.log(err)
      errorToast({ text: err.message })
    }
  }

  async function deletePolygon(id) {
    try {
      const response = await axios.delete(import.meta.env.VITE_API_URL + `/api/microregion/${id}/`, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
    } catch (err) {
      console.log(err)
      errorToast({ text: err.message })
    }
  }

  async function fetchMarkers() {
    try {
      const response = await axios.get(import.meta.env.VITE_API_URL + '/api/patients/', {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      // isLoading.value = false
      // next_url.value = response.data.next_url
      markers.value = response.data.map((marker) => {
        return {
          id: marker.id,
          position: {
            lat: marker.latitude,
            lng: marker.longitude,
          },
          address: marker.address,
          age: marker.age,
        }
      })
      console.log(err)
    } catch (err) {
      console.log(err)
      err.response && errorToast({ text: err.response.data.detail })
    }
    return markers.value
  }

  async function updateMarker(id, updatedMarker) {
    try {
      const response = await axios.patch(import.meta.env.VITE_API_URL + `/api/patients/${id}/`, updatedMarker, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      const index = markers.value.findIndex((marker) => marker.id === id)
      markers.value[index] = response.data
      return response.data
    } catch (err) {
      console.log(err)
      errorToast({ text: err.message })
    }
  }

  return {
    polygons,
    newPolygon,
    fetchPolygons,
    fetchPolygon,
    createPolygon,
    updatePolygon,
    deletePolygon,
    markers,
    fetchMarkers,
    updateMarker,
  }
})
