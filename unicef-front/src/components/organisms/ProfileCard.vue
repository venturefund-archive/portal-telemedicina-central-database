<template>
  <div class="rounded-xl border border-neutral-100 bg-gray-50 lg:w-[38rem]">
    <div class="grid grid-cols-6 gap-y-2 p-5">
      <div>
        <img src="/avatar.png" class="max-w-20 max-h-20 rounded-full bg-neutral-200 p-1" />
      </div>

      <div class="col-span-5 ml-4 md:col-span-4 tracking-wide">
        <p class="pr-2 font-bold capitalize text-gray-600">{{ patientsStore.item.name.join().toLowerCase() }}</p>
        <div class="text-gray-400">
          <p>
            {{ $t('patient-details.genre') }} <span>{{ 'male' == patientsStore.item.gender ? 'Masculino' : 'Feminino' }}</span>
          </p>
          <!--
          <p>
            Region: <span>{{ patientsStore.item.address[0].city }} / {{ patientsStore.item.address[0].state }}</span>
          </p>
          <p>
            Contact: <span>{{ patientsStore.item.telecom[0].value }}</span>
          </p>
          -->
          <p>
            {{ $t('patient-details.date-of-birth') }} <span>{{ format(birthDate, 'dd/MM/yyyy') }}</span>
          </p>
          <p v-if="patientsStore.item.marital_status && patientsStore.item.marital_status.text">
            {{ $t('patient-details.civil-status') }} <span>{{ patientsStore.item.marital_status.text }}</span>
          </p>
        </div>
      </div>
      <div class="col-start-2 ml-4 flex md:col-start-auto md:ml-0 md:justify-end">
        <p class="h-fit rounded-lg bg-sky-200 py-1 px-3 text-sm font-bold text-sky-600 lowercase">
          {{ formatedAge }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, computed } from 'vue'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { MailIcon, LockClosedIcon, LoginIcon, UserIcon } from '@heroicons/vue/outline'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'
import { usePatientsStore } from '@/stores/patients'
import { parseISO, differenceInYears, setDefaultOptions, format, differenceInMonths, differenceInDays, addDays, addMonths } from 'date-fns'
import { useI18n } from "vue3-i18n";
const { t } = useI18n()
const patientsStore = usePatientsStore()
const router = useRouter()

const birthDate = computed(() => parseISO(patientsStore.item.birth_date))

const formatedAge = computed(() => {
  const ageInYears = differenceInYears(new Date(), birthDate.value)
  if (1 == ageInYears) {
    return '1 ' + t('patient-details.year')
  } else if (0 == ageInYears) {
    const ageInMonths = differenceInMonths(new Date(), birthDate.value)
    const ageInDays = differenceInDays(new Date(), birthDate.value)
    if (1 == ageInMonths) {
      return '1 ' + t('patient-details.month')
    } else if (0 == ageInMonths) {
      if (1 == ageInDays){
        return '1 ' + t('patient-details.day')
      }
      return ageInDays + ' ' + t('patient-details.day') + 's'
    }
    return ageInMonths + ' ' + t('patient-details.month') + 's'
  }
  return ageInYears + ' ' + t('patient-details.year') + 's'
})

const props = defineProps({
  id: {
    type: String,
    default: '0',
  },
})
</script>
