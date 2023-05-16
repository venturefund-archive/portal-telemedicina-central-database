<template>
<div class="flex justify-center pt-2">
<section class="flex justify-start" v-if="protocolStore.item">
    <QuickStatisticsCard
      :title="$t('dashboard.total-alerts')"
      :result="protocolStore.item.alert_doses_count"
      class="bg-red-500 overflow-hidden flex items-center justify-center word-break w-full md:w-auto mr-20"
      style="width: 279px; height: 117px;"
    >
      <template #icon="{ sizeClasses }">
        <ExclamationCircleIcon aria-hidden="true" class="h-12 w-12 text-white mr-4" />
      </template>
    </QuickStatisticsCard>

    <QuickStatisticsCard
      :title="$t('dashboard.completed-doses')"
      :result="protocolStore.item.completed_doses_percentage + `%`"
      class="bg-yellow-500 overflow-hidden flex items-center justify-center word-break w-full md:w-auto mr-20"
      style="width: 279px; height: 117px;"
    >
      <template #icon="{ sizeClasses }">
        <CheckCircleIcon aria-hidden="true" class="h-12 w-12 text-white mr-4" />
      </template>
    </QuickStatisticsCard>

    <div v-for="(dose, k) in protocolStore.item.vaccine_doses" :key="k">
      <QuickStatisticsCard
        :class="{ 'bg-blue-500': k == 0, 'bg-[#7A6EFE]': k > 0 }"
        :title="dose.vaccine.name"
        :result="`${dose.completed_percentage}%`"
        class="overflow-hidden flex items-center justify-center word-break w-full md:w-auto mr-20"
        style="width: 279px; height: 117px;"
      >
        <template #icon="{ sizeClasses }">
          <CheckCircleIcon aria-hidden="true" class="h-12 w-12 text-white ml-4" />
        </template>
      </QuickStatisticsCard>
    </div>
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
