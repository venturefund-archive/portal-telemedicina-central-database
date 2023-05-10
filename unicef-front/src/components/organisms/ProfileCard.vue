<template>
  <div class="bg-white shadow rounded-full p-6 w-72 h-[888px]">
    <div class="flex justify-center -mt-16">
      <img class="rounded-full bg-white border border-2 border-white w-16 h-16 object-cover" src="/avatar.png" alt="Profile picture" />
    </div>
    <div class="pt-12 p-3">
      <p class="text-sm font-semibold capitalize">{{ name }}</p>
    </div>
    <ul class="text-neutral-500 px-3 text-sm">
      <li><span class="font-semibold">Idade</span>: {{ age }}</li>
      <li><span class="font-semibold">{{ $t('patient-details.date-of-birth') }}</span>: {{ format(birthDate, 'dd/MM/yyyy') }}</li>
      <li><span class="font-semibold">{{ $t('patient-details.gender') }}</span>: {{ gender }}</li>
      <li><span class="font-semibold">Região</span>: {{ region }}</li>
      <li><span class="font-semibold">CEP</span>: {{ postalCode }}</li>

      <p v-if="patientsStore.item.marital_status && patientsStore.item.marital_status.text">
        {{ $t('patient-details.civil-status') }} <span>{{ patientsStore.item.marital_status.text }}</span>
      </p>
    </ul>
    <div class="mt-4">
      <ul class="divide-y divide-gray-200 font-semibold text-sm">
        <li class="py-4 flex items-center hover:bg-[#F8F9FB] cursor-pointer">
          <div class="bg-[#F8F9FB] border border-gray-200  rounded-full w-12 h-12 p-2 mr-2">
            <img class=" w-7 h-7 flex mx-auto my-auto"  src="@/assets/images/profile-menu-01.png" />
          </div>
          <span class="pl-3">Peso, altura, IMC</span>
        </li>
        <li class="py-4 flex items-center hover:bg-[#F8F9FB] cursor-pointer border-r-4 !border-r-blue-500">
          <div class="bg-[#F8F9FB] border border-gray-200  rounded-full w-12 h-12 p-2 mr-2">
            <img class=" w-7 h-7 flex mx-auto my-auto"  src="@/assets/images/profile-menu-02.png" />
          </div>
          <span class="pl-3" >Cartilha de vacinas</span>
        </li>
        <li class="py-4 flex items-center hover:bg-[#F8F9FB] cursor-pointer">
          <div class="bg-[#F8F9FB] border border-gray-200  rounded-full w-12 h-12 p-2 mr-2">
            <img class=" w-7 h-7 flex mx-auto my-auto"  src="@/assets/images/profile-menu-03.png" />
          </div>
          <span class="pl-3">Período fetal</span>
        </li>
        <li class="py-4 flex items-center hover:bg-[#F8F9FB] cursor-pointer">
          <div class="bg-[#F8F9FB] border border-gray-200  rounded-full w-12 h-12 p-2 mr-2">
            <img class=" w-7 h-7 flex mx-auto my-auto"  src="@/assets/images/profile-menu-04.png" />
          </div>
          <span class="pl-3">Alergias</span>
        </li>
        <li class="py-4 flex items-center hover:bg-[#F8F9FB] cursor-pointer">
          <div class="bg-[#F8F9FB] border border-gray-200  rounded-full w-12 h-12 p-2 mr-2">
            <img class=" w-7 h-7 flex mx-auto my-auto" src="@/assets/images/profile-menu-05.png" />
          </div>
          <span class="pl-3">Medicamentos</span>
        </li>
        <li class="py-4 flex items-center hover:bg-[#F8F9FB] cursor-pointer">
          <div class="bg-[#F8F9FB] border border-gray-200  rounded-full w-12 h-12 p-2 mr-2">
            <img class=" w-7 h-7 flex mx-auto my-auto"  src="@/assets/images/profile-menu-06.png" />
          </div>
          <span class="pl-3">Doenças</span>
        </li>
        <li class="py-4 flex items-center hover:bg-[#F8F9FB] cursor-pointer">
          <div class="bg-[#F8F9FB] border border-gray-200  rounded-full w-12 h-12 p-2 mr-2">
            <img class=" w-7 h-7 flex mx-auto my-auto"  src="@/assets/images/profile-menu-07.png" />
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
const region = ref(patientsStore.item.address[0].city +' / '+ patientsStore.item.address[0].state)
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
