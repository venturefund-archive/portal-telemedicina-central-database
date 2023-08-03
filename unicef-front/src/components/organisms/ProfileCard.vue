<template>
  <div class="h-[888px] w-72 rounded-full bg-white shadow">
    <div class="flex justify-center">
      <img
        class="-mt-7 h-20 w-20 rounded-full border border-2 border-white bg-white object-cover"
        src="/avatar.png"
        alt="Profile picture"
      />
    </div>
    <div class="p-3 pt-14 group">
      <p class="text-sm font-semibold capitalize">{{ name }}</p>
      <div class="flex justify-center relative">
        <div ref="qrcode" class="absolute z-50 -top-48 p-2 border drop-shadow-lg rounded bg-white hidden group-hover:block"></div>
      </div>

      <div class="flex justify-center">
        <span class="text-sm text-neutral-400 cursor-pointer" @click="copiarTexto">
          <span v-if="showTooltip" class="absolute font-normal transition-opacity text-gray-700  px-2 py-1 bg-gray-400 bg-opacity-60 rounded-lg" :class="{ 'opacity-0': !showTooltip, 'opacity-100': showTooltip }">Copiado com sucesso!</span>
          <span class="truncate">{{ id }}</span>
        </span>
      </div>
    </div>
    <ul class="px-3 text-sm text-neutral-500">
      <li>
        <span class="font-semibold">{{ $t('patient-details.age') }}</span
        >: {{ formatedAge }}
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

      <li v-if="patientsStore.item.marital_status && patientsStore.item.marital_status.text">
        {{ $t('patient-details.civil-status') }} <span>{{ patientsStore.item.marital_status.text }}</span>
      </li>
    </ul>
    <div class="mt-4">
      <ul class="divide-y divide-gray-100 text-sm font-semibold">
        <li class=""></li>
        <Tooltip variant="gray" position="right">
          <template #trigger>
            <li class="flex items-center bg-white py-4 pl-4 font-normal opacity-50">
              <div class="mr-2 h-12 w-12 rounded-full border border-gray-100 bg-[#F8F9FB] p-2">
                <img class="mx-auto my-auto flex h-7 w-7" src="@/assets/images/profile-menu-01.png" />
              </div>
              <span class="pl-3">{{ $t('patient-details.imc') }}</span>
            </li>
          </template>
          <template #content>
            <div class="flex text-gray-700 font-normalP">{{ $t('patient-details.comming-soon') }}</div>
          </template>
        </Tooltip>
        <li class="flex cursor-pointer items-center border-r-4 !border-r-blue-500 py-4 pl-4 hover:bg-[#F8F9FB]">
          <div class="mr-2 h-12 w-12 rounded-full border border-gray-100 bg-[#F8F9FB] p-2">
            <img class="mx-auto my-auto flex h-7 w-7" src="@/assets/images/profile-menu-02.png" />
          </div>
          <span class="pl-3">{{ $t('patient-details.booklet') }}</span>
        </li>
        <Tooltip variant="gray" position="right">
          <template #trigger>
            <li class="flex items-center bg-white py-4 pl-4 font-normal opacity-50">
              <div class="mr-2 h-12 w-12 rounded-full border border-gray-100 bg-[#F8F9FB] p-2">
                <img class="mx-auto my-auto flex h-7 w-7" src="@/assets/images/profile-menu-03.png" />
              </div>
              <span
                data-tooltip-target="tooltip-default"
                type="button"
                class="-my-1 rounded-lg text-left text-sm font-normal"
              >
                <span class="pl-3">{{ $t('patient-details.fetal-period') }}</span>
              </span>
            </li>
          </template>
          <template #content>
            <div class="flex text-gray-700 font-normalP justify-center">{{ $t('patient-details.comming-soon') }}</div>
          </template>
        </Tooltip>
        <Tooltip variant="gray" position="right">
          <template #trigger>
            <li class="flex items-center bg-white py-4 pl-4 font-normal opacity-50">
              <div class="mr-2 h-12 w-12 rounded-full border border-gray-100 bg-[#F8F9FB] p-2">
                <img class="mx-auto my-auto flex h-7 w-7" src="@/assets/images/profile-menu-04.png" />
              </div>
              <span class="pl-3">{{ $t('patient-details.allergie') }}</span>
            </li>
          </template>
          <template #content>
            <div class="flex text-gray-700 font-normalP justify-center">{{ $t('patient-details.comming-soon') }}</div>
          </template>
        </Tooltip>
        <Tooltip variant="gray" position="right">
          <template #trigger>
            <li class="flex items-center bg-white py-4 pl-4 font-normal opacity-50">
              <div class="mr-2 h-12 w-12 rounded-full border border-gray-100 bg-[#F8F9FB] p-2">
                <img class="mx-auto my-auto flex h-7 w-7" src="@/assets/images/profile-menu-05.png" />
              </div>
              <span class="pl-3">{{ $t('patient-details.medication') }}</span>
            </li>
          </template>
          <template #content>
            <div class="flex text-gray-700 font-normalP justify-center">{{ $t('patient-details.comming-soon') }}</div>
          </template>
        </Tooltip>
        <Tooltip variant="gray" position="right">
          <template #trigger>
            <li class="flex items-center bg-white py-4 pl-4 font-normal opacity-50">
              <div class="mr-2 h-12 w-12 rounded-full border border-gray-100 bg-[#F8F9FB] p-2">
                <img class="mx-auto my-auto flex h-7 w-7" src="@/assets/images/profile-menu-06.png" />
              </div>
              <span class="pl-3">{{ $t('patient-details.desease') }}</span>
            </li>
          </template>
          <template #content>
            <div class="flex text-gray-700 font-normalP justify-center">{{ $t('patient-details.comming-soon') }}</div>
          </template>
        </Tooltip>
        <Tooltip variant="gray" position="right">
          <template #trigger>
            <li class="flex items-center rounded rounded-b-full bg-white py-4 pl-4 font-normal opacity-50">
              <div class="mr-2 h-12 w-12 rounded-full border border-gray-100 bg-[#F8F9FB] p-2">
                <img class="mx-auto my-auto flex h-7 w-7" src="@/assets/images/profile-menu-07.png" />
              </div>
              <span class="pl-3">{{ $t('patient-details.social-data') }}</span>
            </li>
          </template>
          <template #content>
            <div class="flex text-gray-700 font-normalP justify-center">{{ $t('patient-details.comming-soon') }}</div>
          </template>
        </Tooltip>
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
import QRCode from 'easyqrcodejs';

