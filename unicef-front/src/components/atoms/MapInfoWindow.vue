<template>
  <div class="p-3">
    <form>
    <InputIconWrapper>
      <template #icon>
        <TagIcon aria-hidden="true" class="h-5 w-5" />
      </template>
      <Input
        placeholder="Nome do poligono"
        v-model="state.polygonNames[props.polygonIndex]"
        withIcon
        class="mb-3 block w-full rounded-lg border border-transparent bg-gray-50 p-4 pl-10 text-sm text-gray-900"
      />
    </InputIconWrapper>
    <Button class="mx-3"  type="button" variant="danger" @click="$emit('delete')">
      <HandIcon aria-hidden="true" />
      <span>Excluir</span>
    </Button>
    <Button type="submit" variant="success-outline" @click="$emit('saved', { polygonName: state.polygonNames[props.polygonIndex], polygonIndex})" class="mx-3">
      <PencilIcon aria-hidden="true" />
      <span>Salvar</span>
    </Button>
  </form>
  </div>
</template>

<script setup>
import { HandIcon, PencilIcon, TagIcon } from '@heroicons/vue/outline'
import { useStorage } from '@vueuse/core'

const props = defineProps({
  content: {
    type: String,
    default: '',
  },
  polygonName: {
    type: String,
    default: '',
  },
  polygonIndex: {
    type: Number,
    default: 0,
  },
})
const emit = defineEmits(['delete', 'saved'])

const state = useStorage('app-store', { polygons: [], polygonNames: [] })
if (undefined == state.value.polygonNames) {
  state.value.polygonNames = []
}
</script>
