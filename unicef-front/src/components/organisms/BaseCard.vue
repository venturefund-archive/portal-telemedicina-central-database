<template>
  <div :class="['rounded-2xl py-5', bgClasses]">
    <!-- Card header -->
    <div v-if="!noHeader">
      <slot name="header">
        <div class="flex justify-between">
          <h4 class="text-lg font-medium">{{ title }}</h4>
          <form @submit.prevent="">
            <label for="default-search" class="sr-only mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">{{
              $t('dashboard.search')
            }}</label>
            <div class="relative">
              <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                <svg
                  class="h-5 w-5 text-neutral-500"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  ></path>
                </svg>
              </div>
              <InputIconWrapper>
                <template #icon>
                  <SearchIcon aria-hidden="true" class="h-5 w-5" />
                </template>
                <Input
                  @input="$emit('update:query', $event.target.value)"
                  :placeholder="$t('dashboard.search')"
                  withIcon
                  class="w-full rounded-full bg-white px-10 py-2.5 !shadow-md focus:shadow-none"
                />
              </InputIconWrapper>
            </div>
          </form>
        </div>
      </slot>
    </div>

    <!-- Card body -->
    <slot />
  </div>
</template>

<script setup>
import { SearchIcon } from '@heroicons/vue/outline'
import { DotsHorizontalIcon } from '@heroicons/vue/outline'
import { ref } from 'vue'

const props = defineProps({
  noHeader: {
    type: Boolean,
    default: false,
  },

  bgClasses: {
    type: String,
    default: 'bg-white',
  },

  title: String,
})

const localQuery = ref(props.query)
</script>
