<template>
  <section class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
    <h2 class="sr-only">Quick statistics</h2>

    <QuickStatisticsCard title="Pacientes em espera" result="12" class="bg-red-500">
      <template #icon="{ sizeClasses }">
        <UserGroupIcon aria-hidden="true" class="h-12 w-12 text-white" />
      </template>
    </QuickStatisticsCard>

    <QuickStatisticsCard title="Consultas em espera" result="20" class="bg-yellow-400">
      <template #icon="{ sizeClasses }">
        <CalendarIcon aria-hidden="true" class="h-12 w-12 text-white" />
      </template>
    </QuickStatisticsCard>

    <QuickStatisticsCard title="Consultas totais" result="32" class="bg-blue-500">
      <template #icon="{ sizeClasses }">
        <CalendarIcon aria-hidden="true" class="h-12 w-12 text-white" />
      </template>
    </QuickStatisticsCard>

    <QuickStatisticsCard title="Pacientes em espera" result="30" class="bg-purple-500">
      <template #icon="{ sizeClasses }">
        <BellIcon aria-hidden="true" class="h-12 w-12 text-white" />
      </template>
    </QuickStatisticsCard>
  </section>
</template>

<script setup>
import { UserGroupIcon, EyeIcon, ShoppingCartIcon, ChartPieIcon, CalendarIcon, BellIcon } from '@heroicons/vue/solid'
</script>
