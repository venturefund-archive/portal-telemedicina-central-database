<template>
  <div class="h-[888px] w-72 rounded-full bg-white p-6 shadow">
    <div class="-mt-16 flex justify-center">
      <img
        class="h-16 w-16 rounded-full border border-2 border-white bg-white object-cover"
        src="/avatar.png"
        alt="Profile picture"
      />
    </div>
    <div class="p-3 pt-12">
      <p class="text-sm font-semibold capitalize">{{ name }}</p>
    </div>
    <ul class="px-3 text-sm text-neutral-500">
      <li>
        <span class="font-semibold">{{ $t('patient-details.age') }}</span
        >: {{ age }}
      </li>
      <li>
        <span class="font-semibold">{{ $t('patient-details.date-of-birth') }}</span
        >: {{ format(birthDate, 'dd/MM/yyyy') }}
      </li>
      <li>
        <span class="font-semibold">{{ $t('patient-details.gender') }}</span
        >: {{ gender }}
      </li>
      <li>
        <span class="font-semibold">{{ $t('patient-details.region') }}</span
        >: {{ region }}
      </li>
      <li>
        <span class="font-semibold">{{ $t('patient-details.document') }}</span
        >: {{ postalCode }}
      </li>

      <p v-if="patientsStore.item.marital_status && patientsStore.item.marital_status.text">
        {{ $t('patient-details.civil-status') }} <span>{{ patientsStore.item.marital_status.text }}</span>
      </p>
    </ul>
    <div class="mt-4">
      <ul class="divide-y divide-gray-200 text-sm font-semibold">
        <li class="flex items-center py-4 opacity-50">
          <div class="mr-2 h-12 w-12 rounded-full border border-gray-200 bg-[#F8F9FB] p-2">
            <img class="mx-auto my-auto flex h-7 w-7" src="@/assets/images/profile-menu-01.png" />
          </div>
          <span class="pl-3">Peso, altura, IMC</span>
        </li>
        <li class="flex cursor-pointer items-center border-r-4 !border-r-blue-500 py-4 hover:bg-[#F8F9FB]">
          <div class="mr-2 h-12 w-12 rounded-full border border-gray-200 bg-[#F8F9FB] p-2">
            <img class="mx-auto my-auto flex h-7 w-7" src="@/assets/images/profile-menu-02.png" />
          </div>
          <span class="pl-3">{{ $t('patient-details.booklet') }}</span>
        </li>
        <li class="flex items-center py-4 opacity-50">
          <div class="mr-2 h-12 w-12 rounded-full border border-gray-200 bg-[#F8F9FB] p-2">
            <img class="mx-auto my-auto flex h-7 w-7" src="@/assets/images/profile-menu-03.png" />
          </div>
          <span class="pl-3">Período fetal</span>
        </li>
        <li class="flex items-center py-4 opacity-50">
          <div class="mr-2 h-12 w-12 rounded-full border border-gray-200 bg-[#F8F9FB] p-2">
            <img class="mx-auto my-auto flex h-7 w-7" src="@/assets/images/profile-menu-04.png" />
          </div>
          <span class="pl-3">Alergias</span>
        </li>
        <li class="flex items-center py-4 opacity-50">
          <div class="mr-2 h-12 w-12 rounded-full border border-gray-200 bg-[#F8F9FB] p-2">
            <img class="mx-auto my-auto flex h-7 w-7" src="@/assets/images/profile-menu-05.png" />
          </div>
          <span class="pl-3">Medicamentos</span>
        </li>
        <li class="flex items-center py-4 opacity-50">
          <div class="mr-2 h-12 w-12 rounded-full border border-gray-200 bg-[#F8F9FB] p-2">
            <img class="mx-auto my-auto flex h-7 w-7" src="@/assets/images/profile-menu-06.png" />
          </div>
          <span class="pl-3">Doenças</span>
        </li>
        <li class="flex items-center py-4 opacity-50">
          <div class="mr-2 h-12 w-12 rounded-full border border-gray-200 bg-[#F8F9FB] p-2">
            <img class="mx-auto my-auto flex h-7 w-7" src="@/assets/images/profile-menu-07.png" />
          </div>
          <span class="pl-3">Dados socioculturais</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
// import { HeartIcon, BookOpenIcon, UserIcon, EmojiSadIcon, PillIcon, VirusIcon, UsersIcon } from '@heroicons/vue/solid';
import { ref, onMounted, reactive, computed } from 'vue'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { MailIcon, LockClosedIcon, LoginIcon, UserIcon } from '@heroicons/vue/outline'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'
import { usePatientsStore } from '@/stores/patients'
import {
  parseISO,
  differenceInYears,
  setDefaultOptions,
  format,
  differenceInMonths,
  differenceInDays,
  addDays,
  addMonths,
} from 'date-fns'
import { useI18n } from 'vue3-i18n'
const { t } = useI18n()
const patientsStore = usePatientsStore()
const router = useRouter()

const name = ref(patientsStore.item.name.toLowerCase())
const gender = ref('male' == patientsStore.item.gender ? 'Masculino' : 'Feminino')
const region = ref(patientsStore.item.address[0].city + ' / ' + patientsStore.item.address[0].state)
const postalCode = ref(patientsStore.item.address[0].postal_code)

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
      if (1 == ageInDays) {
        return '1 ' + t('patient-details.day')
      }
      return ageInDays + ' ' + t('patient-details.days')
    }
    return ageInMonths + ' ' + t('patient-details.months')
  }
  return ageInYears + ' ' + t('patient-details.years')
})
const age = ref(formatedAge.value)

const props = defineProps({
  id: {
    type: String,
    default: '0',
  },
})
</script>
