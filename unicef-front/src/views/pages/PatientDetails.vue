<template>
  <PageWrapper title="Patient Details">
    <div v-if="patientsStore.item">
      <ProfileCard :id="id" class="pb-2" />
      <VaccinesList class="py-2" />
    </div>
  </PageWrapper>
</template>

}
<script setup>
import { onMounted, onUpdated, reactive, ref } from 'vue'
import { DotsVerticalIcon, PlusCircleIcon, MinusCircleIcon } from '@heroicons/vue/outline'
import {
    Dialog,
    DialogPanel,
    DialogTitle,
    DialogDescription,
  } from '@headlessui/vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'
import { watch, computed } from 'vue'
import { usePatientsStore } from '@/stores/patients'
const patientsStore = usePatientsStore()


const props = defineProps({
  id: {
    type: String,
    default: '0',
  },
})

onMounted(async () => {
  if (props.id != 0)
    await patientsStore.fetchPatient(props.id)
})
onUpdated(async () => {
  if (props.id != 0)
    await patientsStore.fetchPatient(props.id)
})


function setIsOpen(value) {
  console.log('hit')
  isOpen.value = value
}
</script>
