lo<template>
  <transition
    enter-active-class="transition"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-show="sidebarState.isOpen"
      @click="sidebarState.isOpen = false"
      class="fixed inset-0 z-20 bg-black/50 lg:hidden"
    ></div>
  </transition>

  <aside
    style="transition-property: width, transform; transition-duration: 150ms"
    :class="[
      'fixed inset-y-0 z-20 flex flex-col space-y-6 bg-blue-500 py-4 shadow-lg',
      {
        'w-28 translate-x-0': sidebarState.isOpen || sidebarState.isHovered,
      },
    ]"
    @mouseenter="sidebarState.handleHover(true)"
    @mouseleave="sidebarState.handleHover(false)"
  >
    <SidebarHeader />
    <SidebarContent />
    <SidebarFooter />
  </aside>
</template>

<script setup>
import { onMounted } from 'vue'
import { sidebarState } from '@/composables'

onMounted(() => {
  window.addEventListener('resize', sidebarState.handleWindowResize)
})
</script>
