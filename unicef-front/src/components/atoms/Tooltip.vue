<template>
  <div class="group relative inline-block">
    <slot name="trigger"></slot>

    <div
      class="absolute left-full top-1/2 z-10 rounded bg-blue-500 bg-opacity-70 py-1 px-2 text-xs font-semibold text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100"
      style="transform: translateY(-50%)"
    >
      <slot name="content"></slot>
      <div
        class="absolute left-0 top-1/2 -ml-3 h-3 w-3 bg-blue-500 bg-opacity-70"
        style="clip-path: polygon(100% 0%, 0 50%, 100% 100%); transform: translateY(-50%)"
      ></div>
      <div class="absolute inset-0 left-full -ml-1 w-6"></div>
    </div>
  </div>
</template>
