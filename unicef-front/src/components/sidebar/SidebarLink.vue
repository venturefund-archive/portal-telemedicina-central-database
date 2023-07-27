<template>
  <a
    v-if="href"
    :href="href"
    :class="[
      'flex flex-col items-center gap-2 rounded-md p-2 no-underline transition-colors hover:no-underline',
      {
        'bg-blue-500 text-white': !active,
        ' bg-blue-660 text-white shadow': active,
      },
    ]"
  >
    <slot name="icon">
      <EmptyCircleIcon aria-hidden="true" class="h-6 w-6 flex-shrink-0" />
    </slot>

    <span class="text-base font-normal" v-show="sidebarState.isOpen || sidebarState.isHovered">{{ title }}</span>
  </a>
  <router-link
    v-else-if="to"
    :to="to"
    :class="[
      'flex flex-col items-center gap-2 rounded-md p-2 no-underline transition-colors hover:no-underline',
      {
        'bg-blue-500 text-white': !active,
        ' bg-blue-660 text-white shadow': active,
      },
    ]"
  >
    <slot name="icon">
      <EmptyCircleIcon aria-hidden="true" class="h-6 w-6 flex-shrink-0" />
    </slot>

    <span class="text-base font-normal" v-show="sidebarState.isOpen || sidebarState.isHovered">{{ title }}</span>
  </router-link>
  <button
    v-else
    type="button"
    :class="[
      'flex w-full items-center gap-2 rounded-md p-2 transition-colors',
      {
        'bg-blue-500 text-white': !active,
        ' bg-blue-660 text-white shadow': active,
      },
    ]"
  >
    <slot name="icon">
      <EmptyCircleIcon aria-hidden="true" class="h-6 w-6 flex-shrink-0" />
    </slot>

    <span class="text-base font-normal" v-show="sidebarState.isOpen || sidebarState.isHovered">{{ title }}</span>
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
