<template>
  <div class="relative flex justify-end px-5" style="position: absolute; top: 10%; right: 0; width: 200px">
    <button
      @click="isModalOpen = true"
      class="relative z-10 flex h-12 w-12 items-center justify-center rounded-full bg-red-500 hover:bg-red-600"
    >
      <BellIcon title="População" class="h-8 w-8 text-white hover:text-gray-50" />
    </button>
    <transition name="slide-in">
      <div v-if="isModalOpen" class="fixed inset-0 z-50 overflow-y-auto">
        <div class="flex h-screen">
          <div
            class="fixed relative top-0 left-1/2 z-50 mx-auto flex h-full w-1/2 max-w-md -translate-x-1/2 transform flex-col rounded-md bg-white p-6 shadow-lg"
          >
            <button @click="isModalOpen = false" class="absolute top-2 right-2 text-gray-500">
              <XIcon class="h-6 w-6 cursor-pointer hover:text-blue-500" />
            </button>
            <h2 class="mb-4 text-xl font-semibold">Alertas</h2>
            <div class="flex w-full">
              <label for="default-search" class="sr-only text-sm font-medium text-gray-900">Procurar</label>
              <div class="relative flex w-full items-center p-2">
                <svg
                  class="absolute left-3 h-5 w-5 text-gray-500 dark:text-gray-400"
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
                <input
                  v-model="searchQuery"
                  placeholder="Pesquisar"
                  class="mr-1 w-full rounded-md bg-neutral-100 py-3 px-7 focus:border-blue-500 focus:ring-blue-500"
                />
              </div>
            </div>
            <ul class="divide-y divide-gray-200">
              <li v-for="city in filteredCities" :key="city.name" class="flex items-center justify-between py-3">
                <div>
                  <h3 class="mb-1 font-bold">{{ city.name }}</h3>
                  <p class="text-xs text-neutral-500">{{ city.age }}</p>
                </div>
                <button
                  @click="showDetails(city)"
                  class="cursor-pointer rounded bg-red-500 py-2 px-2 text-sm font-semibold text-white hover:bg-red-700"
                >
                  Notificar
                </button>
              </li>
            </ul>
          </div>
        </div>
        <div class="fixed inset-0 z-40 bg-gray-900 bg-opacity-25" @click="isModalOpen = false"></div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { defineComponent, reactive, computed, onBeforeUpdate, onMounted, watch, ref } from 'vue'
import { HandIcon, PencilIcon, UsersIcon, BellIcon, XIcon } from '@heroicons/vue/solid'
const isModalOpen = ref(false)
const searchQuery = ref('')

const cities = [
  { name: 'Bela Vista', age: 'Baixa proporção de gestantes com realização de exames para sífilis e HIV' },
  { name: 'Bom Retiro', age: 'Baixa proporção do fechamento de ciclo vacinal dos 2 meses' },
  { name: 'Santa Cecília', age: 'Baixa proporção de fechamento do ciclo vacinal 4 anos ' },
  { name: 'Aricanduva', age: 'Baixa proporção de gestantes com realização de exames para sífilis e HIV' },
  { name: 'Artur Alvim', age: 'Baixa proporção do fechamento de ciclo vacinal dos 2 meses' },
  { name: 'Brás', age: 'Baixa proporção de fechamento do ciclo vacinal 4 anos' },
  { name: 'Gangaíba', age: 'Baixa proporção de gestantes com realização de exames para sífilis e HIV' },
  { name: 'Carrão', age: 'Baixa proporção de fechamento do ciclo vacinal 4 anos' },
  { name: 'Ermilio Matarazzo', age: 'Baixa proporção de fechamento do ciclo vacinal 4 anos' },
]
const filteredCities = computed(() => {
  if (!searchQuery.value) {
    return cities
  }
  const normalizedSearch = searchQuery.value.trim().toLowerCase()
  return cities.filter((city) => {
    const normalizedCity = city.name.toLowerCase()
    return normalizedCity.includes(normalizedSearch)
  })
})
</script>

<style>
.container {
  padding: 5px;
}

.list {
  background-color: white;
  border-radius: 5px;
  padding: 5px;
}

.list-item {
  cursor: pointer;
}

.edit-panel {
  position: fixed;
  left: 50%;
  top: 0;
  width: 380px;
  margin: 150px 0 0 -190px; /* Apply negative top and left margins to center the element */
}
.slide-in-enter-active,
.slide-in-leave-active {
  transition: all 0.3s ease;
}

.slide-in-enter,
.slide-in-leave-to {
  transform: translateX(100%);
}
</style>
