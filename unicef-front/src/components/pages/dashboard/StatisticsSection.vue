<template>
  <div class="">
    <section class="flex flex-wrap justify-around" v-if="protocolStore.item">
      <SquareCard
        :title="$t('dashboard.total-alerts')"
        :result="`${protocolStore.item.alert_doses_count}`"
        class="text-gray-500"
      >
        <template #icon="{ sizeClasses }">
          <BellIcon aria-hidden="true" class="mr-2 h-9 text-red-500" />
        </template>
      </SquareCard>

      <SquareCard
        :title="$t('dashboard.completed-doses')"
        :result="protocolStore.item.completed_doses_percentage + `%`"
        class="text-green-400"
      >
      </SquareCard>

      <SquareCard
        v-for="(dose, k) in protocolStore.item.vaccine_doses"
        :key="k"
        :class="{ 'text-blue-500': k == 0, 'text-yellow-300': k > 0 }"
        :title="dose.vaccine.name"
        :result="`${dose.completed_percentage}%`"
        class=""
      >
      </SquareCard>
    </section>
    <section class="flex flex-wrap justify-between" v-else>
      <SkeletonLoader type="text" animation="fade-in" class="h-52 w-56 py-3" v-for="i in 4" />
    </section>
  </div>
</template>

<script setup>
import { BellIcon, CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/vue/solid'
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
