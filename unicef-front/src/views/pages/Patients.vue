<template>
  <PageWrapper title="Patients">
    {{isOpen}}
         <ProfileCard :id="patientId" class="pb-2" />
        <VaccinesList class="py-2" birth_date="2012-06-10" />
  </PageWrapper>
</template>

}
<script setup>
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import { DotsVerticalIcon, PlusCircleIcon, MinusCircleIcon } from '@heroicons/vue/outline'
import {
    Dialog,
    DialogPanel,
    DialogTitle,
    DialogDescription,
  } from '@headlessui/vue'

const props = defineProps({
  patientId: {
    type: String,
    default: '0',
  },
})
// const isOpen = ref(true)

function setIsOpen(value) {
  console.log('hit')
  isOpen.value = value
}
</script>
