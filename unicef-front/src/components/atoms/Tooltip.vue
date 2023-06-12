<template>
  <div class="relative group inline-block">
    <slot name="trigger"></slot>

    <div
      class="absolute bg-blue-500 text-white font-semibold bg-opacity-70 text-xs rounded py-1 px-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 left-full top-1/2 z-10"
      style="transform: translateY(-50%);"
      >
      <slot name="content"></slot>
      <div class="absolute h-3 w-3 bg-blue-500 left-0 top-1/2 -ml-3 bg-opacity-70" style="clip-path: polygon(100% 0%, 0 50%, 100% 100%); transform: translateY(-50%);"></div>
      <div class="absolute inset-0 w-6 left-full -ml-1"></div>
    </div>
  </div>
</template>
