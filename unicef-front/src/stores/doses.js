import { defineStore } from 'pinia'
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import { useStorage } from '@vueuse/core'
import axios from 'axios'
import { errorToast, successToast } from '@/toast'
import { usePatientsStore } from '@/stores/patients'
const patientsStore = usePatientsStore()

export const useDosesStore = defineStore('doses', () => {
  const items = ref([])
  const item = ref(null)

  async function fetchDoses() {
    const state = useStorage('app-store', { token: '' })
    try {
      const response = await axios.get(
        import.meta.env.VITE_API_URL + `/api/vaccines/doses?patient_id=${patientsStore.item.id}`,
        {
          headers: {
            'Content-type': 'application/json',
            Authorization: `token ${state.value.token}`,
          },
        }
      )
      this.items = response.data
    } catch (err) {
      errorToast({ text: err.message })
      console.log(err)
    }
  }

  async function updateDose(id, data) {
    return data.active ? await deactivateDose(id, data) : await activateDose(id, data)
  }

  async function activateDose(id, data) {
    const state = useStorage('app-store', { token: '' })
    try {
      const response = await axios.patch(import.meta.env.VITE_API_URL + `/api/vaccines/alerts/${id}/activate/`, data, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      return response
    } catch (err) {
      errorToast({ text: err })
      console.log(err)
    }
  }

  async function deactivateDose(id, data) {
    const state = useStorage('app-store', { token: '' })
    try {
      const response = await axios.patch(
        import.meta.env.VITE_API_URL + `/api/vaccines/alerts/${id}/deactivate/`,
        data,
        {
          headers: {
            'Content-type': 'application/json',
            Authorization: `token ${state.value.token}`,
          },
        }
      )
      return response
    } catch (err) {
      errorToast({ text: err })
      console.log(err)
    }
  }

  return {
    items,
    item,
    fetchDoses,
    updateDose,
  }
})
