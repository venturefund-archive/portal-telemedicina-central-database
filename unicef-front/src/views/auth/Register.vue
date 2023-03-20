<template>
  <form @submit.prevent="register">
    <div class="grid gap-6">
      <!-- Name input -->
      <div class="space-y-2">
        <Label for="username" value="Username" />
        <InputIconWrapper>
          <template #icon>
            <UserIcon aria-hidden="true" class="h-5 w-5" />
          </template>
          <Input
            withIcon
            id="username"
            type="text"
            :placeholder="$t('auth.username')"
            class="block w-full"
            v-model="registerForm.username"
            required
            autofocus
            autocomplete="username"
            autocapitalize="none"
            autocorrect="off"
          />
        </InputIconWrapper>
      </div>

      <!-- Email input -->
      <div class="space-y-2">
        <Label for="email" :value="$t('auth.e-mail')" />
        <InputIconWrapper>
          <template #icon>
            <MailIcon aria-hidden="true" class="h-5 w-5" />
          </template>
          <Input
            withIcon
            id="email"
            type="email"
            class="block w-full"
            :placeholder="$t('auth.e-mail')"
            v-model="registerForm.email"
            required
          />
        </InputIconWrapper>
      </div>

      <!-- Password input -->
      <div class="space-y-2">
        <Label for="password1" :value="$t('auth.password')" />
        <InputIconWrapper>
          <template #icon>
            <LockClosedIcon aria-hidden="true" class="h-5 w-5" />
          </template>
          <Input
            withIcon
            id="password1"
            type="password"
            class="block w-full"
            :placeholder="$t('auth.password')"
            v-model="registerForm.password1"
            required
            autocomplete="new-password"
          />
        </InputIconWrapper>
      </div>

      <!-- Password confirmation input -->
      <div class="space-y-2">
        <Label for="password2" :value="$t('auth.confirm-password')" />
        <InputIconWrapper>
          <template #icon>
            <LockClosedIcon aria-hidden="true" class="h-5 w-5" />
          </template>
          <Input
            withIcon
            id="password2"
            type="password"
            class="block w-full"
            :placeholder="$t('auth.confirm-password')"
            v-model="registerForm.password2"
            required
            autocomplete="new-password"
          />
        </InputIconWrapper>
      </div>

      <!-- Terms -->
      <div>
        <Label for="terms">
          <div class="flex items-center">
            <Checkbox name="terms" id="terms" v-model:checked="registerForm.terms" />

            <div class="ml-2">
              {{ $t('auth.terms1') }}
              <a target="_blank" href="#" class="text-sm text-blue-600 underline hover:text-blue-900"
                >{{ $t('auth.terms2') }}</a
              >
              {{ $t('auth.terms3') }}
              <a target="_blank" href="#" class="text-sm text-blue-600 underline hover:text-blue-900"
                >{{ $t('auth.terms4') }}</a
              >
            </div>
          </div>
        </Label>
      </div>

      <!-- Register button -->
      <div>
        <Button
          type="submit"
          class="w-full justify-center gap-2"
          :disabled="registerForm.processing"
          v-slot="{ iconSizeClasses }"
        >
          <UserAddIcon aria-hidden="true" :class="iconSizeClasses" />
          <span>{{ $t('auth.register') }}</span>
        </Button>
      </div>

      <!-- Login link -->
      <p class="text-sm text-gray-600 dark:text-gray-400">
        {{ $t('auth.already-have-an-account') }}
        <router-link :to="{ name: 'Login' }" class="text-blue-500 hover:underline">{{ $t('auth.enter') }}</router-link>
      </p>
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import { UserAddIcon } from '@heroicons/vue/outline'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { MailIcon, LockClosedIcon, LoginIcon, UserIcon } from '@heroicons/vue/outline'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'

const router = useRouter()

const registerForm = reactive({
  username: '',
  email: '',
  password1: '',
  password2: '',
  terms: false,
  processing: false,
})

const register = async () => {
  const state = useStorage('app-store', { token: '' })
  try {
    const response = await axios.post(import.meta.env.VITE_API_URL + '/api/dj-rest-auth/registration/', registerForm)
    successToast({ text: response.data.detail })
    router.replace({ name: 'VerifyEmail' })
  } catch (err) {
    if (err.response.data.username) {
      errorToast({ text: 'Username: ' + err.response.data.username.join(', ') })
      return false
    }
    if (err.response.data.email) {
      errorToast({ text: 'Email: ' + err.response.data.email.join(', ') })
      return false
    }
    if (err.response.data.password1) {
      errorToast({ text: 'Password1: ' + err.response.data.password1.join(', ') })
      return false
    }
    if (err.response.data.password2) {
      errorToast({ text: 'Password2: ' + err.response.data.password2.join(', ') })
      return false
    }
    if (err.response.data.non_field_errors) {
      errorToast({ text: err.response.data.non_field_errors.join(', ') })
      return false
    }

    errorToast({ text: err.message })
  }
}
</script>
