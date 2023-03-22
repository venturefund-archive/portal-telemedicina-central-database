import { defineStore } from 'pinia'
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import { useStorage } from '@vueuse/core'
import axios from 'axios'
import { errorToast, successToast } from '@/toast'

export const useVaccinesStore = defineStore('vaccines', () => {
  const items = ref([])
  const item = ref(null)

  async function fetchVaccines() {
    const state = useStorage('app-store', { token: '' })
    try {
      const response = await axios.get(import.meta.env.VITE_API_URL + `/api/vaccines/`, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
        params: {
          system: "BRI"
        }
      })
      this.items = response.data
    } catch (err) {
      errorToast({ text: err.message })
    }
  }

  return {
    items,
    item,
    fetchVaccines,
  }
})
