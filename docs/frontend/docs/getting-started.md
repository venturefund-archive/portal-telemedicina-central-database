# Getting Started with the Frontend

Welcome to the frontend of the Child Health Tracker project! This guide will help you set up and run the frontend on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:
- Node.js 14 or higher
- npm 6 or higher

## Installation

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

## Running the Development Server

To start the frontend development server:

```
npm run dev
```


This will start the server and automatically open your default browser to `http://localhost:5173` (or another port if 5173 is in use).

## Building for Production

To create a production build:

```
npm run build
```


This will generate optimized files in the `dist` directory.

## Running Tests

To run unit tests:

```
npm run test:unit
```

For end-to-end tests:

```
npm run test:e2e
```

## Linting

To lint your code:

```
npm run lint
```

## Project Structure

- `src/`: Contains the source code
  - `components/`: Vue components
  - `views/`: Vue views (pages)
  - `router/`: Vue Router configuration
  - `store/`: Vuex store (if used)
  - `assets/`: Static assets like images and fonts
- `public/`: Public files that are copied to the build directory

## Next Steps

- Explore the `src` directory to understand the project structure
- Check out the [Vue.js documentation](https://vuejs.org/guide/introduction.html) for more information on Vue 3
- Review the [Vite documentation](https://vitejs.dev/guide/) to learn about the build tool

If you encounter any issues or have questions, please refer to our project's main README or open an issue on GitHub.

Happy coding!