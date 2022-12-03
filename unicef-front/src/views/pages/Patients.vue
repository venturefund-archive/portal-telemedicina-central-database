<template>
  <PageWrapper title="Patients">
    <div class="flex">

      <div class="px-5">
        <ProfileCard :id="patientId" class="pb-2" />
        <VaccinesList class="py-2" />
      </div>
    </div>
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
  // blood_type
  // document
  // age
  patientId: {
    type: String,
    default: '0',
  },
})
// const isOpen = ref(true)

</script>
