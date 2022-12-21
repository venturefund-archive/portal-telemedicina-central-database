<template>
    <div class="relative bg-gray-200 p-4">
        <div class="flex justify-between">
        <p class="font-normal">Vaccines</p>  <div v-if="dose.is_completed">
         <CheckIcon class="bg-green-500 text-white h-5 w-5 rounded-full"></CheckIcon>
        </div>
    </div>
        Name: {{ props.vaccine.description }}<br />
        Recomended age: {{ props.dose.maximum_recommended_age }} <br />
        gender: {{ props.dose.gender_recommendation }}<br />
    </div>
    <div class="bg-gray-300 p-4">
        <div v-for="(alert, k) in props.dose.alerts" :key="k">
            <p class="font-normal">Alerts</p>
            Id: {{ alert.id }} <br />
            Alert type: {{ alert.alert_type }}<br />
            created at: {{ alert.created_at }}
        </div>
        Total alerts: {{ props.dose.alerts.length }}
    </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import PerfectScrollbar from 'perfect-scrollbar'
import { CheckIcon } from '@heroicons/vue/outline';

const props = defineProps({
    vaccine: {
        type: Object,
        default: {},
    },
    dose: {
        type: Object,
        default: {},
    },
})
</script>
