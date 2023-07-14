<template>
  <PageWrapper>
    <template #header>
      <div class="pl-5 pt-5">
        <p class="text-xl font-semibold" v-if="loggedUserStore.item">
          {{ $t('dashboard.greetings', { name: loggedUserStore.item.username }) }}
        </p>
        <span class="text-neutral-500">{{ $t('dashboard.welcome') }}</span>
      </div>
    </template>

    <!-- Statistics section -->
    <StatisticsSection class="lg:my-6" />

    <!-- Latest users section -->
    <LatestSection class="lg:my-4" :page-size="100" v-once />
  </PageWrapper>
</template>

<script setup>
import { useLoggedUserStore } from '@/stores/loggedUser'
const loggedUserStore = useLoggedUserStore()
import { onMounted, ref, computed, reactive } from 'vue'
import { usePatientsStore } from '@/stores/patients'
const patientsStore = usePatientsStore()
onMounted(async () => {
  if(patientsStore.items.length == 0){
    await patientsStore.fetchPatients()
    await patientsStore.fetchPatientsRecursive()
  }

})
</script>
