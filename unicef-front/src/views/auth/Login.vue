<template>
  <div>
    <h2 class="font-bold">Restricted access!</h2>
    <p class="mb-5 max-w-xl text-sm text-gray-500">
      Work environment reserved for restricted access of health professionals.
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
          <span class="ml-2 text-sm text-gray-600">Remember me</span>
        </label>

        <router-link :to="{ name: 'ForgotPassword' }" class="text-sm text-blue-500 hover:underline"
          >Forgot your password?</router-link
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
          <span>Log in</span>
        </Button>
      </div>

      <!-- Register link -->
      <p class="text-sm text-gray-600 dark:text-gray-400">
        Don't have an account?
        <router-link :to="{ name: 'Register' }" class="text-blue-500 hover:underline">Register</router-link>
      </p>
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { MailIcon, LockClosedIcon, LoginIcon, UserIcon } from '@heroicons/vue/outline'
// import { useHttp } from '@/composables
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
// import { errorToast } from '@/toast'

const router = useRouter()

const loginForm = reactive({
  username: '',
  password: '',
  remember: false,
  processing: false,
})

const login = async () => {
  const state = useStorage('app-store', { token: '' })
  // console.log('token guardado: ' + state.value.token)
  try {
    const response = await axios.post('http://localhost:8000/dj-rest-auth/login/', loginForm)

    if (!response.data.non_field_errors || 0 === response.data.non_field_errors.length) {
      state.value.token = response.data.key
      router.replace({ name: 'Dashboard' })
    }
  } catch (err) {
    console.log(err.message)
    // errorToast(err.message)
  }
}
</script>
