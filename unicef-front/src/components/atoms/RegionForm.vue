<template>
  <div class="p-3">
    <form
      @submit.prevent="
        $emit('saved', { localPolygon: { ...localPolygon, coordinates: polygonCoordinates }, polygonIndex })
      "
    >
      <InputIconWrapper>
        <template #icon>
          <TagIcon aria-hidden="true" class="h-5 w-5" />
        </template>
        <Input
          placeholder="Nome do poligono"
          v-model="localPolygon.name"
          withIcon
          class="mb-3 block w-full rounded-lg border border-transparent bg-gray-50 p-4 pl-10 text-sm text-gray-900"
        />
      </InputIconWrapper>
      <Button class="mx-3" type="button" variant="danger" @click="$emit('delete')">
        <HandIcon aria-hidden="true" />
        <span>Excluir</span>
      </Button>
      <Button type="submit" variant="success-outline" class="mx-3">
        <PencilIcon aria-hidden="true" />
        <span>Salvar</span>
      </Button>
    </form>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watchEffect } from 'vue'
import { HandIcon, PencilIcon, TagIcon } from '@heroicons/vue/outline'
import { useStorage } from '@vueuse/core'
import { useMicroRegionsStore } from '@/stores/microregions'
const microregionsStore = useMicroRegionsStore()

const props = defineProps({
  content: {
    type: String,
    default: '',
  },
  polygon: {
    type: Object,
    default: () => ({ id: 0, name: '' }), // Default to an object with name: ''
  },
  googlePolygon: {
    type: Object,
    default: () => ({ id: 0, name: '' }), // Default to an object with name: ''
  },
  polygonIndex: {
    type: Number,
    default: 0,
  },
})

const polygonCoordinates = ref([])
const localPolygon = ref({ ...props.polygon }) // Create local ref copy of polygon prop

watchEffect(() => {
  // Update localPolygon when props.polygon changes
  localPolygon.value = { ...props.polygon }
})

const emit = defineEmits(['delete', 'saved'])
onMounted(async () => {
  const vertices = props.googlePolygon.getPath()
  vertices.forEach(function (vertex) {
    polygonCoordinates.value.push([vertex.lng(), vertex.lat()])
  })
})
</script>
