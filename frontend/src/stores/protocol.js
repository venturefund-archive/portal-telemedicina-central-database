import { defineStore } from 'pinia'
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import { useStorage } from '@vueuse/core'
import axios from 'axios'
import { errorToast, successToast } from '@/toast'

export const useProtocolStore = defineStore('protocol', () => {
  const items = ref([])
  const item = ref(null)
  const isLoading = ref(false)

  async function fetchProtocol(id) {
    const state = useStorage('app-store', { token: '' })
    try {
      isLoading.value = true
      const response = await axios.get(import.meta.env.VITE_API_URL + `/api/vaccine-protocol/metrics/${id}/`, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      isLoading.value = false
      this.item = response.data
    } catch (err) {
      isLoading.value = false
      errorToast({ text: err.message })
    }
  }

  return {
    items,
    item,
    isLoading,
    fetchProtocol,
  }
})
