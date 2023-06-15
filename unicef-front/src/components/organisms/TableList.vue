<template>
  <div class="overflow-hidden rounded rounded-b-2xl text-sm shadow" style="min-height: 793px">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-white">
        <tr>
          <th scope="col" class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-600">
            {{$t('manager.group')}}
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-600">
            {{$t('manager.quantity')}}
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-600">
            {{$t('manager.team')}}
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-600">
            {{$t('manager.area')}}
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-600">
            {{$t('manager.street')}}
          </th>
        </tr>
      </thead>
      <tbody class="bg-white">
        <tr
          v-for="(user, index) in users"
          :key="index"
          class="hover:bg-gray-100"
          :class="index % 2 == 1 ? 'bg-[#F9FAFB]' : 'bg-white'"
        >
          <td class="whitespace-nowrap px-6 py-4 font-semibold" v-if="index === users.length - 1">
            {{ user.group }}
          </td>
          <td class="whitespace-nowrap px-6 py-4 font-semibold" v-else>{{ user.group }}</td>
          <td class="whitespace-nowrap px-6 py-4 text-gray-500">{{ user.qtd }}</td>
          <td class="whitespace-nowrap px-6 py-4 text-gray-500">{{ user.team }}</td>
          <td class="whitespace-nowrap px-6 py-4 text-gray-500">{{ user.area }}</td>
          <td class="whitespace-nowrap px-6 py-4 text-gray-500" v-if="index === users.length - 1">
            {{ user.street }}
          </td>
          <td class="whitespace-nowrap px-6 py-4 text-gray-500" v-else>{{ user.street }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { faStreetView } from '@fortawesome/free-solid-svg-icons'
import { ref, computed } from 'vue'
import { useI18n } from 'vue3-i18n'
const { t } = useI18n()
const users = computed(() => [
  {
    group: t('manager.diabetic'),
    qtd: '20',
    team: '02-Integração',
    area: '15',
    street: t('manager.street'),
  },
  {
    group: t('manager.pregnant'),
    qtd: '50',
    team: '03-Riviera',
    area: '10',
    street: t('manager.street'),
  },
  {
    group: t('manager.diabetic'),
    qtd: '10',
    team: '02-Miami',
    area: '12',
    street: t('manager.street'),
  },
  {
    group: t('manager.elderly'),
    qtd: '60',
    team: '02-Integração',
    area: '01',
    street: t('manager.street'),
  },
  {
    group: t('manager.lessone'),
    qtd: '20',
    team: '02-Integração',
    area: '05',
    street: t('manager.street'),
  },
  {
    group: t('manager.lessfive'),
    qtd: '20',
    team: '02-Integração',
    area: '19',
    street: t('manager.street'),
  },
  {
    group: t('manager.diabetic'),
    qtd: '20',
    team: '02-Integração',
    area: '15',
    street: t('manager.street'),
  },
  // adicione mais usuários aqui
])
</script>
