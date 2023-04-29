<template>
  <div class="min-w-96 text-lg font-normal">
    <div class="relative bg-neutral-50 p-4">
      <div class="flex items-center justify-between pt-1 pb-2.5">
        <div class="flex">
          <div v-if="!props.withoutDetails">
            <CheckCircleIcon class="h-7 w-7 rounded-full bg-lime-600 text-white" v-if="dose.is_completed" />
            <ExclamationCircleIcon class="h-7 w-7 rounded-full bg-red-500 text-white" v-else />
          </div>
          <p class="px-2 font-semibold tracking-wider">{{ props.vaccine.description }}</p>
        </div>
        <span class="rounded-lg bg-green-200 bg-opacity-50 p-1.5 text-sm uppercase text-green-800"
          >{{ $t('patient-details.dose') }} <span class="font-semibold">#{{ props.dose.dose_order }}</span></span
        >
      </div>
      <p>
        {{ $t('patient-details.recommended') }}: {{ formatDuration({ months: props.dose.maximum_recommended_age }) }}
      </p>
      <p>{{ $t('patient-details.gender') }}: {{ props.dose.gender_recommendation }}</p>
    </div>
    <div class="bg-neutral-200 p-4 font-normal" v-if="props.dose.alerts.length > 0">
      <p class="font-semibold">Alerts</p>
      <div v-for="(alert, k) in props.dose.alerts" :key="k">
        Id: {{ alert.id }} <br />
        Tipo de alerta: {{ alert.alert_type }}<br />
        Criado em: {{ formatRelative(parseISO(alert.created_at), new Date()) }}
      </div>
      <span>Total: {{ props.dose.alerts.length }} alertas</span>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, computed } from 'vue'
import PerfectScrollbar from 'perfect-scrollbar'
import { CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/vue/outline'
import { usePatientsStore } from '@/stores/patients'
import { parseISO, formatRelative, formatDuration, add, setDefaultOptions, differenceInMonths } from 'date-fns'
const patientsStore = usePatientsStore()

const birthDate = ref(parseISO(patientsStore.item.birth_date))
const recommendedDate = ref(add(birthDate.value, { months: props.dose.maximum_recommended_age }))

const props = defineProps({
  withoutDetails: {
    type: Boolean,
    default: false,
  },
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
