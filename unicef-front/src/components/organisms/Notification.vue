<template>
        <div class="relative flex justify-end">
  <button @click="isModalOpen = true" class="relative z-10 flex items-center justify-center w-12 h-12 rounded-full bg-red-500 hover:bg-red-600">
    <BellIcon title="População" class="h-8 w-8 text-white hover:text-gray-50" />
  </button>
  <transition name="slide-in">
  <div v-if="isModalOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-end h-screen/2">
      <div class="fixed top-0 left-1/2 transform -translate-x-1/2 h-full w-1/2 flex justify-center flex-col p-6 max-w-md mx-auto relative bg-white rounded-md shadow-lg z-50">
        <button @click="isModalOpen = false" class="absolute top-2 right-2 text-gray-500">
          <XIcon class="h-6 w-6"/>
        </button>
        <h2 class="text-xl font-semibold mb-4">Alertas</h2>
        <input type="text" v-model="searchQuery" placeholder="Pesquisar" class="border border-gray-300 rounded-md px-3 py-2 w-full mb-4"/>
        <ul class="divide-y divide-gray-200">
          <li v-for="city in filteredCities" :key="city.name" class="py-3">
            <h3 class="font-bold mb-1">{{ city.name }}</h3>
            <p class="text-sm">{{ city.age }} years old</p>
          </li>
        </ul>
      </div>
    </div>
    <div class="fixed inset-0 z-40 bg-gray-900 bg-opacity-10 backdrop-blur"></div>
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
  { name: 'São Paulo', age: 467 },
  { name: 'Rio de Janeiro', age: 456 },
  { name: 'Belo Horizonte', age: 124 },
  { name: 'Brasília', age: 61 },
  { name: 'Salvador', age: 472 }
]
const filteredCities = computed(() => {
  if (!searchQuery.value) {
    return cities
  }
  const normalizedSearch = searchQuery.value.trim().toLowerCase()
  return cities.filter(city => {
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
