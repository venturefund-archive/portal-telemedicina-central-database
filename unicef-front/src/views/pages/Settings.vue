<template>
  <PageWrapper>
    <div class="rounded rounded-t-xl py-4">
      <h2 class="mt-10 text-2xl font-semibold text-gray-700">Configurações</h2>
    </div>
    <div class="h-full rounded-xl border border-gray-100 bg-white px-16 py-16 shadow">
      <h3 class="text-xl font-semibold text-gray-700">Editar dados da conta</h3>
      <hr class="my-4 text-gray-200" />
      <form @submit.prevent="submitForm" class="flex w-full flex-col sm:w-96">
        <div class="flex w-full flex-col p-4">
          <Input
            v-model="formData.username"
            type="text"
            id="username"
            class="rounded border border-gray-300 p-2"
            placeholder="username"
          />
          <Input
            v-model="formData.name"
            type="text"
            id="name"
            class="rounded border border-gray-300 p-2"
            placeholder="Nome completo"
            required
          />
        </div>

        <div class="flex w-full justify-end p-4">
          <button type="submit" class="rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-600">
            Salvar
          </button>
        </div>
      </form>
    </div>
  </PageWrapper>
</template>

<script setup>
import { SunIcon, MoonIcon, SearchIcon, LogoutIcon, MenuIcon, XIcon, ArrowsExpandIcon } from '@heroicons/vue/outline'
import { onMounted, ref, computed } from 'vue'
import { useLoggedUserStore } from '@/stores/loggedUser'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'

const loggedUserStore = useLoggedUserStore()

let formData = ref({
  username: '',
  name: '',
  client: '',
})

const submitForm = async () => {
  const state = useStorage('app-store', { token: '' })
  try {
    const response = await loggedUserStore.updateMe(formData.value.username, formData.value)
    successToast({ text: response.data.detail })
    router.replace({ name: 'Settings' })
  } catch (err) {
    console.log(err)
    if (err.response.data.client.non_field_errors) {
      errorToast({ text: err.response.data.client.non_field_errors.join(', ') })
      return false
    } else if (err.data.message) {
      errorToast({ text: err.message })
    }
  }
}

onMounted(async () => {
  const response = await loggedUserStore.fetchMe()
  // const {client, ...rest} = loggedUserStore.item;
  // formData.value = {...rest, client: [client.client_name]}

  let { city, ...clientWithoutCity } = loggedUserStore.item.client
  formData.value = { ...loggedUserStore.item, client: clientWithoutCity }
})
</script>
