# Components

This directory contains the Vue components used in the Child Development Analyzer frontend application. The components are organized into different categories based on their complexity and purpose.

## Directory Structure

The components are organized into the following subdirectories:

- `atoms/`: Basic building blocks of the application
- `molecules/`: Combinations of atoms to form more complex UI elements
- `organisms/`: Complex components that combine multiple molecules and atoms
- `icons/`: SVG icons used throughout the application

## Key Components

### Atoms

1. `Button.vue`: A reusable button component with various styles and variants.
2. `Input.vue`: A customizable input component.
3. `Logo.vue`: Displays the UNICEF logo.
4. `VaccineAlertInfo.vue`: Shows vaccine alert information.

### Organisms

1. `Navbar.vue`: The main navigation bar component.
2. `PatientListCard.vue`: Displays patient information in a card format.

### Sidebar

The sidebar components are crucial for the application's layout:

1. `Sidebar.vue`: The main sidebar component that includes the header, content, and footer.
2. `SidebarContent.vue`: Contains the main navigation links.
3. `SidebarFooter.vue`: Displays information at the bottom of the sidebar.
4. `SidebarHeader.vue`: Shows the logo and other header information.

### Icons

Custom icon components are defined in the `icons/outline.jsx` file. These include:

- `MenuFoldLineRightIcon`
- `MenuFoldLineLeftIcon`
- `DashboardIcon`

## Usage

Components are typically imported and used in Vue files. For example:

```vue
<template>
<div>
<Navbar />
<Sidebar>
<SidebarContent />
<SidebarFooter />
</Sidebar>
<Button variant="primary">Click me</Button>
</div>
</template>
<script setup>
import Navbar from '@/components/organisms/Navbar.vue'
import Sidebar from '@/components/sidebar/Sidebar.vue'
import SidebarContent from '@/components/sidebar/SidebarContent.vue'
import SidebarFooter from '@/components/sidebar/SidebarFooter.vue'
import Button from '@/components/atoms/Button.vue'
</script>
````


## Styling

The components use Tailwind CSS for styling. Custom styles are defined in the `frontend/src/tailwind.css` file and the Tailwind configuration is in `frontend/tailwind.config.js`.

## State Management

Some components interact with the Pinia stores located in `frontend/src/stores/`. For example, the `Navbar.vue` component uses the `useLoggedUserStore` to display user information.

## Internationalization

The components support internationalization using the Vue I18n plugin. Translations are stored in JSON files in the `frontend/src/locales/` directory.

## Contributing

When adding new components or modifying existing ones, please follow these guidelines:

1. Use appropriate naming conventions (PascalCase for component names).
2. Place components in the correct subdirectory based on their complexity.
3. Use Tailwind CSS classes for styling when possible.
4. Ensure components are responsive and accessible.
5. Add appropriate props and emit events for component communication.
6. Document any complex logic or important information in comments.

For more detailed information on the project structure and development guidelines, please refer to the main project README and CONTRIBUTING files.
