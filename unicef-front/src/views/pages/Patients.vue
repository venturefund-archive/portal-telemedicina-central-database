<template>
  <PageWrapper title="Patients">
  <section class="grid grid-cols-1 gap-6 lg:grid-cols-2">
    <h2 class="sr-only">Patients and Scale</h2>

    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-1">
      <BaseCard title="Patients on hold" :actions="[{ title: 'View', to: '#' }]">
        <div class="mt-4 flex items-center justify-between" v-for="i in 4" :key="i">
          <router-link :to="{ name: 'Patient', params:{id:i} }">
          <div class="flex items-center gap-2">
            <img class="h-10 w-10 rounded-md object-cover" src="https://placekitten.com/200/300" />
            <div>
              <h5 class="text-sm text-gray-600 dark:text-gray-300">Name</h5>
              <p class="text-sm text-gray-400 dark:text-gray-500">email@example.com</p>
            </div>
          </div>
        </router-link>
          <Button size="sm" iconOnly variant="secondary" v-slot="{ iconSizeClasses }">
            <DotsVerticalIcon aria-hidden="true" :class="iconSizeClasses" />
            <span class="sr-only">Actions</span>
          </Button>
        </div>
      </BaseCard>
    </div>

  </section>

  </PageWrapper>
</template>

<script setup>
import { DotsVerticalIcon, PlusCircleIcon, MinusCircleIcon } from '@heroicons/vue/outline'
</script>
