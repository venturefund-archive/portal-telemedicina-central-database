<template>
  <div class="min-h-screen bg-white text-gray-900">
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
        <transition name="fade" mode="out-in">
          <div :key="route.name">
            <component :is="Component"></component>
          </div>
        </transition>
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
