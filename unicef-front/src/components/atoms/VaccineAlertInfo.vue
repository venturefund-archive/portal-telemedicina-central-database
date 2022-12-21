<template>
    <div class="font-normal text-lg min-w-96">
        <div class="relative bg-neutral-50 p-4">
            <div class="flex justify-between py-1">
                <p class="font-semibold px-1">{{ props.vaccine.description }}</p>
                <div v-if="dose.is_completed">
                    <CheckCircleIcon class="bg-lime-600 text-white h-7 w-7 rounded-full"></CheckCircleIcon>
                </div>
                <div class="py-1" v-if="!dose.is_completed">
                    <ExclamationCircleIcon class="bg-red-500 text-white h-7 w-7 rounded-full"></ExclamationCircleIcon>
                </div>
            </div>

            <p class="">Dose <span class="font-semibold">#{{ props.dose.dose_order }} </span></p>
            Age: {{ props.dose.maximum_recommended_age }} <br />
            gender: {{ props.dose.gender_recommendation }}<br />
        </div>
        <div class="bg-neutral-200 p-4 font-normal">
            <p class="font-semibold">Alerts</p>
            <div v-for="(alert, k) in props.dose.alerts" :key="k">
                Id: {{ alert.id }} <br />
                Alert type: {{ alert.alert_type }}<br />
                created at: {{ alert.created_at }}
            </div>
            Total alerts: {{ props.dose.alerts.length }}
        </div>
    </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import PerfectScrollbar from 'perfect-scrollbar'
import { CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/vue/outline';

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
