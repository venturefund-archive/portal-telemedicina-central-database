<template>
  <footer class="flex w-full flex-shrink-0 flex-col gap-2 px-6 py-4 lg:flex-row lg:justify-between">
    <p class="text-sm text-gray-500 dark:text-gray-400">
      &#169;
      <span>{{ new Date().getFullYear() }}</span> unicef, All rights reserved
    </p>

    <p class="flex items-center gap-1 text-sm text-gray-500 dark:text-gray-400">
      <span>Made</span>
      <span>by</span>
      <a href="https://portaltelemedicina.com.br/" target="_blank" class="text-blue-600 hover:underline"
        >Portal Telemedicina</a
      >
    </p>
  </footer>
</template>
