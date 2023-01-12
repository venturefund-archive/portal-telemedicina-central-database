<template>
  <footer class="mt-5 mb-20 ">
    <div class="flex w-full px-10 py-4 lg:flex-row lg:justify-between text-gray-500 dark:text-gray-400">
      <p class="text-sm">
        &#169;
        <span>{{ new Date().getFullYear() }}</span> <a href="https://portaltelemedicina.com.br/" target="_blank"
                                                       class="text-blue-600 hover:underline"
      >Portal Telemedicina</a>. Todos os direitos reservados.
      </p>
      <p class="flex items-center gap-1 text-sm">
        <span>Distribuído por UNICEF</span>
      </p>
    </div>
    <div class="flex w-full px-10 py-4 lg:flex-row lg:justify-end text-gray-400 dark:text-gray-400">
      <p class="text-sm text-neutral-300 text-center" v-if="commit_ref">
        <a :href="repository_url+'/-/commit/' + commit_ref" target="_blank">#{{ commit_ref.substring(0, 7) }}</a>
        <span v-if="branch">
        on <a :href="repository_url+'/-/tree/' + branch" target="_blank">{{ branch }}</a>.
      </span>
      </p>
    </div>
  </footer>
</template>


<script setup>
import { ref } from "vue"

const site_name = ref(import.meta.env.SITE_NAME)
const url = ref(import.meta.env.URL)
const repository_url = ref(import.meta.env.REPOSITORY_URL) // URL for the linked Git repository.
const commit_ref = ref(import.meta.env.COMMIT_REF) // Reference of the commit we’re building.
const branch = ref(import.meta.env.BRANCH) // Reference to check out after fetching changes from the Git repository. useful in split testing https://www.netlify.com/docs/split-testing/#exposing-split-test-information-in-your-site
</script>
