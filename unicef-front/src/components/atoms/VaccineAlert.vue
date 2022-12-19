<template>
<!-- @click="setIsOpen(!isOpen)" -->
  <div class="hover:scale-125">
    <div v-if="1 == status" class="w-9 h-9 bg-sky-500 border border-tranparent shadow-md rounded-full"></div>

    <span v-else-if="2 == status"
          class="flex h-9 w-9">
        <span class="animate-ping absolute inline-flex h-9 w-9 rounded-full bg-red-500 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-9 w-9 bg-red-500"></span>
    </span>

    <div v-else-if="3 == status" class="w-9 h-9 bg-red-500 border border-tranparent shadow-md rounded-full"></div>
    <div v-else-if="4 == status" class="w-9 h-9 bg-neutral-200 border border-tranparent shadow-md rounded-full"></div>
    <div v-else class=""></div>
  </div>

</template>


<script setup>
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import InputIconWrapper from '@/components/InputIconWrapper.vue'
import { MailIcon, LockClosedIcon, LoginIcon, UserIcon } from '@heroicons/vue/outline'
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { errorToast, successToast } from '@/toast'
import { computed } from 'vue'
const router = useRouter()
const emit = defineEmits(['click'])

const props = defineProps({
  status: {
    type: Number,
    default: 0,
    validator(value) {
      return [0, 1, 2, 3, 4].includes(value)
    },
  },
})
</script>
