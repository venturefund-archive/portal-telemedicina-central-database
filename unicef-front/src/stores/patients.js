import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useStorage } from '@vueuse/core'
import axios from 'axios'
import { errorToast } from '@/toast'

export const usePatientsStore = defineStore('patients', () => {
  const items = ref([])
  const item = ref(null)
  const state = useStorage('app-store', { token: '' })

  async function searchPatients() {
    return await fetchPatients()
  }

  const fetchPatients = async () => {
    try {
      const response = await axios.get(import.meta.env.VITE_API_URL + '/api/patients/', {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      items.value = response.data.results
    } catch (err) {
      console.log(err)
      err.response && errorToast({ text: err.response.data.detail })
    }
    return items.value
  }

  async function fetchPatient(id) {
    try {
      const response = await axios.get(import.meta.env.VITE_API_URL + `/api/patients/${id}/`, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      item.value = response.data
    } catch (err) {
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
      errorToast({ text: err.response.data.detail })
      console.log(err)
    }
  }

  return {
    items,
    item,
    searchPatients,
    fetchPatients,
    fetchPatient,
    movePatient,
  }
})
