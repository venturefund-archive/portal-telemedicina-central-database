<template>
  <PageWrapper>
      <div class="py-4 rounded rounded-t-xl">
        <h2 class="font-semibold text-2xl text-gray-700 mt-10">Configurações</h2>
      </div>
    <div class="bg-white  px-16 py-16 h-full rounded-xl border border-gray-100 shadow">
        <h3 class="text-xl font-semibold text-gray-700">Editar dados da conta</h3>
        <hr class="text-gray-200 my-4">
        <form @submit.prevent="submitForm" class="flex w-full flex-col  sm:w-96">
        <div class="w-full flex flex-col p-4">
          <input v-model="formData.username" type="text" id="username" class="p-2 border border-gray-300 rounded" placeholder="username" />
          <input v-model="formData.name" type="text" id="name" class="p-2 border border-gray-300 rounded" placeholder="Nome completo" required />
        </div>

        <div class="w-full p-4 flex justify-end">
          <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">Salvar</button>
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
});

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
    }else if (err.data.message) {
        errorToast({ text: err.message })
    }
  }
}

onMounted(async () => {
    const response = await loggedUserStore.fetchMe()
    // const {client, ...rest} = loggedUserStore.item;
    // formData.value = {...rest, client: [client.client_name]}

    let { city, ...clientWithoutCity } = loggedUserStore.item.client;
    formData.value = { ...loggedUserStore.item, client: clientWithoutCity };

})
</script>
