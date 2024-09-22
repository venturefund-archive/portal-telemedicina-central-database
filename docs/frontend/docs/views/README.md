# Views

This directory contains the Vue components that represent entire pages or major sections of the application. These views are typically rendered by the router and may contain multiple smaller components.

## Directory Structure

The views are organized in the `frontend/src/views` directory. Each view is a Vue component file (.vue) that represents a specific page or major section of the application.

## Key Views

1. `HomeView.vue`: The main landing page of the application.
2. `LoginView.vue`: Handles user authentication and login.
3. `PatientDetailsView.vue`: Displays detailed information about a specific patient.
4. `PatientListView.vue`: Shows a list of patients.
5. `VaccineBookletView.vue`: Displays the vaccine booklet for a patient.

## Router Integration

These views are integrated with the Vue Router, which is configured in:

```typescript:frontend/src/router/index.js```

## State Management

Views often interact with the Pinia stores to manage global state. The stores are located in:

```typescript:frontend/src/stores```


## Internationalization

Views support internationalization using the Vue I18n plugin. Translations are stored in JSON files in the `frontend/src/locales/` directory.

## Styling

Views use Tailwind CSS for styling. Custom styles are defined in:

```css:frontend/src/tailwind.css```


## Best Practices

When creating or modifying views:

1. Keep views focused on layout and composition of smaller components.
2. Use components from `@/components` for reusable UI elements.
3. Implement page-specific logic in the view or in a dedicated composable.
4. Use Pinia stores for managing global state.
5. Implement proper error handling and loading states.
6. Ensure responsive design using Tailwind CSS classes.
7. Use Vue Router for navigation between views.
8. Implement proper accessibility features (ARIA attributes, keyboard navigation, etc.).

## Example View Structure

Here's a basic structure of a view component:

```vue
<template>
<div>
<!-- Layout and composition of smaller components -->
<Header />
<main>
<ComponentA />
<ComponentB />
</main>
<Footer />
</div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from '@/stores/someStore'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import ComponentA from '@/components/ComponentA.vue'
import ComponentB from '@/components/ComponentB.vue'
const store = useStore()
// View-specific logic
const someData = ref(null)
onMounted(async () => {
// Fetch data or perform other initialization
someData.value = await store.fetchSomeData()
})
</script>
```

For more detailed information on the project structure and development guidelines, please refer to the main project README and CONTRIBUTING files.