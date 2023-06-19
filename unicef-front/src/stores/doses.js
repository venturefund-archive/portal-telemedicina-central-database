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

  async function addVaccine(data) {
    const state = useStorage('app-store', { token: '' })
    try {
      const response = await axios.post(import.meta.env.VITE_API_URL + `/api/vaccines/status/`, data, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })

      if (response && response.data) {
        const updatedItem = response.data
        console.log('updatedItem', updatedItem)
        // console.log('array', items.value)
        const foundedItemIndex = items.value.findIndex((dose) => dose.id === updatedItem.vaccine_dose)

        if (foundedItemIndex !== -1) {
          console.log('aa')
          // Atualizando o item no array de itens
          // console.log(items.value[foundedItemIndex])
          items.value[foundedItemIndex].status = 1
          // items.value[foundedItemIndex].status = { ...items.value[foundedItemIndex].status, completed: updatedItem.completed }
          // console.log(items.value[foundedItemIndex])
        } else {
          // console.log('bb')
          // Se o item não existir, você pode optar por adicioná-lo ao array
          items.value.push(updatedItem)
        }
        item.value = updatedItem

        return updatedItem
      } else {
        throw new Error('No data received from the server.')
      }
    } catch (err) {
      console.log('ppp')
      // Mostra um toast de erro com uma mensagem descritiva
      errorToast({ text: `Failed to add vaccine: ${err.message}` })

      // Rejeitar a promessa com o erro
      return Promise.reject(err)
    }
  }

  return {
    items,
    item,
    fetchDoses,
    updateDose,
    addVaccine,
  }
})
