<template>
  <label for="default-search" class="sr-only mb-2 text-sm font-medium text-gray-900">Procurar</label>
  <div class="relative">
    <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-2">
      <slot name="icon" />
    </div>
    <slot />
  </div>
</template>
