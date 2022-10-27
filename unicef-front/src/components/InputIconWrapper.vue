<template>
  <div class="relative text-gray-500 focus-within:text-gray-900 dark:focus-within:text-gray-400">
    <div aria-hidden="true" class="pointer-events-none absolute inset-y-0 flex items-center px-4">
      <slot name="icon" />
    </div>
    <slot />
  </div>
</template>
