import { defineStore } from 'pinia'
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import { useStorage } from '@vueuse/core'
import axios from 'axios'
import { errorToast, successToast } from '@/toast'

export const usePatientsStore = defineStore('patients', () => {
  const items = ref([])
  const item = ref(null)

  async function searchPatients() {
    return await this.fetchPatients()
  }
  async function fetchPatients() {
    const state = useStorage('app-store', { token: '' })
    try {
      const response = await axios.get(import.meta.env.VITE_API_URL + '/api/patients/', {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      this.items = response.data.results
    } catch (err) {
      console.log(err)
      err.response && errorToast({ text: err.response.data.detail })
    }
  }
  async function fetchPatient(id) {
    const state = useStorage('app-store', { token: '' })
    try {
      const response = await axios.get(import.meta.env.VITE_API_URL + `/api/patients/${id}/`, {
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
  async function movePatient(id, data) {
    const state = useStorage('app-store', { token: '' })
    try {
      const response = await axios.patch(import.meta.env.VITE_API_URL + `/api/patients/${id}/`, data, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      return response
    } catch (err) {
      errorToast({ text: err.message })
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
