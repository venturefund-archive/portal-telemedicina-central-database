<template>
  <nav
    aria-label="secondary"
    :class="[
      'sticky top-0 z-10 flex items-center justify-between bg-white px-5 py-4 shadow-md transition-transform duration-500',
      {
        '-translate-y-full': scrolling.down,
        'translate-y-0': scrolling.up,
      },
    ]"
  >
    <div class="flex grow items-center pr-5">
      <form @submit.prevent="search" class="!w-full sm:w-96 ">
        <InputIconWrapper>
          <template #icon>
            <SearchIcon aria-hidden="true" class="h-5 w-5" />
          </template>
          <AutoComplete v-model="queryText" :suggestions="filteredResults" />
        </InputIconWrapper>
      </form>
    </div>

    <div class="flex items-center gap-2">
      <div class="px-10">
        <LanguageSwitcher />
      </div>
      <!-- Dropdwon -->
      <Dropdown align="right" width="48">
        <template #trigger>
          <button
            class="flex rounded-md border border-transparent text-sm transition focus:outline-none focus:ring focus:ring-green-500 focus:ring-offset-0 focus:ring-offset-white"
          >
            <div class="flex flex-col items-end justify-center">
              <p class="font-bold">{{ loggedUserStore.item.username }}</p>
              <p class="text-sm text-gray-500 hidden">Nurse</p>
            </div>
            <img class="mx-5 h-12 w-12 rounded-md object-cover" :src="userAvatar" alt="User Name" />
          </button>
        </template>
        <template #content>
          <DropdownLink to="/settings" @click="settings" class="flex justify-around group" >
            <CogIcon class="group-hover:animate-spin w-6 h-6" />
            <span class="text-base">Configurações</span>
          </DropdownLink>
        </template>
      </Dropdown>
      <div>
        <div
          class="border-r-1 inline-flex items-center justify-center gap-2 border border-l-0 border-gray-100 border-b-transparent border-t-transparent px-4 py-5"
        ></div>
      </div>
      <Button
        iconOnly
        variant="third"
        @click="toggleFullScreen"
        v-slot="{ iconSizeClasses }"
        class="hidden md:inline-flex transition-transform duration-500 duration-500 ease-in-out hover:scale-110"
        srText="Toggle fullscreen mode"
      >
        <ArrowsExpandIcon v-show="!isFullscreen" aria-hidden="true" :class="iconSizeClasses" />
        <ArrowsInnerIcon v-show="isFullscreen" aria-hidden="true" :class="iconSizeClasses" />
      </Button>
      <Button
        iconOnly
        variant="third"
        @click="logout"
        v-slot="{ iconSizeClasses }"
        class="hidden md:inline-flex"
        srText="Configurações"
      >
        <LogoutIcon v-show="!isFullscreen" aria-hidden="true" :class="iconSizeClasses" class="text-blue-500" />
        <LogoutIcon @click="logout" v-show="isFullscreen" aria-hidden="true" :class="iconSizeClasses" />
      </Button>
    </div>
  </nav>

  <!-- Mobile bottom bar -->
  <div
    class="block sm:hidden"
    :class="[
      'dark:bg-dark-eval-1 fixed inset-x-0 bottom-0 z-10 flex items-center justify-between bg-blue-500 px-4 py-4 transition-transform duration-500 sm:px-6 md:hidden',
      {
        'translate-y-full': scrolling.down,
        'translate-y-0': scrolling.up,
      },
    ]"
  >
    <router-link to="/">
      <Logo class="h-10" />
      <span class="sr-only">UNICEF</span>
    </router-link>
    <SidebarContent />

    <Button
      iconOnly
      variant="secondary"
      v-if="!sidebarState.isOpen"
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
import { CogIcon, SearchIcon, LogoutIcon, MenuIcon, XIcon, ArrowsExpandIcon } from '@heroicons/vue/outline'
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

const items = ref([])
const queryText = ref('')

const router = useRouter()
const { isFullscreen, toggle: toggleFullScreen } = useFullscreen()

const logout = async () => {
  const state = useStorage('app-store', { token: '' })
  state.value.token = null
  successToast({ text: 'Você saiu com sucesso!' })
  router.replace({ name: 'Login' })
}

const filteredResults = computed(() => {
  if (queryText.value === '') {
    return []
  }

  let matches = 0

  return patientsStore.items.filter((patient) => {
    if (
      (patient.name.toLowerCase().includes(queryText.value.toLowerCase()) ||
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
})

onUnmounted(() => {
  document.removeEventListener('scroll', handleScroll)
})
</script>
