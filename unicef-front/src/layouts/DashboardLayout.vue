<template>
  <div class="min-h-screen bg-[#F8F9FB] text-gray-900">
    <div class="hidden sm:block">
      <Sidebar />
    </div>

    <div
      style="transition-property: margin; transition-duration: 150ms"
      :class="[
        'flex min-h-screen flex-col',
        {
          'lg:ml-28': sidebarState.isOpen,
          'md:ml-16': !sidebarState.isOpen,
        },
      ]"
    >
      <Navbar />

      <router-view v-slot="{ Component, route }">
        <template v-if="Component">
          <Transition mode="out-in">
            <div>
              <KeepAlive>
                <Suspense>
                  <component :is="Component" :key="route.name" />

                  <template #fallback> Loading... </template>
                </Suspense>
              </KeepAlive>
            </div>
          </Transition>
        </template>
      </router-view>

      <PageFooter />
    </div>
  </div>
</template>

<script setup>
import { sidebarState } from '@/composables'
import { onMounted, ref, computed, reactive } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'
import { usePatientsStore } from '@/stores/patients'
import { useVaccinesStore } from '@/stores/vaccines'
import { useLoggedUserStore } from '@/stores/loggedUser'
import { useDosesStore } from '@/stores/doses'
const loggedUserStore = useLoggedUserStore()
const patientsStore = usePatientsStore()
const vaccinesStore = useVaccinesStore()
const router = useRouter()
const dosesStore = useDosesStore()

const isLoading = ref(true)

onMounted(async () => {
  isLoading.value = true
  await patientsStore.fetchPatients()
  await patientsStore.fetchPatientsRecursive()
  isLoading.value = false
})
</script>
<style scoped>
.dot1 {
  animation: dot1 2s infinite;
}

.dot2 {
  animation: dot2 2s infinite;
}

.dot3 {
  animation: dot3 2s infinite;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
@keyframes dot1 {
  0%,
  20%,
  100% {
    opacity: 0;
  }
  25%,
  90% {
    opacity: 1;
  }
}

@keyframes dot2 {
  0%,
  50%,
  100% {
    opacity: 0;
  }
  55%,
  90% {
    opacity: 1;
  }
}

@keyframes dot3 {
  0%,
  80%,
  100% {
    opacity: 0;
  }
  85%,
  90% {
    opacity: 1;
  }
}
</style>
