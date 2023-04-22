<template>
  <div class="flex flex-shrink-0 items-center justify-between px-3">
    <router-link to="/" class="inline-flex items-center gap-2 mx-auto">
      <span class="sr-only">Unicef</span>
      <LogoFull v-if="sidebarState.isOpen || sidebarState.isHovered" aria-hidden="true" />
      <Logo v-else aria-hidden="true" class="h-12" />
    </router-link>
  </div>
</template>

<script setup>
import { MenuFoldLineLeftIcon, MenuFoldLineRightIcon } from '@/components/icons/outline'
import { XIcon } from '@heroicons/vue/outline'
import { sidebarState } from '@/composables'
</script>
