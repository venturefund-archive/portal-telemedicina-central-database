import { defineStore } from 'pinia'
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import { useStorage } from '@vueuse/core'
import axios from 'axios'
import { errorToast, successToast } from '@/toast'

export const useLoggedUserStore = defineStore('loggedUser', () => {
  const item = ref(null)

  async function fetchMe() {
    const state = useStorage('app-store', { token: '' })
    try {
      const response = await axios.get(import.meta.env.VITE_API_URL + '/api/users/me/', {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      this.item = response.data
    } catch (err) {
      state.value.token = null
      if (err.response && err.response.status === 401 && err.response.status === 500) {
        errorToast({ text: err.message })
        throw err
      } else {
        errorToast({ text: err.response.data.detail })
        throw err
      }
    }
  }

  async function updateMe(id, data) {
    const state = useStorage('app-store', { token: '' })
    try {
      const response = await axios.put(import.meta.env.VITE_API_URL + '/api/users/' + id + '/', data, {
        headers: {
          'Content-type': 'application/json',
          Authorization: `token ${state.value.token}`,
        },
      })
      console.log(response.data)
      this.item = response.data
    } catch (err) {
      state.value.token = null
      if (err.response && err.response.status === 401 && err.response.status === 500) {
        errorToast({ text: err.message })
        throw err
      } else {
        errorToast({ text: err.response.data.detail })
        throw err
      }
    }
  }

  return {
    item,
    fetchMe,
    updateMe,
  }
})
