<template>
  <form @submit.prevent="submit">
    <div class="grid gap-4">

      <div class="space-y-2">
        <Label for="password" value="New password" />
        <InputIconWrapper>
          <template #icon>
            <LockClosedIcon aria-hidden="true" class="h-5 w-5" />
          </template>
          <Input
            withIcon
            id="password"
            type="password"
            placeholder="New password"
            class="block w-full"
            v-model="resetPasswordForm.password"
            required
            autocomplete="new-password"
          />
        </InputIconWrapper>
      </div>

      <div class="space-y-2">
        <Label for="password_confirmation" value="Confirm Password" />
        <InputIconWrapper>
          <template #icon>
            <LockClosedIcon aria-hidden="true" class="h-5 w-5" />
          </template>
          <Input
            withIcon
            id="password_confirmation"
            type="password"
            placeholder="Confirm Password"
            class="block w-full"
            v-model="resetPasswordForm.password_confirmation"
            required
            autocomplete="new-password"
          />
        </InputIconWrapper>
      </div>

      <div>
        <Button type="submit" class="w-full justify-center" :disabled="resetPasswordForm.processing"
          >Reset Password</Button
        >
      </div>
    </div>
  </form>
</template>

<script setup>
import axios from 'axios'
import { reactive } from 'vue'
import { MailIcon, LockClosedIcon } from '@heroicons/vue/outline'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'

const props = defineProps({
  uid: String,
  token: String,
})

const resetPasswordForm = reactive({
  password: '',
  password_confirmation: '',
  processing: false,
})

const submit = async () => {
  const state = useStorage('app-store', { token: '' })
  try {
    const response = await axios.post(
      import.meta.env.VITE_AUTH_API_URL2 + `password/reset/confirm/${props.uid}/${props.token}/`, {
        new_password1: resetPasswordForm.password,
        new_password2: resetPasswordForm.password_confirmation,
        uid: props.uid,
        token: props.token,
      }
    )
    successToast({ text: response.detail })
    router.replace({ name: 'Dashboard' })
  } catch (err) {
    if (err.response.data.token) {
      errorToast({ text: err.response.data.token.join(', ') })
      return false
    }
    if (err.response.data.new_password1) {
      errorToast({ text: err.response.data.new_password1.join(', ') })
      return false
    }
    if (err.response.data.new_password2) {
      errorToast({ text: err.response.data.new_password2.join(', ') })
      return false
    }
    errorToast({ text: err.message })
  }
}
</script>
