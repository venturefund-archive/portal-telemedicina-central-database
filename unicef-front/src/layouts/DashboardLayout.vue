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
</script>
<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
