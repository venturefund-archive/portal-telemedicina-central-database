<template>
  <PerfectScrollbar
    tagname="nav"
    aria-label="main"
    class="relative flex max-h-full flex-1 flex-row justify-around gap-4 px-3 px-8 sm:flex-col sm:justify-start sm:px-3"
  >
    <SidebarLink :title="$t('dashboard.dashboard')" :to="{ name: 'Dashboard' }" :active="isCurrentRoute('Dashboard')">
      <template #icon>
        <TemplateIcon class="h-6 w-6 flex-shrink-0" aria-hidden="true" />
      </template>
    </SidebarLink>

    <SidebarLink
      :title="$t('dashboard.patients')"
      class="capitalize"
      :to="{ name: 'PatientDetailsNobody' }"
      :active="isCurrentRoute('PatientDetails') || isCurrentRoute('PatientDetailsNobody')"
    >
      <template #icon>
        <UserGroupIcon class="h-6 w-6 flex-shrink-0" aria-hidden="true" />
      </template>
    </SidebarLink>

    <SidebarLink
      :title="$t('dashboard.map')"
      :to="{ name: 'Map' }"
      :active="isCurrentRoute('map') || isCurrentRoute('Map')"
    >
      <template #icon>
        <MapIcon class="h-6 w-6 flex-shrink-0" aria-hidden="true" />
      </template>
    </SidebarLink>
  </PerfectScrollbar>

  <Button
    iconOnly
    variant="secondary"
    class="mx-auto w-10 bg-white opacity-80"
    v-slot="{ iconSizeClasses }"
    v-show="sidebarState.isOpen || sidebarState.isHovered"
    @click="sidebarState.isOpen = !sidebarState.isOpen"
    :srText="sidebarState.isOpen ? 'Close sidebar' : 'Open sidebar'"
  >
    <MenuFoldLineLeftIcon
      aria-hidden="true"
      v-show="sidebarState.isOpen"
      :class="['hidden lg:block', iconSizeClasses]"
      class="text-blue-500"
    />

    <MenuFoldLineRightIcon
      aria-hidden="true"
      v-show="!sidebarState.isOpen"
      :class="['hidden lg:block', iconSizeClasses]"
    />

    <XIcon aria-hidden="true" :class="['lg:hidden', iconSizeClasses]" />
  </Button>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { TemplateIcon } from '@/components/icons/outline'
import { MenuFoldLineLeftIcon, MenuFoldLineRightIcon } from '@/components/icons/outline'
import { ShieldCheckIcon, DocumentIcon, UserGroupIcon, MapIcon } from '@heroicons/vue/outline'
import SidebarCollapsible from '@/components/sidebar/SidebarCollapsible.vue'
import SidebarCollapsibleItem from '@/components/sidebar/SidebarCollapsibleItem.vue'
import { XIcon } from '@heroicons/vue/outline'
import { sidebarState } from '@/composables'
import { computed } from 'vue'
import { useStorage } from '@vueuse/core'

const isCurrentRoute = (routeName) => {
  return useRouter().currentRoute.value.name == routeName
}

const isCurrentPath = (path) => {
  return useRouter().currentRoute.value.path.startsWith(path)
}
</script>