const { t } = useI18n()
const patientsStore = usePatientsStore()
const router = useRouter()

const name = ref(patientsStore.item.name.toLowerCase())
const gender = computed(() =>
  'male' == patientsStore.item.gender ? t('patient-details.male') : t('patient-details.female')
)
const region = ref(patientsStore.item.address.city + ' / ' + patientsStore.item.address.state)
const postalCode = ref(patientsStore.item.address.postal_code)

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

const props = defineProps({
  id: {
    type: String,
    default: '0',
  },
})
const showTooltip = ref(false);

const copiarTexto = () => {
  const areaDeTransferencia = document.createElement('textarea');
  areaDeTransferencia.value = props.id;
  document.body.appendChild(areaDeTransferencia);
  areaDeTransferencia.select();
  document.execCommand('copy');
  document.body.removeChild(areaDeTransferencia);

  showTooltip.value = true;

  // Esconder o tooltip após 2 segundos (2000ms)
  setTimeout(() => {
    showTooltip.value = false;
  }, 999);
};

const qrcodeUrl = ref(`${window.location.protocol}//${window.location.host}/patients/${patientsStore.item.id}`);
let qrcode = ref(null);

onMounted(() => {
  new QRCode(qrcode.value, {
    text: qrcodeUrl.value,
    width: 96,
    height: 96,
    colorDark: "#000000",
    colorLight: "#ffffff",
    correctLevel: QRCode.CorrectLevel.H
  });
});
</script>
<style>
@keyframes fadeInOut {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  50% {
    opacity: 1;
    transform: translateY(0);
  }
  100% {
    opacity: 0;
    transform: translateY(-20px);
  }
}

.animate-tooltip {
  animation: fadeInOut 2s ease-in-out;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

</style>
