<template>
  <PageWrapper>
    <template #header>
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
