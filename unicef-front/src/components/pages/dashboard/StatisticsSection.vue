<template>
  <div class="pt-2">
    <section class="flex flex-wrap justify-around" v-if="protocolStore.item">
      <QuickStatisticsCard
        :title="$t('dashboard.total-alerts')"
        :result="protocolStore.item.alert_doses_count"
        class="word-break my-2 flex min-h-full bg-red-500"
      >
        <template #icon="{ sizeClasses }">
          <ExclamationCircleIcon aria-hidden="true" class="mr-4 h-12 w-12 text-white" />
        </template>
      </QuickStatisticsCard>

      <QuickStatisticsCard
        :title="$t('dashboard.completed-doses')"
        :result="protocolStore.item.completed_doses_percentage + `%`"
        class="word-break my-2 flex min-h-full bg-yellow-500"
      >
        <template #icon="{ sizeClasses }">
          <CheckCircleIcon aria-hidden="true" class="break-word mr-4 h-12 w-12 text-white" />
        </template>
      </QuickStatisticsCard>

      <QuickStatisticsCard
        v-for="(dose, k) in protocolStore.item.vaccine_doses"
        :key="k"
        :class="{ 'bg-blue-500': k == 0, 'bg-[#7A6EFE]': k > 0 }"
        :title="dose.vaccine.name"
        :result="`${dose.completed_percentage}%`"
        class="word-break my-2 flex min-h-full"
      >
        <template #icon="{ sizeClasses }">
          <CheckCircleIcon aria-hidden="true" class="h-12 w-12 text-white" />
        </template>
      </QuickStatisticsCard>
    </section>
      <section class="flex flex-wrap justify-around" v-else>
      <SkeletonLoader type="text" animation="fade-in" class="py-3 h-[130px] w-[300px]" v-for="i in 4" />
    </section>
  </div>
</template>

<script setup>
import { CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/vue/solid'
import { useProtocolStore } from '@/stores/protocol'
import { onMounted, onUpdated, reactive, ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { watch, computed } from 'vue'
const protocolStore = useProtocolStore()
const router = useRouter()

onMounted(async () => {
  await protocolStore.fetchProtocol(1)
})
</script>

<style>
.break-word {
  word-wrap: break-word;
  overflow-wrap: break-word;
}
</style>
