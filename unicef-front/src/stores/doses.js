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
      const response = await axios.post(import.meta.env.VITE_API_URL + '/api/vaccines/status/', data, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })

      if (response && response.data) {
        const updatedItem = response.data
        const foundedItemIndex = items.value.findIndex((dose) => dose.id === updatedItem.vaccine_dose)

        if (foundedItemIndex !== -1) {
          // Update item
          items.value[foundedItemIndex].status = {
            completed: updatedItem.completed,
            batch: updatedItem.batch,
            fhir_store: updatedItem.fhir_store,
            application_date: updatedItem.application_date,
            next_dose_application_date: updatedItem.next_dose_application_date,
            health_professional: {
              id: updatedItem.health_professional.id,
              client: updatedItem.health_professional.client,
              name: updatedItem.health_professional.name,
              cns_number: updatedItem.health_professional.cns_number,
              cnes_number: updatedItem.health_professional.cnes_number,
            },
          }
          console.log(items.value[foundedItemIndex])
        } else {
          // Item doesn't exist, so add it to the array
          items.value.push(updatedItem)
        }

        return updatedItem
      } else {
        throw new Error('No data received from the server.')
      }
    } catch (err) {
      // Show an error toast with a descriptive message
      errorToast({ text: `Failed to add vaccine: ${err.message}` })

      // Reject the promise with the error
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
