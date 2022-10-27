<template>
  <div :class="['rounded-md p-3 shadow-md', bgClasses]">
    <!-- Card header -->
    <div class="" v-if="!noHeader">
      <slot name="header">
        <div class="flex justify-between">
          <h4 class="text-lg font-medium">{{ title }}</h4>
          <form>
            <label for="default-search" class="sr-only mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >Search</label
            >
            <div class="relative">
              <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                <svg
                  class="h-5 w-5 text-gray-500 dark:text-gray-400"
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
              <input
                type="search"
                class="block w-full rounded-lg border border-transparent bg-gray-50 p-4 pl-10 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
                placeholder="Search"
                required
              />
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
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import { DotsHorizontalIcon } from '@heroicons/vue/outline'

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
</script>
