<template>
  <PageWrapper>
    <template #header>
      <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <h2 class="text-xl font-semibold leading-tight">Dashboard</h2>
      </div>
      <div class="pl-5 pt-3">
        <p class="font-bold" v-if="loggedUserStore.item">Welcome, {{ loggedUserStore.item.username }}</p>
        <span>Have a nice day and a nice job.</span>
      </div>
    </template>

    <!-- Statistics section -->
    <StatisticsSection />

    <!-- Latest users section -->
    <LatestSection />

    <!-- Latest vaccines section -->
    <div class="flex">
      <h4 class="text-lg font-medium">Child development milestones</h4>
      <span class="px-3 text-xs">0 to 15 years</span>
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
