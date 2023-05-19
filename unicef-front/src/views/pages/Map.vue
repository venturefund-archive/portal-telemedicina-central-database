<template>
  <PageWrapper>
    <div class="pb-10">
      <div class="flex items-baseline justify-center py-10">
        <div class="mr-4 md:flex-1">
          <MapGoogle />
        </div>
        <div class="md:w-1/3">
          <div class="m-3">
            <PatientListCard />
          </div>
        </div>
      </div>
    </div>
  </PageWrapper>
</template>

<script setup>
import { onMounted } from 'vue'
import MapGoogle from '@/components/organisms/MapGoogle.vue'
</script>
