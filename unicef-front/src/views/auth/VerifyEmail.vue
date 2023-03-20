<template>
  <div class="mb-4 text-sm text-gray-600 dark:text-gray-400">
    {{ $t('auth.thanks-text') }}  </div>

  <div class="mb-4 text-sm font-medium text-green-600" v-if="verificationLinkSent">
    {{ $t('auth.request-text') }}
  </div>

  <form @submit.prevent="submit">
    <div class="mt-4 flex items-center justify-between">
      <!-- <Button type="submit" :class="{ 'opacity-25': verifyEmailForm.processing }" :disabled="verifyEmailForm.processing"
        >Resend Verification Email</Button
      > -->

      <router-link
        :to="{ name: 'Login' }"
        method="post"
        as="button"
        class="text-sm text-blue-600 hover:underline dark:text-blue-400"
        >{{ $t('auth.back') }}</router-link
      >
    </div>
  </form>
</template>

<script setup>
import { reactive, ref } from 'vue'

const props = defineProps({
  status: String,
})

const verifyEmailForm = reactive({
  processing: false,
})

const verificationLinkSent = ref(false)

const submit = () => {
  verificationLinkSent.value = true
}
</script>
