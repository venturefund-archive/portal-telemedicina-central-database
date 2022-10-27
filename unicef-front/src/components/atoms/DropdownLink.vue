<template>
  <MenuItem v-slot="{ active, disabled }">
    <router-link
      :class="[
        'block w-full px-4 py-2 text-left text-sm leading-5 text-gray-700 transition duration-150 ease-in-out focus:outline-none',
        {
          'bg-gray-100': active,
          'pointer-events-none': disabled,
        },
      ]"
    >
      <slot />
    </router-link>
  </MenuItem>
</template>

<script setup>
import { MenuItem } from '@headlessui/vue'
</script>
