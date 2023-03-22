<template>
    <div class="bg-white w-full md:w-1/2 h-full p-4 rounded float-right ga">
  <h2 class="font-bold text-lg mb-4">Pessoas em atraso</h2>
  <div class="flex items-center">
    <div class="flex gap-2">
      <button class="border border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white py-1 px-4 rounded-md text-sm">CPFS</button>
      <button class="border border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white py-1 px-4 rounded-md text-sm">Bairro</button>
    </div>
    <div class="mt-4 md:mt-0 flex items-center">
      <button @click="showList = !showList" class="relative z-10 flex flex-col items-center px-4 py-2 text-gray-500 bg-primary rounded-md">
        <UsersIcon title="População" class="h-6 w-6 text-blue-500"/>
        <span class="text-xs">População</span>
      </button>
      <ul v-if="showList" class="absolute z-20 rounded-md shadow-md bg-white mt-96">
        <li v-for="item in items" :class="{ 'font-bold': item === selectedItem }" class="px-4 py-2 font-normal cursor-pointer hover:bg-gray-100" :key="item" @click="">
          {{ item }}
        </li>
      </ul>
    </div>
  </div>


    <ul>
      <li v-for="person in peopleList" :key="person.id" class="flex justify-between items-center border-b-2 border-gray-200 py-2">
        <div class="flex-grow">
          <h3 class="font-bold text-base">{{ person.name }}</h3>
          <p class="text-xs">{{ person.birthday }}</p>
        </div>
        <button class="bg-blue-500 hover:bg-blue-600 text-white py-1 px-4 rounded-md text-sm">Details</button>
      </li>
    </ul>
  </div>

</template>

<script setup>
import { defineComponent, reactive, computed, onBeforeUpdate, onMounted, watch, ref, onUnmounted } from 'vue'
import { HandIcon, PencilIcon, UsersIcon, BellIcon, XIcon } from '@heroicons/vue/solid'
const isModalOpen = ref(false)
const selectedItem = ref(null)

const handleClickOutside = (event) => {
  if (!event.target.closest('.mt-4')) {
    showList.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
})

function onItemClick(item) {
  selectedItem.value = item;
  console.log(`Item clicado: ${item}`)
}

const showList = ref(false);
const items = ['Todos', 'Gestantes','Puérperas', 'Recém-nascidos', 'Primeira infância', 'Segunda infância', 'Terceira Infância','Adolescência'];

const asd = ref( {
      showList: false,
      items: ['Item 1', 'Item 2', 'Item 3'] // Substitua com o seu array de strings
  })

  const peopleList = [
    { id: 1, name: 'John Doe', birthday: 'Jan 1st, 1980' },
    { id: 2, name: 'Jane Smith', birthday: 'Feb 14th, 1995' },
    { id: 3, name: 'Bob Johnson', birthday: 'Dec 31st, 1975' },
  ];

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

@media (min-width: 768px) {
  .w-1\\/2 {
    width: 50%;
  }
}
</style>
