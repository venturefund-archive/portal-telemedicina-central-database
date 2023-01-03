<template>
  <div>
    <h2 class="font-bold">Acesso restrito!</h2>
    <p class="mb-5 max-w-xl text-sm text-gray-500">
      Ambiente de trabalho reservado para acesso restrito de profissionais de saúde.
    </p>
  </div>
  <form @submit.prevent="login">
    <div class="grid gap-6">
      <!-- User input -->
      <div class="mb-1 space-y-2">
        <InputIconWrapper>
          <template #icon>
            <UserIcon aria-hidden="true" class="h-5 w-5" />
          </template>
          <Input
            withIcon
            id="username"
            type="text"
            class="block w-full"
            placeholder="Username"
            v-model="loginForm.username"
            autofocus
            autocomplete="username"
          />
        </InputIconWrapper>
      </div>

      <!-- Password input -->
      <div class="mb-2 mt-5">
        <InputIconWrapper>
          <template #icon>
            <LockClosedIcon aria-hidden="true" class="h-5 w-5" />
          </template>
          <Input
            withIcon
            id="password"
            type="password"
            class="block w-full"
            placeholder="Password"
            v-model="loginForm.password"
            autocomplete="current-password"
          />
        </InputIconWrapper>
      </div>

      <!-- Remember me -->
      <div class="flex items-center justify-between">
        <label class="flex items-center">
          <Checkbox name="remember" v-model:checked="loginForm.remember" />
          <span class="ml-2 text-sm text-gray-600">Lembrar-me</span>
        </label>

        <router-link :to="{ name: 'ForgotPassword' }" class="text-sm text-blue-500 hover:underline"
          >Esqueceu a senha?</router-link
        >
      </div>

      <!-- Login button -->
      <div>
        <Button
          type="submit"
          class="w-full justify-center gap-2"
          :disabled="loginForm.processing"
          v-slot="{ iconSizeClasses }"
        >
          <LoginIcon aria-hidden="true" :class="iconSizeClasses" />
          <span>Entrar</span>
        </Button>
      </div>

      <!-- Register link -->
      <p class="text-sm text-gray-600 dark:text-gray-400">
        Ainda não tem uma conta?
        <router-link :to="{ name: 'Register' }" class="text-blue-500 hover:underline">Cadastrar</router-link>
      </p>
    </div>
  </form>
</template>

<script setup>
import { onMounted, reactive } from 'vue'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { MailIcon, LockClosedIcon, LoginIcon, UserIcon } from '@heroicons/vue/outline'
// import { useHttp } from '@/composables
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'

const router = useRouter()

const loginForm = reactive({
  username: '',
  password: '',
  remember: false,
  processing: false,
})

const login = async () => {
  const state = useStorage('app-store', { token: '' })
  try {
    const response = await axios.post(import.meta.env.VITE_API_URL + '/api/dj-rest-auth/login/', loginForm)

    if (response.data.non_field_errors) {
      errorToast({ text: err.message })
      return false
    }
    state.value.token = response.data.key
    successToast({ text: 'Você se conectou com sucesso.' })
    router.replace({ name: 'Dashboard' })
  } catch (err) {
    if (err.response.data.non_field_errors) {
      errorToast({ text: err.response.data.non_field_errors.join(', ') })
      return false
    }
    errorToast({ text: err.message })
  }
}
</script>
