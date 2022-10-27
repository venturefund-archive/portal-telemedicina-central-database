<template>
  <div>
    <h2 class="font-bold">Acesso restrito!</h2>
    <p class="max-w-xl mb-5 text-gray-500 text-sm">
      Ambiente de trabalho reservado para acesso restrito dos profissionais de saúde.
    </p>
  </div>
  <form @submit.prevent="login">
    <div class="grid gap-6">
      <!-- User input -->
      <div class="space-y-2 mb-1">
        <InputIconWrapper>
          <template #icon>
            <MailIcon aria-hidden="true" class="h-5 w-5" />
          </template>
          <Input
            withIcon
            id="username"
            type="email"
            class="block w-full"
            placeholder="Username"
            v-model="loginForm.username"
            required
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
            required
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
import { MailIcon, LockClosedIcon, LoginIcon } from '@heroicons/vue/outline'

const loginForm = reactive({
  username: '',
  password: '',
  remember: false,
  processing: false,
})

const login = () => {}
</script>
