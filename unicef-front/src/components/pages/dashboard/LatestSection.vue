<template>
  <section class="grid grid-cols-1 gap-6 lg:grid-cols-2">
    <h2 class="sr-only">Pacientes e escala</h2>

    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-1">
      <BaseCard title="Pacientes em espera" :actions="[{ title: 'View', to: '#' }]">
        <div class="mt-4 flex items-center justify-between" v-for="i in 4" :key="i">
          <div class="flex items-center gap-2">
            <img class="h-10 w-10 rounded-md object-cover" src="https://placekitten.com/200/300" />
            <div>
              <h5 class="text-sm text-gray-600 dark:text-gray-300">Name</h5>
              <p class="text-sm text-gray-400 dark:text-gray-500">email@example.com</p>
            </div>
          </div>
          <Button size="sm" iconOnly variant="secondary" v-slot="{ iconSizeClasses }">
            <DotsVerticalIcon aria-hidden="true" :class="iconSizeClasses" />
            <span class="sr-only">Ações</span>
          </Button>
        </div>
      </BaseCard>
    </div>

    <BaseCard title="Escala do dia">
      <div class="mt-4 flex items-center justify-between" v-for="i in 4" :key="i">
        <div class="flex items-center gap-2">
          <div>
            <h5 class="text-sm text-gray-600 dark:text-gray-300">10:30</h5>
            <p class="text-sm text-gray-400 dark:text-gray-500">20 Mar 2020</p>
          </div>
        </div>
      </div>
    </BaseCard>
  </section>
</template>

<script setup>
import { DotsVerticalIcon, PlusCircleIcon, MinusCircleIcon } from '@heroicons/vue/outline'
</script>
