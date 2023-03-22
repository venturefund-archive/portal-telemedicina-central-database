<template>
  <div class="mb-4 text-sm text-gray-600 dark:text-gray-400">
    {{ $t('auth.password-change-confirm-text') }}
  </div>

  <form @submit.prevent="submit">
    <div class="grid gap-4">
      <div class="space-y-2">
        <Label for="password" :value="$t('auth.password')" />
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
            v-model="confirmPasswordForm.password"
            required
            autocomplete="current-password"
            autofocus
          />
        </InputIconWrapper>
      </div>

      <div>
        <Button type="submit" class="w-full justify-center" :disabled="confirmPasswordForm.processing">Confirm</Button>
      </div>
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { LockClosedIcon } from '@heroicons/vue/outline'

const confirmPasswordForm = reactive({
  password: '',
  processing: false,
})

const submit = () => {
  //
}
</script>
