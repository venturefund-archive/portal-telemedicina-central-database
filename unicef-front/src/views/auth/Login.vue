<template>
  <div>
    <p v-for="(error,k) in errors" :key="k">{{error}}</p>
    <h2 class="font-bold">Restricted access!</h2>
    <p class="max-w-xl mb-5 text-gray-500 text-sm">
      Work environment reserved for restricted access of health professionals.
    </p>
  </div>
  <form @submit.prevent="login">
    <div class="grid gap-6">
      <!-- User input -->
      <div class="space-y-2 mb-1">
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
import { MailIcon, LockClosedIcon, LoginIcon,UserIcon } from '@heroicons/vue/outline'
// import { useHttp } from '@/composables
import axios from 'axios'
import { useRouter } from "vue-router";
import { useStorage } from '@vueuse/core'
const router = useRouter();

const errors = []
const loginForm = reactive({
  username: '',
  password: '',
  remember: false,
  processing: false,
})

const login = async () => {
  const data = {
      "name": "Login",
      "description": "Check the credentials and return the REST Token\nif the credentials are valid and authenticated.\nCalls Django Auth login method to register User ID\nin Django session framework\n\nAccept the following POST parameters: username, password\nReturn the REST Framework Token Object's key.",
      "renders": [
          "application/json",
          "text/html"
      ],
      "parses": [
          "application/json",
          "application/x-www-form-urlencoded",
          "multipart/form-data"
      ],
      "actions": {
          "POST": {
              "username": {
                  "type": "string",
                  "required": false,
                  "read_only": false,
                  "label": "Username"
              },
              "email": {
                  "type": "email",
                  "required": false,
                  "read_only": false,
                  "label": "Email"
              },
              "password": {
                  "type": "string",
                  "required": true,
                  "read_only": false,
                  "label": "Password"
              }
          }
      }
  }
  console.log('tokenantigo:')
  const state = useStorage('my-store', { token: 'hi' })
  console.log(state.value.token)
  try {
    const response = await axios.post('http://localhost:8000/accounts/login/', loginForm)
    const accessToken = response.key
    state.value.token = accessToken
    errors =  response.non_field_errors
    await router.replace({ name: "Dashboard" }) ;
  } catch (err) {
    errors.push(err)
    // if (err instanceof InvalidOtpError) {
    //   await router.push({ name: "auth.login.otp" });
    // } else {
    //   toast.error(get(err, "message"));
    //   throw err;
    // }
  }

  // console.log(loginForm.username)
  // console.log(data)e: "Dashboard" });
}
</script>
