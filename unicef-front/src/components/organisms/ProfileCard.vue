<template>
  <div class="w-[30rem] rounded-xl border border-neutral-100 bg-gray-50">
    <div class="grid grid-cols-6 gap-y-2 p-5">
      <div>
        <img src="https://picsum.photos/seed/2/200/200" class="max-w-20 max-h-20 rounded-full" />
      </div>

      <div class="col-span-5 ml-4 md:col-span-4">
        <p class="font-bold text-gray-600 pr-2">{{ patientsStore.item.name }}</p>
        <div class="text-gray-400">
          <p>Gender: <span>{{ patientsStore.item.gender }}</span></p>
          <p>Document: <span>{{ patientsStore.item.id }}</span></p>
          <!--
          <p>
            Region: <span>{{ patientsStore.item.address[0].city }} / {{ patientsStore.item.address[0].state }}</span>
          </p>
          <p>
            Contact: <span>{{ patientsStore.item.telecom[0].value }}</span>
          </p>
          -->
          <p>
            Birth date: <span>{{ patientsStore.item.birth_date }}</span>
          </p>
          <p>
            Marital Status: <span>{{ patientsStore.item.marital_status }}</span>
          </p>
        </div>
      </div>
      <div class="col-start-2 ml-4 flex md:col-start-auto md:ml-0 md:justify-end">
        <p class="h-fit w-fit rounded-lg bg-sky-200 py-1 px-3 text-sm font-bold text-sky-600">Years: {{ differenceInYears(new Date(), birthDate) }}</p>
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

import { parseISO, differenceInYears } from 'date-fns'
import { usePatientsStore } from '@/stores/patients'
const patientsStore = usePatientsStore()

const router = useRouter()

const birthDate = computed(() => parseISO(patientsStore.item.birth_date) )

const props = defineProps({
  id: {
    type: String,
    default: '0',
  },
})
</script>
