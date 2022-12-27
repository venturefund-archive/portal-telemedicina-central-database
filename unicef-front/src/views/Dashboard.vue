<template>
  <PageWrapper>
    <template #header>
      <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <h2 class="text-xl font-semibold leading-tight">Dashboard</h2>
      </div>
      <div class="pl-5 pt-3">
        <p class="font-bold" v-if="loggedUserStore.item">Bem-vindo, {{ loggedUserStore.item.username }}</p>
        <span>Tenha um ótimo dia e um bom trabalho.</span>
      </div>
    </template>

    <!-- Statistics section -->
    <StatisticsSection class="lg:my-6" />

    <!-- Latest users section -->
    <LatestSection class="lg:my-4" />

    <!-- Latest vaccines section -->
    <div class="flex">
      <h4 class="text-lg font-medium">Marcos do desenvolvimento infantil</h4>
      <span class="px-3 text-xs">0 a 15 anos</span>
    </div>
  </PageWrapper>
</template>

<script setup>
import { onMounted } from 'vue'
import { useLoggedUserStore } from '@/stores/loggedUser'
const loggedUserStore = useLoggedUserStore()

onMounted(async () => {
  await loggedUserStore.fetchMe()
})
</script>
