<template>
  <footer class="mt-20">
    <div class="flex w-full px-10 py-4 text-gray-500 dark:text-gray-400 lg:flex-row lg:justify-between">
      <p class="text-sm">
        &#169;
        <span class="pr-0.5">{{ new Date().getFullYear() }}</span>
        <a href="https://portaltelemedicina.com.br/" target="_blank" class="text-blue-600 hover:underline"
          >Portal Telemedicina</a
        >. {{ $t('dashboard.all-rights-reserved') }}
      </p>
      <p class="flex items-center gap-1 text-sm">
        <span>{{ $t('dashboard.distributed-by-unicef') }}</span>
      </p>
    </div>
    <div class="flex w-full px-10 py-4 text-gray-400 dark:text-gray-400 lg:flex-row lg:justify-end">
      <p class="text-center text-sm text-neutral-300" v-if="commit_ref">
        <a :href="repository_url + '/-/commit/' + commit_ref" target="_blank">#{{ commit_ref.substring(0, 7) }}</a>
        <span v-if="branch">
          on <a :href="repository_url + '/-/tree/' + branch" target="_blank">{{ branch }}</a
          >.
        </span>
      </p>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue'
</script>
