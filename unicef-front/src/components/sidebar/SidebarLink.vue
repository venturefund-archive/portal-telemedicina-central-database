<template>
  <a
    v-if="href"
    :href="href"
    :class="[
      'flex items-center flex-col gap-2 rounded-md p-2 no-underline transition-colors hover:no-underline',
      {
        'text-white bg-blue-500':
          !active,
        ' text-white shadow bg-blue-660': active,
      },
    ]"
  >
    <slot name="icon">
      <EmptyCircleIcon aria-hidden="true" class="h-6 w-6 flex-shrink-0" />
    </slot>

    <span class="text-base font-medium" v-show="sidebarState.isOpen || sidebarState.isHovered">{{ title }}</span>
  </a>
  <router-link
    v-else-if="to"
    :to="to"
    :class="[
      'flex items-center flex-col gap-2 rounded-md p-2 no-underline transition-colors hover:no-underline',
      {
        'text-white bg-blue-500':
          !active,
        ' text-white shadow bg-blue-660': active,
      },
    ]"
  >
    <slot name="icon">
      <EmptyCircleIcon aria-hidden="true" class="h-6 w-6 flex-shrink-0" />
    </slot>

    <span class="text-base font-medium" v-show="sidebarState.isOpen || sidebarState.isHovered">{{ title }}</span>
  </router-link>
  <button
    v-else
    type="button"
    :class="[
      'flex w-full items-center gap-2 rounded-md p-2 transition-colors',
      {
        'text-white bg-blue-500':
          !active,
        ' text-white shadow bg-blue-660': active,
      },
    ]"
  >
    <slot name="icon">
      <EmptyCircleIcon aria-hidden="true" class="h-6 w-6 flex-shrink-0" />
    </slot>

    <span class="text-base font-medium" v-show="sidebarState.isOpen || sidebarState.isHovered">{{ title }}</span>
    <slot name="arrow" />
  </button>
</template>

<script setup>
import { sidebarState } from '@/composables'
import { EmptyCircleIcon } from '@/components/icons/outline'

const props = defineProps({
  href: {
    type: String,
    required: false,
  },
  to: {
    type: [String, Object],
    required: false,
  },
  active: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    required: true,
  },
})
</script>
