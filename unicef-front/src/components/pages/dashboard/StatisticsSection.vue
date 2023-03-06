<template>
  <section class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4 place-content-center" v-if="protocolStore.item">
    <h2 class="sr-only">Quick statistics</h2>
    <QuickStatisticsCard title="Doses completas" :result="protocolStore.item.completed_doses_percentage + `%`" class="bg-green-500">
      <template #icon="{ sizeClasses }">
        <CheckCircleIcon aria-hidden="true" class="h-12 w-12 text-white" />
      </template>
    </QuickStatisticsCard>
    <div v-for="(dose, k) in protocolStore.item.vaccine_doses" :key="k">
      <QuickStatisticsCard class="bg-blue-500"
                           :title="dose.vaccine.name"
                           :result="`${dose.completed_percentage}%`">
        <template #icon="{ sizeClasses }">
          <CheckCircleIcon aria-hidden="true" class="h-12 w-12 text-white" />
        </template>
      </QuickStatisticsCard>
    </div>

    <QuickStatisticsCard title="Total de alertas" :result="protocolStore.item.alert_doses_count" class="bg-red-500">
      <template #icon="{ sizeClasses }">
        <ExclamationCircleIcon aria-hidden="true" class="h-12 w-12 text-white" />
      </template>
    </QuickStatisticsCard>
  </section>
</template>

<script setup>
import {CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/vue/solid'
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
