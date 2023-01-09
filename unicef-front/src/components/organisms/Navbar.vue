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
    <div class="flex items-center pr-5 grow">
      <form @submit.prevent="search" class="w-full lg:w-1/2">
        <label for="default-search" class="sr-only mb-2 text-sm font-medium text-gray-900">Procurar</label>
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
          <AutoComplete v-model="queryText" :suggestions="filteredResults" />
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
              <p class="font-bold" v-if="loggedUserStore.item">{{ loggedUserStore.item.username }}</p>
              <p class="text-sm text-gray-500">Enfermeiro</p>
            </div>
            <img class="mx-5 h-12 w-12 rounded-md object-cover" :src="userAvatar" alt="User Name" />
          </button>
        </template>
        <template #content>
          <DropdownLink to="#" @click="logout">Sair</DropdownLink>
        </template>
      </Dropdown>
      <Button
        iconOnly
        variant="secondary"
        @click="toggleFullScreen"
        v-slot="{ iconSizeClasses }"
        class="hidden md:inline-flex"
        srText="Toggle fullscreen mode"
      >
        <ArrowsExpandIcon v-show="!isFullscreen" aria-hidden="true" :class="iconSizeClasses" />
        <ArrowsInnerIcon v-show="isFullscreen" aria-hidden="true" :class="iconSizeClasses" />
      </Button>
      <Button
        iconOnly
        variant="secondary"
        @click="logout"
        v-slot="{ iconSizeClasses }"
        class="hidden md:inline-flex"
        srText="Sair"
      >
        <LogoutIcon v-show="!isFullscreen" aria-hidden="true" :class="iconSizeClasses" />
        <LogoutIcon v-show="isFullscreen" aria-hidden="true" :class="iconSizeClasses" />
      </Button>
    </div>
  </nav>

  <!-- Mobile bottom bar -->
  <div
    :class="[
      'dark:bg-dark-eval-1 fixed z-10 inset-x-0 bottom-0 flex items-center justify-between bg-white px-4 py-4 transition-transform duration-500 sm:px-6 md:hidden',
      {
        'translate-y-full': scrolling.down,
        'translate-y-0': scrolling.up,
      },
    ]"
  >
    <router-link to="/">
      <Logo class="h-10 w-10" />
      <span class="sr-only">UNICEF</span>
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
import { onMounted, onUnmounted, reactive } from 'vue'
import { useFullscreen } from '@vueuse/core'
import { SunIcon, MoonIcon, SearchIcon, LogoutIcon, MenuIcon, XIcon, ArrowsExpandIcon } from '@heroicons/vue/outline'
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
import { ref, watch, computed } from 'vue'
import { usePatientsStore } from '@/stores/patients'
import { useLoggedUserStore } from '@/stores/loggedUser'
const loggedUserStore = useLoggedUserStore()
const patientsStore = usePatientsStore()

const queryText = ref('')

const router = useRouter()
const { isFullscreen, toggle: toggleFullScreen } = useFullscreen()

const logout = async () => {
  const state = useStorage('app-store', { token: '' })
  try {
    const response = await axios.post(import.meta.env.VITE_API_URL + '/api/dj-rest-auth/logout/')
    state.value = null
    successToast({ text: 'Você saiu com sucesso!' })
    router.replace({ name: 'Login' })
  } catch (err) {
    errorToast({ text: err.message })
  }
}

const filteredResults = computed(() => {
  if (queryText.value === '') {
    return []
  }

  let matches = 0

  return patientsStore.items.filter((patient) => {
    if (
      (patient.name.join().toLowerCase().includes(queryText.value.toLowerCase()) ||
        patient.id.toLowerCase().includes(queryText.value.toLowerCase())) &&
      matches < 10
    ) {
      matches++
      return patient
    }
  })
})

onMounted(async () => {
  document.addEventListener('scroll', handleScroll)
  await loggedUserStore.fetchMe()
  await patientsStore.searchPatients()
})

onUnmounted(() => {
  document.removeEventListener('scroll', handleScroll)
})
</script>
