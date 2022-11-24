<template>
  <div class="mb-4 text-sm text-gray-600 dark:text-gray-400">
    Forgot your password? No problem. Just let us know your email address and we will email you a password reset link
    that will allow you to choose a new one.
  </div>

  <form @submit.prevent="submit">
    <div class="grid gap-6">
      <div class="space-y-2">
        <Label for="email" value="Email" />
        <InputIconWrapper>
          <template #icon>
            <MailIcon aria-hidden="true" class="h-5 w-5" />
          </template>
          <Input
            withIcon
            id="email"
            type="email"
            class="block w-full"
            placeholder="Email"
            v-model="forgotPasswordForm.email"
            required
            autofocus
            autocomplete="username"
          />
        </InputIconWrapper>
      </div>

      <div>
        <Button
          type="submit"
          class="w-full justify-center gap-2"
          :disabled="forgotPasswordForm.processing"
          v-slot="{ iconSizeClasses }"
        >
          <PaperAirplaneIcon aria-hidden="true" :class="iconSizeClasses" />
          <span>Email Password Reset Link</span>
        </Button>
      </div>
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { MailIcon, LockClosedIcon, LoginIcon, UserIcon } from '@heroicons/vue/outline'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'

const router = useRouter()

const forgotPasswordForm = reactive({
  email: '',
  processing: false,
})

const submit = async () => {
  try {
    const response = await axios.post(import.meta.env.VITE_AUTH_API_URL + 'password/reset/', forgotPasswordForm)
    successToast({ text: response.data.detail })
    router.replace({ name: 'Login' })
  } catch (err) {
    errorToast({ text: err.message })
  }
}
</script>
