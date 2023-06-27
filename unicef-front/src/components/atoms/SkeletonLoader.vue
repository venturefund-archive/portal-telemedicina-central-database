<template>
  <div>
    <div
      v-for="i in count"
      :key="i"
      class="skeleton-loader"
      :class="[type, animation]"
      :style="{ width: width, height: height, borderRadius: `${radius}px` }"
    ></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
  width: {
    type: [Number, String],
    default: '100%',
  },
  height: {
    type: [Number, String],
    default: '16px',
  },
  type: {
    type: String,
    default: 'text',
    validator: (value) => ['text', 'button', 'avatar', 'input'].includes(value),
  },
  animation: {
    type: String,
    default: 'fade-in',
    validator: (value) => ['fade-in', 'wave'].includes(value),
  },
  radius: {
    type: Number,
    default: 12,
  },
  count: {
    type: Number,
    default: 1,
  },
})
</script>

<style scoped>
.skeleton-loader {
  @apply bg-gray-300;
  margin-bottom: 8px;
}

.text {
}

.button {
  @apply h-9 w-20;
}

.avatar {
  @apply h-12 w-12 rounded-full;
}

.input {
  @apply h-9;
}

.fade-in {
  animation: fadeIn 1.5s infinite;
}

.wave {
  background-image: linear-gradient(90deg, #eee 25%, #f0f0f0 50%, #eee 75%);
  background-size: 200% 100%;
  animation: wave 1.5s infinite;
}

@keyframes fadeIn {
  0% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.5;
  }
}

@keyframes wave {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
