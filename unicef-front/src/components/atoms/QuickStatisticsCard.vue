<template>
  <BaseCard :actions="actions" class="flex items-start">
    <template #header>
      <div class="flex pt-1">
        <slot name="icon" :sizeClasses="'w-8 h-8 text-blue-500'"> </slot>
      </div>
    </template>

    <div class="relative overflow-hidden pl-3">
      <div class="flex flex-col justify-between">
        <h4 class="text-3xl font-semibold text-white">{{ result }}</h4>
        <p class="text-base font-semibold text-white">{{ title }}</p>
      </div>
    </div>
  </BaseCard>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import ApexCharts from 'apexcharts'
import { ChartBarIcon, TrendingUpIcon, TrendingDownIcon, MinusIcon } from '@heroicons/vue/outline'

const chartEl = ref(null)

const props = defineProps({
  title: String,
  result: [String, Number],
  status: {
    type: String,
    default: 'success',
    validator(value) {
      return ['success', 'warning', 'danger'].includes(value)
    },
  },
  percentage: {
    type: [String, Number],
  },
  actions: {
    type: Array,
    default: [],
  },
  chartData: {
    type: [Array, Object],
    default: () => ({
      data: [],
      categories: [],
    }),
  },
})

onMounted(() => {
  let chart = new ApexCharts(chartEl.value, {
    series: [
      {
        name: props.title,
        data: props.chartData.data ?? props.chartData,
      },
    ],
    chart: {
      height: '100%',
      width: '100%',
      type: 'line',
      toolbar: {
        show: false,
      },
      sparkline: {
        enabled: true,
      },
    },
    stroke: {
      width: 2,
      curve: 'smooth',
    },
    grid: {
      show: false,
      padding: {
        left: 0,
        right: 0,
      },
      xaxis: {
        lines: {
          show: false,
        },
      },
      yaxis: {
        lines: {
          show: false,
        },
      },
    },
    xaxis: {
      type: 'datetime',
      categories: props.chartData.categories ?? [
        '1/11/2000',
        '2/11/2000',
        '3/11/2000',
        '4/11/2000',
        '5/11/2000',
        '6/11/2000',
        '7/11/2000',
        '8/11/2000',
        '9/11/2000',
        '10/11/2000',
        '11/11/2000',
        '12/11/2000',
        '1/11/2001',
      ],
      tickAmount: 10,
      labels: {
        show: false,
      },
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
    },
    title: {
      show: false,
    },
    fill: {
      type: 'gradient',
      gradient: {
        shade: 'dark',
        gradientToColors: ['#FDD835'],
        shadeIntensity: 1,
        type: 'horizontal',
        opacityFrom: 1,
        opacityTo: 1,
        stops: [0, 100, 100, 100],
      },
    },
    yaxis: {
      labels: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    tooltip: {
      x: { show: false },
    },
  })
  if (chartEl.value) {
    chart.render()
  }
})
</script>
