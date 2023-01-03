<template>
  <div class="min-h-screen bg-gray-100 text-gray-900">
    <Sidebar />

    <div
      style="transition-property: margin; transition-duration: 150ms"
      :class="[
        'flex min-h-screen flex-col',
        {
          'lg:ml-64': sidebarState.isOpen,
          'md:ml-16': !sidebarState.isOpen,
        },
      ]"
    >
      <Navbar />

      <router-view></router-view>

      <PageFooter />
    </div>
  </div>
</template>

<script setup>
import { sidebarState } from '@/composables'
</script>
