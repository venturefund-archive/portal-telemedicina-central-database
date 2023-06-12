import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useStorage } from '@vueuse/core'
import axios from 'axios'
import { errorToast } from '@/toast'

export const usePatientsStore = defineStore('patients', () => {
  const items = ref([])
  const item = ref(null)
  const isLoading = ref(false)
  const state = useStorage('app-store', { token: '' })

  async function searchPatients() {
    return await fetchPatients()
  }

  const fetchPatients = async () => {
    try {
      isLoading.value = true
      const response = await axios.get(import.meta.env.VITE_API_URL + '/api/patients/', {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      items.value = response.data.results
      isLoading.value = false
    } catch (err) {
      isLoading.value = false
      console.log(err)
      err.response && errorToast({ text: err.response.data.detail })
    }
    return items.value
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
      // const index = items.value.findIndex((item) => item.id === id);
      // console.log(index)
      // if (index !== -1) {
      //   // Mutação de uma maneira detectável
      //   items.value[index] = {
      //     ...items.value[index],
      //     address: {
      //       ...items.value[index].address,
      //       latitude: data.latitude,
      //       longitude: data.longitude,
      //     },
      //   };
      // }
      items.value.find(p => id == p.id).address.latitude = data.latitude
      items.value.find(p => id == p.id).address.longitude = data.longitude
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
    searchPatients,
    fetchPatients,
    fetchPatient,
    movePatient,
  }
})
