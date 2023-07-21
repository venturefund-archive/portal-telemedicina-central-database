<template>
    <div>
      <h1>Polygon Details</h1>
      <div v-if="currentPolygon">
        <p><strong>ID:</strong> {{ currentPolygon.id }}</p>
        <p><strong>Name:</strong> {{ currentPolygon.name }}</p>
        <p><strong>Coordinates:</strong></p>
        <ul>
          <li v-for="(coordinate, index) in currentPolygon.coordinates" :key="index">
            {{ `Lat: ${coordinate.lat}, Lng: ${coordinate.lng}` }}
          </li>
        </ul>
      </div>
      <button @click="deleteCurrentPolygon">Delete This Polygon</button>
    </div>
  </template>

  <script>
  import { computed, onMounted } from 'vue';
  import { useMapStore } from '@/stores/map';

  export default {
    props: {
      id: {
        type: Number,
        // required: true
      }
    },
    setup(props) {
      const mapStore = useMapStore();

      const currentPolygon = computed(() => mapStore.newPolygon);

      const deleteCurrentPolygon = async () => {
        await mapStore.deletePolygon(props.id);
        // Redirect, emit event, or perform other cleanup after deletion
      }

      onMounted(async () => {
        // await mapStore.fetchPolygon(props.id);
      })

      return {
        currentPolygon,
        deleteCurrentPolygon
      }
    }
  }
  </script>
