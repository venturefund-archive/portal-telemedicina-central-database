<template>
  <div class="min-w-96 text-lg font-normal">
    <div class="relative bg-neutral-50 p-4">
      <div class="flex justify-between py-1">
        <p class="px-1 font-semibold">{{ props.vaccine.description }}</p>
        <div v-if="dose.is_completed">
          <CheckCircleIcon class="h-7 w-7 rounded-full bg-lime-600 text-white"></CheckCircleIcon>
        </div>
        <div class="py-1" v-if="!dose.is_completed">
          <ExclamationCircleIcon class="h-7 w-7 rounded-full bg-red-500 text-white"></ExclamationCircleIcon>
        </div>
      </div>

      <p class="">
        Dose <span class="font-semibold">#{{ props.dose.dose_order }} </span>
      </p>
      Idade: {{ props.dose.maximum_recommended_age }} meses <br />
      Gênero: {{ props.dose.gender_recommendation }}<br />
    </div>
    <div class="bg-neutral-200 p-4 font-normal">
      <p class="font-semibold">Alerts</p>
      <div v-for="(alert, k) in props.dose.alerts" :key="k">
        Id: {{ alert.id }} <br />
        Tipo de alert: {{ alert.alert_type }}<br />
        Criado em: {{ formatRelative(parseISO(alert.created_at), new Date()) }}
      </div>
      Total: {{ props.dose.alerts.length }} alertas
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import PerfectScrollbar from 'perfect-scrollbar'
import { CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/vue/outline'

import { parseISO, formatRelative } from 'date-fns'

const props = defineProps({
  vaccine: {
    type: Object,
    default: {},
  },
  dose: {
    type: Object,
    default: {},
  },
})
</script>
