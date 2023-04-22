<template>
  <div>
    <h2 class="font-bold">{{ $t('auth.restricted-access') }}</h2>
    <p class="mb-5 max-w-xl text-sm text-gray-500">
      {{ $t('auth.work-environment-reserved-for-restricted-access-of-health-professionals') }}
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
            :placeholder="$t('auth.username')"
            v-model="loginForm.username"
            autofocus
            autocomplete="username"
            autocapitalize="none"
            autocorrect="off"
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
            :placeholder="$t('auth.password')"
            v-model="loginForm.password"
            autocomplete="current-password"
          />
        </InputIconWrapper>
      </div>

      <!-- Remember me -->
      <div class="flex items-center justify-between">
        <label class="flex items-center">
          <Checkbox name="remember" v-model:checked="loginForm.remember" />
          <span class="ml-2 text-sm text-gray-600">{{ $t('auth.remember-me') }}</span>
        </label>

        <router-link :to="{ name: 'ForgotPassword' }" class="text-sm text-blue-500 hover:underline"
          >{{ $t('auth.forgot-password') }}</router-link
        >
      </div>

      <!-- Login button -->
      <div>
        <Button
          type="submit"
          class="w-full justify-center gap-2 rounded-full"
          :disabled="loginForm.processing"
          v-slot="{ iconSizeClasses }"
        >
          <LoginIcon aria-hidden="true" :class="iconSizeClasses" />
          <span>{{ $t('auth.enter') }}</span>
        </Button>
      </div>

      <!-- Register link -->
      <p class="text-sm text-gray-600 dark:text-gray-400">
        {{ $t('auth.not-have-an-account-yet') }}
        <router-link :to="{ name: 'Register' }" class="text-blue-500 hover:underline">{{ $t('auth.register') }}</router-link>
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
import { useI18n } from "vue3-i18n"
const { t, locale } = useI18n()

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
    successToast({ text: t('auth.you-connected-successfully') })
    router.replace({ name: 'Dashboard' })
  } catch (err) {
    if (err.response.data.non_field_errors) {
      errorToast({ text: t('auth.user-under-approval-phase-or-user-under-analysis') })
      return false
    }
    if (err.response.data.username) {
      errorToast({ text: 'username: ' + err.response.data.username.join(', ') })
      return false
    }
  }
}
</script>
