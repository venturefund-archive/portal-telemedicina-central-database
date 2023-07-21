<template>
  <div>
    <div ref="mapContainer" class="map-container"></div>
    <Marker
      v-for="marker in markers"
      :key="marker.id"
      :marker="marker"
      @update:position="updateMarkerPosition(marker)"
    />
    <!-- <Polygon
      v-for="polygon in polygons"
      :key="polygon.id"
      :polygon="polygon"
      @update:position="updatePolygonPosition(polygon)"
    /> -->
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, provide, inject } from 'vue'
import { usePatientsStore } from '@/stores/patients'
const patientsStore = usePatientsStore()
import { useMapStore } from '@/stores/map';

const markers = ref([]);
const polygons = ref([]);
const mapContainer = ref(null);
const map = ref(null);
const geocoder = ref(null);
const mapStore = useMapStore();

provide('map', map);
provide('geocoder', geocoder);

onUnmounted(() => {
  // polygonData.polygon.setMap(null);
  // polygonData.infoWindow.close();
  // if (polygonData.label) {
  //   polygonData.label.setMap(null);
  // }
  polygons.value = [];
})

onMounted(async () => {
  await initializeMap();
  await loadPolygons()
})

const loadPolygons = async () => {
  try {
    const loadedPolygons = await mapStore.fetchPolygons();
    loadedPolygons.forEach((polygonData) => {
      const polygonObj = createLoadedPolygon(polygonData);
      polygons.value.push(polygonObj);
    });
  } catch (error) {
    console.error('Erro ao carregar polígonos:', error);
  }
}

const createLoadedPolygon = (polygonData) => {
  const polygon = new google.maps.Polygon({
    paths: polygonData.coordinates,
    map: map.value,
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: '#FF0000',
    fillOpacity: 0.35,
  });

  const infoWindow = new google.maps.InfoWindow();
  const nameInput = document.createElement('input');
  const saveButton = document.createElement('button');
  const deleteButton = document.createElement('button');

  nameInput.type = 'text';
  nameInput.value = polygonData.name;
  saveButton.textContent = 'Save';
  deleteButton.textContent = 'Delete';

  const content = document.createElement('div');
  content.appendChild(nameInput);
  content.appendChild(saveButton);
  content.appendChild(deleteButton);

  const polygonObj = {
    polygon,
    infoWindow,
    name: polygonData.name,
    label: null,
  };

  // Click event listener
  google.maps.event.addListener(polygon, 'click', () => {
    infoWindow.setPosition(getPolygonCenter(polygon));
    infoWindow.open(map.value);
  });

  saveButton.addEventListener('click', async () => {
    polygonObj.name = nameInput.value;
    updatePolygonLabel(polygonObj);
    await mapStore.updatePolygon(polygonData.id, {
      name: polygonObj.name,
      coordinates: polygon.getPath().getArray().map(latLng => {
        return [latLng.lng(), latLng.lat()];
      })
    });
    infoWindow.close();
  });

  deleteButton.addEventListener('click', () => {
    polygonObj.id = polygonData.id
    deletePolygon(polygonObj);
  });

  infoWindow.setContent(content);

  // Add label
  updatePolygonLabel(polygonObj);

  return polygonObj;
};


const initializeMap = async () => {
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

  await placeMarkers();
};

const placeMarkers = async () => {
  try {
    await patientsStore.fetchPatients()
    markers.value = patientsStore.items
  } catch (error) {
    console.error('Erro ao carregar marcadores:', error)
  }

  markers.value.forEach((person) => {
    const marker = createMarker({
      ...person,
      position: { lat: person.address.latitude, lng: person.address.longitude },
    });
    markers.value.push(marker);
  });
};

const createMarker = (person) => {
  const marker = new google.maps.Marker({
    position: person.position,
    map: map.value,
    draggable: false,
    icon: {
      url: person.alerts.length > 0 ? 'marker-alert.svg' : 'marker.svg',
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
  <p>Address: ${JSON.stringify(person.address)}</p>
  <p>Alerts: ${JSON.stringify(person.alerts)}</p>
  <p>Age: ${person.age_in_days}</p>
  <button id="marker${person.id}">${isMarkerMovable ? 'Cancel' : 'Move Marker'}</button>
`;

const createPolygon = (polygonData) => {

  const polygon = new google.maps.Polygon({
    paths: polygonData.coordinates,
    map: map.value,
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: '#FF0000',
    fillOpacity: 0.35,
  });

  // Aqui você poderia adicionar qualquer outro código para adicionar eventos de clique, janelas de informação, etc., se necessário.

  return polygon;
};

const createPolygonInfoWindow = (polygon, openImmediately = true) => {
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

  saveButton.addEventListener('click', async  () => {
    polygonData.name = nameInput.value
    await mapStore.createPolygon({
      name: polygonData.name,
      coordinates: polygonData.polygon.getPath().getArray().map(latLng => {
        return [latLng.lng(), latLng.lat()];
      })
    });
    updatePolygonLabel(polygonData);
    infoWindow.close();
  });

  deleteButton.addEventListener('click', () => {
    deletePolygon(polygonData);
  });

  infoWindow.setContent(content);

  // Open infoWindow when polygon is created
  // Abra infoWindow quando o polígono for criado apenas se openImmediately for true
  if (openImmediately) {
    infoWindow.setPosition(polygon.getPath().getAt(0));
    infoWindow.open(map.value);
  }
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

const deletePolygon = async (polygonData) => {
  const index = polygons.value.indexOf(polygonData);
  if (index !== -1) {
    try {
      console.log(polygonData)
      await mapStore.deletePolygon(polygonData.id);

      const polygon = polygonData.polygon;
      polygon.setMap(null);
      polygonData.infoWindow.close();
      if (polygonData.label) {
        polygonData.label.setMap(null);
      }
      polygons.value.splice(index, 1);

    } catch (err) {
      console.log(err);
      errorToast({ text: err.message });
    }
  }
};

</script>

<style scoped>
.map-container {
  height: 500px;
  width: 100%;
}
</style>
