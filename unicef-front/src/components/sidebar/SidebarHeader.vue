<template>
  <div class="flex flex-shrink-0 items-center justify-between px-3">
    <router-link :to="{ name: 'Dashboard' }" class="inline-flex items-center gap-2">
      <span class="sr-only">Unicef</span>
      <LogoFull class="w-36" v-if="sidebarState.isOpen || sidebarState.isHovered" aria-hidden="true" />
      <Logo v-else aria-hidden="true" class="h-auto w-10" />
    </router-link>

    <Button
      iconOnly
      variant="secondary"
      v-slot="{ iconSizeClasses }"
      v-show="sidebarState.isOpen || sidebarState.isHovered"
      @click="sidebarState.isOpen = !sidebarState.isOpen"
      :srText="sidebarState.isOpen ? 'Close sidebar' : 'Open sidebar'"
    >
      <MenuFoldLineLeftIcon
        aria-hidden="true"
        v-show="sidebarState.isOpen"
        :class="['hidden lg:block', iconSizeClasses]"
      />

      <MenuFoldLineRightIcon
        aria-hidden="true"
        v-show="!sidebarState.isOpen"
        :class="['hidden lg:block', iconSizeClasses]"
      />

      <XIcon aria-hidden="true" :class="['lg:hidden', iconSizeClasses]" />
    </Button>
  </div>
</template>

<script setup>
import { MenuFoldLineLeftIcon, MenuFoldLineRightIcon } from '@/components/icons/outline'
import { XIcon } from '@heroicons/vue/outline'
import { sidebarState } from '@/composables'
</script>
