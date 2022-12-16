<template>
  <PerfectScrollbar tagname="nav" aria-label="main" class="relative flex max-h-full flex-1 flex-col gap-4 px-3">
    <SidebarLink title="Dashboard" :to="{ name: 'Dashboard' }" :active="isCurrentRoute('Dashboard')">
      <template #icon>
        <TemplateIcon class="h-6 w-6 flex-shrink-0" aria-hidden="true" />
      </template>
    </SidebarLink>

  </PerfectScrollbar>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { TemplateIcon } from '@/components/icons/outline'
import { ShieldCheckIcon, DocumentIcon, UserGroupIcon } from '@heroicons/vue/outline'
import SidebarCollapsible from '@/components/sidebar/SidebarCollapsible.vue'
import SidebarCollapsibleItem from '@/components/sidebar/SidebarCollapsibleItem.vue'

const isCurrentRoute = (routeName) => {
  return useRouter().currentRoute.value.name == routeName
}

const isCurrentPath = (path) => {
  return useRouter().currentRoute.value.path.startsWith(path)
}
</script>
