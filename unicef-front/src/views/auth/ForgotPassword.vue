<template>
  <div class="mb-4 text-sm text-gray-600 dark:text-gray-400">
    {{ $t('auth.forgot-your-password-text') }}
  </div>

  <form @submit.prevent="submit">
    <div class="grid gap-6">
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
          class="w-full justify-center gap-2 rounded-full"
          :disabled="forgotPasswordForm.processing"
          v-slot="{ iconSizeClasses }"
        >
          <PaperAirplaneIcon aria-hidden="true" :class="iconSizeClasses" />
          <span>{{ $t('auth.e-mail-password-reset-link') }}</span>
        </Button>
      </div>
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { MailIcon, LockClosedIcon, LoginIcon, UserIcon, PaperAirplaneIcon } from '@heroicons/vue/outline'
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
    const response = await axios.post(import.meta.env.VITE_API_URL + '/api/dj-rest-auth/password/reset/', forgotPasswordForm)
    successToast({ text: response.data.detail })
    router.replace({ name: 'Login' })
  } catch (err) {
    errorToast({ text: err.message })
  }
}
</script>
