<template>
  <nav
    aria-label="secondary"
    :class="[
      'dark:bg-dark-eval-1 sticky top-0 z-10 flex items-center justify-between bg-white px-6 py-4 transition-transform duration-500',
      {
        '-translate-y-full': scrolling.down,
        'translate-y-0': scrolling.up,
      },
    ]"
  >
    <div class="flex items-center gap-2">
      <form>
        <label for="default-search" class="sr-only mb-2 text-sm font-medium text-gray-900">Search</label>
        <div class="relative">
          <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <svg
              class="h-5 w-5 text-gray-500 dark:text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              ></path>
            </svg>
          </div>
          <input
            type="search"
            class="block w-full rounded-lg border border-transparent bg-gray-50 p-4 pl-10 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500 md:w-96"
            placeholder="Search for appointments, patients etc"
            required
          />
        </div>
      </form>
    </div>

    <div class="flex items-center gap-2">
      <!-- Dropdwon -->
      <Dropdown align="right" width="48">
        <template #trigger>
          <button
            class="dark:focus:ring-offset-dark-eval-1 flex rounded-md border-2 border-transparent text-sm transition focus:outline-none focus:ring focus:ring-blue-500 focus:ring-offset-1 focus:ring-offset-white"
          >
            <div class="flex flex-col items-end justify-center">
              <p class="font-bold">Cody Simmmons</p>
              <p class="text-sm text-gray-500">Nurse</p>
            </div>
            <img class="mx-5 h-12 w-12 rounded-md object-cover" :src="userAvatar" alt="User Name" />
          </button>
        </template>
        <template #content>
          <DropdownLink to="#" @click="logout">Log Out</DropdownLink>
        </template>
      </Dropdown>
      <Button
        iconOnly
        variant="secondary"
        @click="toggleFullScreen"
        v-slot="{ iconSizeClasses }"
        class="hidden md:inline-flex"
        srText="Toggle dark mode"
      >
        <ArrowsExpandIcon v-show="!isFullscreen" aria-hidden="true" :class="iconSizeClasses" />
        <ArrowsInnerIcon v-show="isFullscreen" aria-hidden="true" :class="iconSizeClasses" />
      </Button>
    </div>
  </nav>

  <!-- Mobile bottom bar -->
  <div
    :class="[
      'dark:bg-dark-eval-1 fixed inset-x-0 bottom-0 flex items-center justify-between bg-white px-4 py-4 transition-transform duration-500 sm:px-6 md:hidden',
      {
        'translate-y-full': scrolling.down,
        'translate-y-0': scrolling.up,
      },
    ]"
  >
    <Button iconOnly variant="secondary" v-slot="{ iconSizeClasses }" srText="Search">
      <SearchIcon aria-hidden="true" :class="iconSizeClasses" />
    </Button>

    <router-link to="/">
      <Logo class="h-10 w-10" />
      <span class="sr-only">unicef</span>
    </router-link>

    <Button
      iconOnly
      variant="secondary"
      @click="sidebarState.isOpen = !sidebarState.isOpen"
      v-slot="{ iconSizeClasses }"
      class="md:hidden"
      srText="Search"
    >
      <MenuIcon v-show="!sidebarState.isOpen" aria-hidden="true" :class="iconSizeClasses" />
      <XIcon v-show="sidebarState.isOpen" aria-hidden="true" :class="iconSizeClasses" />
    </Button>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useFullscreen } from '@vueuse/core'
import { SunIcon, MoonIcon, SearchIcon, MenuIcon, XIcon, ArrowsExpandIcon } from '@heroicons/vue/outline'
import {
  handleScroll,
  isDark,
  scrolling,
  // toggleDarkMode,
  sidebarState,
} from '@/composables'
import { ArrowsInnerIcon } from '@/components/icons/outline'
import userAvatar from '@/assets/images/avatar.jpg'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'

const router = useRouter()
const { isFullscreen, toggle: toggleFullScreen } = useFullscreen()

const logout = async () => {
  const state = useStorage('app-store', { token: '' })
  try {
    const response = await axios.post(import.meta.env.VITE_AUTH_API_URL + 'logout/')
    state.value = null
    successToast({ text: "You've successfully logged out." })
    router.replace({ name: 'Login' })
  } catch (err) {
    errorToast({ text: err.message })
  }
}

const me = async () => {
  const state = useStorage('app-store', { token: '' })
  try {
    const response = await axios.get(import.meta.env.VITE_AUTH_API_URL + 'user/', {
      headers: {
        'Content-type': 'application/json',
        Authorization: `Bearer ${state.value.token}`,
      },
    })
  } catch (err) {
    errorToast({ text: err.message })
  }
}

onMounted(() => {
  document.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  document.removeEventListener('scroll', handleScroll)
})
</script>
