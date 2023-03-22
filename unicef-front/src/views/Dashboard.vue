<template>
  <PageWrapper>
    <template #header>
      <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <h2 class="text-xl font-semibold leading-tight">Dashboard</h2>
      </div>
      <div class="pl-5 pt-3">
        <p class="font-semibold" v-if="loggedUserStore.item">{{ $t('dashboard.greetings', { name: loggedUserStore.item.username }) }}</p>
        <span class="text-neutral-500">{{ $t('dashboard.welcome') }}</span>
      </div>
    </template>

    <!-- Statistics section -->
    <StatisticsSection class="lg:my-6" />

    <!-- Latest users section -->
    <LatestSection class="lg:my-4" />
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
