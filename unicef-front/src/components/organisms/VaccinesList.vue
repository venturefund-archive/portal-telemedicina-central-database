<template>
  <!-- component -->
  <div class="flex flex-col">
    <div class="overflow-x-auto sm:-mx-6 lg:-mx-8 px-3 py-2">
      <div class="inline-block min-w-full sm:px-6 lg:px-8">
        <div class="overflow-hidden">
          <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
            <table class="w-full text-left text-sm text-neutral-100 dark:text-neutral-100">
              <thead class="bg-neutral-200 text-xs uppercase text-white dark:text-white">
                <tr>
                  <th scope="col" colspan="2" class="bg-blue-200 px-6 py-4 text-center text-gray-900">Vacinas</th>
                  <th scope="col" colspan="9" class="bg-blue-300 px-6 py-4 text-center">
                    <span class="rounded-t-xl border border-transparent bg-neutral-500 p-2 font-semibold text-white"
                      >Meses</span
                    >
                  </th>
                  <th scope="col" colspan="4" class="bg-blue-400 px-6 py-4 text-center text-gray-900">
                    <span class="rounded-t-xl border border-transparent bg-neutral-500 p-2 font-semibold text-white"
                      >Anos</span
                    >
                  </th>
                </tr>
                <tr class="text-center">
                  <th scope="col" class="px-6 py-4 text-gray-900"></th>
                  <th scope="col" class="px-6 py-4 text-gray-900">
                    <span class="rounded-t-xl border border-transparent bg-neutral-500 p-2 font-semibold text-white"
                      >Ao nascer</span
                    >
                  </th>
                  <th scope="col" class="px-6 py-4 text-gray-900">2</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">3</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">4</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">5</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">6</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">7-11</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">12</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">15</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">18</th>
                  <!-- anos -->
                  <th scope="col" class="px-6 py-4 text-gray-900">4 a 6</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">10</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">11 a 12</th>
                  <th scope="col" class="px-6 py-4 text-gray-900">13 a 15</th>
                </tr>
              </thead>
              <tbody>
                <tr class="border-b hover:bg-neutral-300" v-for="(vaccine, k) in vaccines" :key="k">
                  <td colspan="2" class="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900 capitalize">{{ vaccine.name }}</td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm font-light text-gray-900"><VaccineAlert :status="Math.floor((Math.random() * 4) + 1)"/></td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm font-light text-gray-900"><VaccineAlert :status="Math.floor((Math.random() * 4) + 1)"/></td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm font-light text-gray-900"><VaccineAlert :status="Math.floor((Math.random() * 4) + 1)"/></td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm font-light text-gray-900"><VaccineAlert :status="Math.floor((Math.random() * 4) + 1)"/></td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm font-light text-gray-900"><VaccineAlert :status="Math.floor((Math.random() * 4) + 1)"/></td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm font-light text-gray-900"><VaccineAlert :status="Math.floor((Math.random() * 4) + 1)"/></td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm font-light text-gray-900"><VaccineAlert :status="Math.floor((Math.random() * 4) + 1)"/></td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm font-light text-gray-900"><VaccineAlert :status="Math.floor((Math.random() * 4) + 1)"/></td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm font-light text-gray-900"><VaccineAlert :status="Math.floor((Math.random() * 4) + 1)"/></td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm font-light text-gray-900"><VaccineAlert :status="Math.floor((Math.random() * 4) + 1)"/></td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm font-light text-gray-900"><VaccineAlert :status="Math.floor((Math.random() * 4) + 1)"/></td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm font-light text-gray-900"><VaccineAlert :status="Math.floor((Math.random() * 4) + 1)"/></td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm font-light text-gray-900"><VaccineAlert :status="Math.floor((Math.random() * 4) + 1)"/></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

<Teleport to="body"><Modal ref="modal" /></Teleport>

<button
    class="block rounded-lg bg-blue-700 px-5 py-2.5 text-center text-sm font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
    type="button"
    @click="openModal"
  >
    Toggle modal
  </button>

  </div>
</template>

<script setup>
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { MailIcon, LockClosedIcon, LoginIcon, UserIcon } from '@heroicons/vue/outline'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'
import { computed } from 'vue'

const modal = ref()
const router = useRouter()

const vaccines = reactive([
  { name: 'BCGID'},
  { name: 'Hepatite B'},
  { name: 'Tríplice bacteriana'},
  { name: '(DTPw ou DTPa)'},
  { name: 'Haemophilus'},
  { name: 'influenzae b'},
  { name: 'Poliomelite'},
  { name: 'Rotavírus'},
  { name: 'Pneumocócicas'},
  { name: 'Meningocócicas'},
  { name: 'Varicela'},
  { name: 'Influenza'},
  { name: 'Poliomelite oral'},
  { name: 'Febre amarela'},
  { name: 'Hepatite A'},
  { name: 'Tríplice viral'},
  { name: 'Covid'},
  { name: 'HPV'},
  { name: 'Tríplice bacteraina acelular'},
])
const profileForm = reactive({
  // blood_type
  // document
  // age
  name: '',
  phone: '(00) 00 000-000',
  state: '',
  city: '',
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

const addDose = () => {
  return console.log('dose adicionada')
}

onMounted(() => {
  profile()
})
</script>
