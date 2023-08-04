<template>
  <div class="h-auto w-auto rounded-2xl border border-gray-200 bg-white p-4 text-lg font-normal">
    <div class="z-10 p-10">
      <div class="relative">
        <div class="flex items-center justify-between pb-10 pt-1">
          <div class="flex items-center">
            <CheckCircleIcon class="h-8 w-8 rounded-full bg-lime-600 text-white" v-if="isCompleted" />
            <ExclamationCircleIcon class="h-8 w-8 rounded-full bg-red-500 text-white" v-else-if="hasAlerts && active" />
            <VolumeOffIcon class="h-8 w-8 rounded-full bg-red-500 p-1 text-white" v-else-if="hasAlerts && !active" />
            <LightBulbIcon class="h-9 w-9 rounded-full bg-blue-300 p-1 text-white" v-else />
          </div>
          <div class="flex items-center p-2">
            <div>
              <h2 v-if="isCompleted">{{ $t('patient-details.completed-dose') }}</h2>
              <h2 v-else-if="hasAlerts && active">{{ $t('patient-details.delayed-dose') }}</h2>
              <h2 v-else-if="hasAlerts && !active">{{ $t('patient-details.silenced-dose') }}</h2>
              <h2 v-else>{{ $t('patient-details.recommended-dose') }}</h2>
            </div>
          </div>
          <div class="ml-auto">
            <span class="rounded-lg bg-blue-500 p-1.5 text-sm uppercase tracking-wide text-white">
              {{ $t('patient-details.dose') }} <span class="font-semibold">#{{ props.dose.dose_order }}</span>
            </span>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="vaccine" class="block p-2 text-base">{{ $t('patient-details.vaccine') }}</label>
            <input
              id="vaccine"
              type="text"
              v-model="doseForm.vaccine.description"
              class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2"
              readonly
            />
          </div>
          <div>
            <label for="recommended" class="block p-2 text-base">{{ $t('patient-details.recommended') }}</label>
            <input
              id="recommended"
              type="text"
              v-model="doseForm.recommended_age"
              class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2"
              readonly
            />
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4" v-if="props.dose.status && props.dose.status.completed">
          <div>
            <label for="cns_number" class="block px-4 py-2 text-base">
              CSN {{ $t('patient-details.profissional') }}
            </label>
            <input
              id="cns_number"
              type="text"
              v-model="doseForm.health_professional.cns_number"
              class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2"
              readonly
            />
          </div>

          <div>
            <label for="profissional" class="block p-2 text-base">{{ $t('patient-details.profissional') }}</label>
            <input
              id="profissional"
              type="text"
              v-model="doseForm.health_professional.name"
              class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2"
              readonly
            />
          </div>

          <div>
            <label for="cnes_number" class="block px-4 py-2 text-base"> CNES </label>
            <input
              id="cnes_number"
              type="text"
              v-model="doseForm.health_professional.cnes_number"
              class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2"
              readonly
            />
          </div>

          <div>
            <label for="batch" class="block p-2 text-base">{{ $t('patient-details.batch') }}</label>
            <input
              id="batch"
              type="text"
              v-model="doseForm.batch"
              class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2"
              readonly
            />
          </div>

          <div>
            <label for="data-application" class="block px-4 py-2 text-base">{{
              $t('patient-details.dose-application-date')
            }}</label>
            <input
              id="data-application"
              type="text"
              v-model="doseForm.application_date"
              class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2"
              readonly
            />
          </div>
          <div>
            <label for="next-data-application" class="block px-4 py-2 text-base">
              {{ $t('patient-details.next-application') }}
            </label>
            <input
              id="next-data-application"
              type="text"
              v-model="doseForm.next_dose_application_date"
              class="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2"
              readonly
            />
          </div>
        </div>
      </div>
      <div v-if="shouldShow" class="py-10">
        <button
          @click="toggleActive"
          class="ml-2 flex items-center rounded-lg px-2 py-1"
          :class="!active ? 'bg-blue-500' : 'bg-red-500'"
        >
          <VolumeOffIcon v-if="active" class="h-8 w-8 p-1 text-white" />
          <VolumeUpIcon v-if="!active" class="h-8 w-8 p-1 text-white" />
          <span v-if="active" class="ml-1 text-sm font-semibold text-white">{{
            $t('patient-details.alert-silent-notification')
          }}</span>
          <span v-else class="ml-1 text-sm font-semibold text-white">{{
            $t('patient-details.alert-activate-notification')
          }}</span>
        </button>

        <!--        <button-->
        <!--          v-if="!isCompleted"-->
        <!--          type="button"-->
        <!--          @click=""-->
        <!--          class="mt-5 flex items-center space-x-5 rounded-full bg-red-700 py-2 px-3 text-base  text-white hover:bg-red-600"-->
        <!--        >-->
        <!--          <PlusCircleIcon class="h-6 w-6" />-->
        <!--          <span class="uppercase tracking-wide">{{ $t('patient-details.add-alert') }}</span>-->
        <!--        </button>-->

        <div v-for="(alert, k) in props.dose.alerts" :key="k">
          <span class="flex justify-end text-sm text-gray-500">
            {{ $t('patient-details.registred') }} {{ formatRelative(parseISO(alert.created_at), new Date()) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  // PlusCircleIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
  VolumeUpIcon,
  VolumeOffIcon,
  LightBulbIcon,
} from '@heroicons/vue/outline'
import { useI18n } from 'vue3-i18n'

import { usePatientsStore } from '@/stores/patients'
import { parseISO, formatRelative, formatDuration, add, setDefaultOptions, differenceInMonths, format } from 'date-fns'
const emit = defineEmits(['update:toggle-active'])
const { t } = useI18n()
const patientsStore = usePatientsStore()
const birthDate = computed(() => parseISO(patientsStore.item.birth_date))

const doseApplicationDate = computed(() => {
  if (!props.dose.status) {
    return ''
  }
  return format(parseISO(props.dose.status.application_date), 'dd/MM/yyyy')
})
const nextDoseApplicationDate = computed(() => {
  if (!props.dose.status) {
    return ''
  }
  if (!props.dose.status?.next_dose_application_date) {
    return t('patient-details.unknown')
  }
  return format(parseISO(props.dose.status?.next_dose_application_date), 'dd/MM/yyyy')
})

const recommendedDate = ref(add(birthDate.value, { months: props.dose.maximum_recommended_age }))
const isCompleted = computed(() => props.dose?.status?.completed)
const hasAlerts = computed(() => props.dose.alerts.length > 0)
const doseForm = ref({
  patient_id: patientsStore.item.id,
  vaccine_id: null,
  vaccine_dose: null,
  vaccine: {
    description: props.vaccine.description,
  },
  recommended_age: formatDuration({ months: props.dose.maximum_recommended_age }),
  health_professional: {
    name:
      props.dose?.status?.health_professional?.name == null
        ? t('patient-details.unknown')
        : props.dose?.status?.health_professional?.name,
    cns_number:
      props.dose?.status?.health_professional?.cns_number == null
        ? t('patient-details.unknown')
        : props.dose?.status?.health_professional?.cns_number,
    cnes_number:
      props.dose?.status?.health_professional?.cnes_number == null
        ? t('patient-details.unknown')
        : props.dose?.status?.health_professional?.cnes_number,
  },
  batch: props.dose.status?.batch,
  application_date: doseApplicationDate.value,
  next_dose_application_date: nextDoseApplicationDate.value,
  fhir_store: 1,
  completed: true,
  processing: false,
})

const shouldShow = computed(() => {
  const isFormStatusTrue = doseForm.value.status
  const isDoseStatusCompletedTrue = isCompleted.value

  return hasAlerts.value && !isFormStatusTrue && !isDoseStatusCompletedTrue
})

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

let active = ref(props.dose.alerts.filter((alert) => alert.active).length > 0)

const toggleActive = () => {
  emit('update:toggle-active', { dose: props.dose, active: active.value })
  active.value = !active.value
}
</script>
