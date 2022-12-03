<template>
  <div class="w-[30rem] rounded-xl border border-neutral-100 bg-gray-50">
    <div class="flex justify-between p-5">
      <div>
        <img src="https://picsum.photos/seed/2/200/200" class="max-w-20 max-h-20 rounded-full" />
      </div>
      <div class="ml-4">
        <p class="cursor-pointer font-bold text-gray-600 hover:underline">#{{ profileForm.id }} - {{ profileForm.name.join() }}</p>
        <div class="text-gray-400">
          <p>Blood Type: <span class="cursor-pointer hover:underline">B+</span></p>
          <p>Gender: <span class="cursor-pointer hover:underline">{{ profileForm.gender }}</span></p>
          <p>Marital Status: <span class="cursor-pointer hover:underline">{{ profileForm.marital_status }}</span></p>
          <p>
            Region: <span class="cursor-pointer hover:underline">{{ profileForm.address[0].city }} / {{ profileForm.address[0].state }}</span>
            <span class="cursor-pointer hover:underline">{{ profileForm.address[0].postalCode }}</span>
          </p>
          <p>{{ profileForm.telecom.system }}: <span class="cursor-pointer hover:underline">{{ profileForm.telecom.value }}</span></p>
        </div>
      </div>
      <div class="">
        <p class="rounded-lg bg-sky-200 py-1 px-3 text-sm font-bold text-sky-600">Age: 06</p>
      </div>
    </div>
  </div>

</template>

<script setup>
import { onMounted, reactive } from 'vue'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { MailIcon, LockClosedIcon, LoginIcon, UserIcon } from '@heroicons/vue/outline'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'

const router = useRouter()

const profileForm = reactive({
  id: "4172",
  name: [
    'Asd Qwe Zxc'
  ],
  telecom: {
    system: 'phone',
    value: '555-385-9019',
    use: 'home'
  },
  gender: 'male',
  birth_date: '2012-06-10',
  address: [
    {
      line:[
        '370 Auer Knoll'
      ],
      postal_code: '02476',
      postalCode: '02476',
      city: 'Arlington',
      state: 'MA',
      country: 'US'
    }
  ],
  marital_status: 'Never Married',

  processing: false,
})

const profile = async () => {
  const state = useStorage('app-store', { token: '' })
  try {
    // const patient_id = 4172
    // const response = await axios.post(import.meta.env.VITE_AUTH_API_URL + `patients/${patient_id}`, profileForm)
  } catch (err) {
    errorToast({ text: err.message })
  }
}

onMounted( async () => {
  await profile()
})
</script>
