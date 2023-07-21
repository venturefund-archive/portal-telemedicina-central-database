<template>
  <!-- empty, because markers are not represented by DOM elements -->
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, inject } from 'vue'
import { usePatientsStore } from '@/stores/patients'
const patientsStore = usePatientsStore()

const props = defineProps({
  marker: Object
});

const map = inject('map');
const geocoder = inject('geocoder');

let googleMarker = null;

onMounted(() => {
  googleMarker = new google.maps.Marker({
    position: props.marker.position,
    map: map.value,
    draggable: false,
    icon: {
      url: 'marker.svg',
    },
  });

  googleMarker.addListener("click", () => {
    const infowindow = new google.maps.InfoWindow({
      content: getMarkerContent(props.marker, googleMarker.getDraggable()),
    });

    googleMarker.infowindow = infowindow;
    infowindow.open(map.value, googleMarker);

    infowindow.addListener('domready', () => {
      const moveButton = document.querySelector(`#marker${props.marker.id}`);
      moveButton.addEventListener('click', () => {
        toggleMarkerMovement(googleMarker, props.marker);
      });
    });

    infowindow.addListener('closeclick', () => {
      if(googleMarker.getDraggable()) {
        toggleMarkerMovement(googleMarker, props.marker);
      }
    });
  });

  googleMarker.addListener('dragend', () => {
    const updatedMarker = {
      ...props.marker,
      position: googleMarker.getPosition().toJSON()
    };
    patientsStore.updateMarker(props.marker.id, updatedMarker);
  });
});

watch(() => props.marker.position, () => {
  if (googleMarker) {
    googleMarker.setPosition(new google.maps.LatLng(props.marker.position.lat, props.marker.position.lng));
  }
});

onUnmounted(() => {
  if (googleMarker) {
    googleMarker.setMap(null);
    googleMarker = null;
  }
});

const getMarkerContent = (person, isMarkerMovable) => `
  <p>ID: ${person.id}</p>
  <p>Address: ${person.address}</p>
  <p>Age: ${person.age}</p>
  <button id="marker${person.id}">${isMarkerMovable ? 'Cancel' : 'Move Marker'}</button>
`;

const toggleMarkerMovement = (marker, person) => {
  if (marker.getDraggable()) {
    marker.setDraggable(false);
    marker.setIcon('marker.svg');
  } else {
    marker.setDraggable(true);
    marker.setIcon('marker-editing.svg');
    marker.infowindow.setContent(getMarkerContent(person, true));
  }
};
</script>
