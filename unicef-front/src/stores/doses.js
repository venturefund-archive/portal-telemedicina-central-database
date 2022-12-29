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
      const response = await axios.get(`/api/vaccines/doses?patient_id=${patientsStore.item.id}`, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      this.items = response.data
    } catch (err) {
      errorToast({ text: err.message })
    }
  }

  return {
    items,
    item,
    fetchDoses,
  }
})
