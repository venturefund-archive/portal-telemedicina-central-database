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
      items.value = response.data.features
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

  return {
    items,
    item,
    fetchMicroRegions,
    searchMicroRegions,
    fetchMicroRegion,
  }
})
