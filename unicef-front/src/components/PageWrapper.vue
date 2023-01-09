<template>
  <!-- Page Heading -->
  <header v-if="$slots.header || title">
    <div class="p-4 sm:p-6">
      <slot name="header">
        <h2 class="text-xl font-semibold leading-tight">{{ title }}</h2>
      </slot>
    </div>
  </header>

  <!-- Page Content -->
  <main class="w-full" :class="{ 'mt-2': !$slots.header }">
    <div class="px-5 lg:px-8">
      <slot />
    </div>
  </main>
</template>

<script setup>
const props = defineProps({
  title: String,
})
</script>
