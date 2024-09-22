# State Management

This application uses Pinia for state management. Pinia is a store library for Vue, providing a straightforward and effective way to manage global state in the application.

## Store Structure

The stores are located in the `frontend/src/stores` directory. Each store is responsible for managing a specific domain of the application. The main stores are:

1. `map.js`: Manages state related to map functionality.
2. `patients.js`: Handles patient data and operations.
3. `microregions.js`: Manages microregion data.
4. `protocol.js`: Handles vaccine protocol data.
5. `vaccines.js`: Manages vaccine-related state.
6. `loggedUser.js`: Handles the logged-in user's state.
7. `doses.js`: Manages vaccine doses data.

## Store Implementation

Each store is implemented using Pinia's `defineStore` function. The general structure of a store includes:

- State: Reactive data using `ref` or `reactive`.
- Actions: Functions that can modify the state or perform asynchronous operations.
- Getters: Computed properties based on the state (if needed).

Here's an example of a typical store structure:


```javascript
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useStorage } from '@vueuse/core'
import axios from 'axios'
import { errorToast } from '@/toast'
export const useExampleStore = defineStore('example', () => {
// State
const items = ref([])
const item = ref(null)
// Actions
async function fetchItems() {
const state = useStorage('app-store', { token: '' })
try {
const response = await axios.get(import.meta.env.VITE_API_URL + '/api/items/', {
headers: {
'Content-type': 'application/json',
Authorization: token ${state.value.token},
},
})
items.value = response.data
} catch (err) {
errorToast({ text: err.message })
}
}
// Return state and actions
return {
items,
item,
fetchItems,
}
})
```

## Using Stores in Components

To use a store in a component:

1. Import the store
2. Call the store function to get an instance
3. Use the state, actions, or getters from the store

Example:

```vue
<script setup>
import { useVaccinesStore } from '@/stores/vaccines'
const vaccinesStore = useVaccinesStore()
// Use the store
vaccinesStore.fetchVaccines()
console.log(vaccinesStore.items)
</script>
```

## Key Features

- **Centralized State Management**: All global state is managed in one place, making it easier to track and update.
- **TypeScript Support**: Pinia provides excellent TypeScript support out of the box.
- **Modular**: Each store is a self-contained module, promoting code organization and reusability.
- **DevTools Support**: Pinia integrates with Vue DevTools, allowing for easy debugging and state inspection.
- **Composition API**: Stores are defined using the Composition API, aligning with Vue 3's preferred style.

## Best Practices

1. Keep stores focused on a specific domain or feature.
2. Use actions for all state modifications, especially for asynchronous operations.
3. Leverage Vue's reactivity system by using `ref` and `reactive` for state.
4. Use the `useStorage` composable from VueUse for persisting state to local storage when needed.
5. Handle errors in actions and use toast notifications to inform users of issues.

By following these patterns and best practices, the application maintains a clean and manageable state architecture, promoting scalability and maintainability.