<template>
  <div>
    <div ref="mapContainer" class="map-container"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const mapContainer = ref(null);
const map = ref(null);
const geocoder = ref(null);
const markers = ref([]);
const polygons = ref([]);

onMounted(() => {
  initializeMap();
});

onUnmounted(() => {
  markers.value.forEach(marker => marker.setMap(null));
  markers.value = [];

  polygons.value.forEach(polygonData => {
    polygonData.polygon.setMap(null);
    polygonData.infoWindow.close();
    if (polygonData.label) {
      polygonData.label.setMap(null);
    }
  });
  polygons.value = [];
});

const initializeMap = () => {
  const mapOptions = {
    zoom: 14,
    center: new google.maps.LatLng(-23.5015, -48.5592),
  };
  map.value = new google.maps.Map(mapContainer.value, mapOptions);
  geocoder.value = new google.maps.Geocoder();

  const drawingManager = new google.maps.drawing.DrawingManager({
    drawingMode: null,
    drawingControl: true,
    drawingControlOptions: {
      position: google.maps.ControlPosition.TOP_CENTER,
      drawingModes: [
        google.maps.drawing.OverlayType.POLYGON,
      ],
    },
    polygonOptions: {
      editable: false,
      draggable: false,
    },
  });
  drawingManager.setMap(map.value);

  google.maps.event.addListener(drawingManager, 'overlaycomplete', (event) => {
    const polygon = event.overlay;
    createPolygonInfoWindow(polygon);
    drawingManager.setDrawingMode(null);
  });

  placeMarkers();
};

const placeMarkers = () => {
  const data = Array.from({ length: 10 }, (_, id) => {
    const latitude = -23.5015 + Math.random() * 0.02 - 0.01;
    const longitude = -48.5592 + Math.random() * 0.02 - 0.01;
    return {
      id,
      position: { lat: latitude, lng: longitude },
      address: `Address ${id}`,
      age: Math.floor(Math.random() * 100) + 1
    };
  });

  data.forEach((person) => {
    const marker = createMarker(person);
    markers.value.push(marker);
  });
};

const createMarker = (person) => {
  const marker = new google.maps.Marker({
    position: person.position,
    map: map.value,
    draggable: false,
    icon: {
      url: 'marker.svg',
    },
  });

  marker.addListener("click", () => {
    const infowindow = new google.maps.InfoWindow({
      content: getMarkerContent(person, marker.getDraggable()),
    });

    marker.infowindow = infowindow;
    infowindow.open(map.value, marker);

    infowindow.addListener('domready', () => {
      const moveButton = document.querySelector(`#marker${person.id}`);
      moveButton.addEventListener('click', () => {
        toggleMarkerMovement(marker, person);
      });
    });

    infowindow.addListener('closeclick', () => {
      if(marker.getDraggable()) {
        toggleMarkerMovement(marker, person);
      }
    });
  });

  marker.addListener('dragend', () => {
    updateMarkerPosition(marker, person);
  });

  return marker;
};

const toggleMarkerMovement = (marker, person) => {
  if (marker.getDraggable()) {
    marker.setDraggable(false);
    marker.setIcon('marker.svg');
    updateMarkerPosition(marker, person);
  } else {
    marker.setDraggable(true);
    marker.setIcon('marker-editing.svg');
    marker.infowindow.setContent(getMarkerContent(person, true));
  }
};

const updateMarkerPosition = (marker, person) => {
  geocoder.value.geocode({ 'location': marker.getPosition() }, (results, status) => {
    if (status === 'OK') {
      if (results[0]) {
        person.address = results[0].formatted_address;
        marker.infowindow.setContent(getMarkerContent(person, false));
      } else {
        console.log('No results found');
      }
    } else {
      console.log('Geocoder failed due to: ' + status);
    }
  });
};

const getMarkerContent = (person, isMarkerMovable) => `
  <p>ID: ${person.id}</p>
  <p>Address: ${person.address}</p>
  <p>Age: ${person.age}</p>
  <button id="marker${person.id}">${isMarkerMovable ? 'Cancel' : 'Move Marker'}</button>
`;


const createPolygonInfoWindow = (polygon) => {
  const infoWindow = new google.maps.InfoWindow();
  const nameInput = document.createElement('input');
  const saveButton = document.createElement('button');
  const deleteButton = document.createElement('button');

  nameInput.type = 'text';
  saveButton.textContent = 'Save';
  deleteButton.textContent = 'Delete';

  const content = document.createElement('div');
  content.appendChild(nameInput);
  content.appendChild(saveButton);
  content.appendChild(deleteButton);

  const polygonData = {
    polygon,
    infoWindow,
    name: '',
    label: null,
  };

  saveButton.addEventListener('click', () => {
    polygonData.name = nameInput.value;
    updatePolygonLabel(polygonData);
    infoWindow.close();
  });

  deleteButton.addEventListener('click', () => {
    deletePolygon(polygonData);
  });

  infoWindow.setContent(content);

  // Open infoWindow when polygon is created
  infoWindow.setPosition(polygon.getPath().getAt(0));
  infoWindow.open(map.value);
  nameInput.value = polygonData.name;

  // Add polygon click event listener
  google.maps.event.addListener(polygon, 'click', () => {
    infoWindow.open(map.value);
    nameInput.value = polygonData.name; // set the current name in the input field
  });

  polygons.value.push(polygonData);
};

const updatePolygonLabel = (polygonData) => {
  if (polygonData.label) {
    polygonData.label.setMap(null);
  }

  const labelContent = `
    ${polygonData.name}
  `;

  const label = new google.maps.Marker({
    position: getPolygonCenter(polygonData.polygon),
    map: map.value,
    icon: {
      url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
        <svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"></svg>
      `),
      labelOrigin: new google.maps.Point(0, -12),
    },
    label: {
      text: labelContent,
      color: 'black',
      fontSize: '16px',
      fontWeight: 'bold',
    },
    clickable: false,
  });

  polygonData.label = label;
};

const getPolygonCenter = (polygon) => {
  const bounds = new google.maps.LatLngBounds();
  polygon.getPath().forEach((point) => {
    bounds.extend(point);
  });
  return bounds.getCenter();
};

const deletePolygon = (polygonData) => {
  const index = polygons.value.indexOf(polygonData);
  if (index !== -1) {
    const polygon = polygonData.polygon;
    polygon.setMap(null);
    polygonData.infoWindow.close();
    if (polygonData.label) {
      polygonData.label.setMap(null);
    }
    polygons.value.splice(index, 1);
  }
};

</script>

<style scoped>
.map-container {
  height: 500px;
  width: 100%;
}
</style>
