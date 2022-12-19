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
      const response = await axios.get('/api/users/me/', {
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
    item,
    fetchMe,
  }
})
