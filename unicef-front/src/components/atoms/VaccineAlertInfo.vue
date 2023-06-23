<template>
  <div class="p-4 text-lg font-normal rounded-2xl border border-gray-50 bg-white drop-shadow-md h-auto w-auto">
    <div class="z-10 p-10">
      <div class="relative">
        <div class="flex items-center justify-between pt-1 pb-10">
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
            <span class="rounded-lg bg-blue-500 p-1.5 text-sm uppercase text-white">
              {{ $t('patient-details.dose') }} <span class="font-semibold">#{{ props.dose.dose_order }}</span>
            </span>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="vaccine" class="block p-2 text-sm font-medium text-gray-700">{{
              $t('patient-details.vaccine')
            }}</label>
            <input
              id="vaccine"
              type="text"
              :value="props.vaccine.description"
              class="block w-full rounded-full border-none bg-gray-100 py-2 px-4"
              readonly
            />
          </div>
          <div>
            <label for="recommended" class="block p-2 text-sm font-medium text-gray-700">{{
              $t('patient-details.recommended')
            }}</label>
            <input
              id="recommended"
              type="text"
              :value="formatDuration({ months: props.dose.maximum_recommended_age })"
              class="block w-full rounded-full border-none bg-gray-100 py-2 px-4"
              readonly
            />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4" v-if="props.dose.status && props.dose.status.completed">
          <div>
            <label for="cns_number" class="block py-2 px-4 text-sm font-medium text-gray-700"> CSN </label>
            <input
              id="cns_number"
              type="text"
              :value="
                props.dose?.status?.health_professional?.cns_number == null
                  ? 'Desconhecido'
                  : props.dose?.status?.health_professional?.cns_number
              "
              class="block w-full rounded-full border-none bg-gray-100 py-2 px-4"
              readonly
            />
          </div>

          <div>
            <label for="profissional" class="block p-2 text-sm font-medium text-gray-700">{{
              $t('patient-details.profissional')
            }}</label>
            <input
              id="profissional"
              type="text"
              :value="
                props.dose.status.health_professional.name == null
                  ? 'Desconhecido'
                  : props.dose.status.health_professional.name
              "
              class="block w-full rounded-full border-none bg-gray-100 py-2 px-4"
              readonly
            />
          </div>

          <div>
            <label for="cnes_number" class="block py-2 px-4 text-sm font-medium text-gray-700"> CNES </label>
            <input
              id="cnes_number"
              type="text"
              :value="
                props.dose?.status?.health_professional?.cnes_number == null
                  ? 'Desconhecido'
                  : props.dose?.status?.health_professional?.cnes_number
              "
              class="block w-full rounded-full border-none bg-gray-100 py-2 px-4"
              readonly
            />
          </div>

          <div>
            <label for="batch" class="block p-2 text-sm font-medium text-gray-700">{{
              $t('patient-details.batch')
            }}</label>
            <input
              id="batch"
              type="text"
              :value="props.dose.status.batch"
              class="block w-full rounded-full border-none bg-gray-100 py-2 px-4"
              readonly
            />
          </div>

          <div>
            <label for="data-application" class="block py-2 px-4 text-sm font-medium text-gray-700">{{
              $t('patient-details.dose-application-date')
            }}</label>
            <input
              id="data-application"
              type="text"
              :value="format(doseApplicationDate, 'dd/MM/yyyy')"
              class="block w-full rounded-full border-none bg-gray-100 py-2 px-4"
              readonly
            />
          </div>
          <div>
            <label for="next-data-application" class="block py-2 px-4 text-sm font-medium text-gray-700">
              {{ $t('patient-details.next-application') }}
            </label>
            <input
              id="next-data-application"
              type="text"
              :value="format(nextDoseApplicationDate, 'dd/MM/yyyy')"
              class="block w-full rounded-full border-none bg-gray-100 py-2 px-4"
              readonly
            />
          </div>
        </div>
      </div>
      <div v-if="(props.dose.status == null || false == props.dose.status.completed) &&
                  props.dose.alerts.length > 0" class="py-10">
        <button
          @click="toggleActive"
          class="ml-2 flex items-center rounded-lg py-1 px-2"
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
      </div>

      <div class="font-normal" v-if="(props.dose.status == null || false == props.dose.status.completed) && props.dose.alerts.length > 0">
        <div>
          <div v-for="(alert, k) in props.dose.alerts" :key="k">
            <span class="flex justify-end text-sm text-gray-500">
              {{ $t('patient-details.registred') }} {{ formatRelative(parseISO(alert.created_at), new Date()) }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  CheckCircleIcon,
  ExclamationCircleIcon,
  LightBulbIcon,
  VolumeOffIcon,
  VolumeUpIcon,
  CheckIcon,
  XIcon,
} from '@heroicons/vue/outline'
import { usePatientsStore } from '@/stores/patients'
import { parseISO, formatRelative, formatDuration, add, setDefaultOptions, differenceInMonths, format } from 'date-fns'
const emit = defineEmits(['update:toggle-active'])

const patientsStore = usePatientsStore()
const birthDate = computed(() => parseISO(patientsStore.item.birth_date))

const doseApplicationDate = computed(() => parseISO(props.dose.status.application_date))
const nextDoseApplicationDate = computed(() => parseISO(props.dose.status.next_dose_application_date))

const recommendedDate = ref(add(birthDate.value, { months: props.dose.maximum_recommended_age }))
const isCompleted = computed(() => props.dose.status && props.dose.status.completed)
const hasAlerts = computed(() => props.dose.alerts.length > 0)
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
