import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useStorage } from '@vueuse/core'
import axios from 'axios'
import { errorToast } from '@/toast'

export const usePatientsStore = defineStore('patients', () => {
  const items = ref([])
  const item = ref(null)
  const next_url = ref(null)
  const isLoading = ref(false)
  const state = useStorage('app-store', { token: '' })

  const fetchPatients = async () => {
    try {
      isLoading.value = true

      // Chamar a função auxiliar com a URL inicial
      const response = await axios.get(import.meta.env.VITE_API_URL + '/api/patients/', {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      isLoading.value = false
      next_url.value = response.data.next_url
      items.value = response.data.results
    } catch (err) {
      isLoading.value = false
      console.log(err)
      err.response && errorToast({ text: err.response.data.detail })
    }

    return items.value
  }

  const fetchPatientsRecursive = async (nextUrl) => {
    try {
      isLoading.value = false
      const response = await axios.get(!nextUrl ? next_url.value : nextUrl, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })

      next_url.value = response.data.next_url
      items.value.push(...response.data.results)
      console.log(items.value.length)

      // Verificar se existe um next_url e, em caso afirmativo, chamar recursivamente a função auxiliar
      if (next_url.value) {
        // shouldStop.value = true
        return await fetchPatientsRecursive(next_url.value)
      }
      return response.data.results
    } catch (err) {
      isLoading.value = false
      console.log(err)
      err.response && errorToast({ text: err.response.data.detail })
    }
  }

  async function fetchPatient(id) {
    try {
      isLoading.value = true
      const response = await axios.get(import.meta.env.VITE_API_URL + `/api/patients/${id}/`, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      item.value = response.data
      isLoading.value = false
      state.value.patientLastViewed = id
    } catch (err) {
      isLoading.value = false
      errorToast({ text: err.response.data.detail })
      console.log(err)
    }
  }

  async function movePatient(id, data) {
    try {
      const response = await axios.patch(import.meta.env.VITE_API_URL + `/api/patients/${id}/`, data, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      return response
    } catch (err) {
      console.log(err)
      errorToast({ text: err.response.data.detail })
    }
  }

  return {
    items,
    item,
    isLoading,
    fetchPatients,
    fetchPatientsRecursive,
    fetchPatient,
    movePatient,
  }
})
