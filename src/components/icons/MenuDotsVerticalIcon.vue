<script setup lang="ts">defineProps<{ fill_color: string }>();</script>

<template>
  <svg xmlns="http://www.w3.org/2000/svg" id="Layer_1" data-name="Layer 1" viewBox="0 0 24 24">
    <circle :fill="fill_color" cx="12" cy="2.5" r="2.5" />
    <circle :fill="fill_color" cx="12" cy="12" r="2.5" />
    <circle :fill="fill_color" cx="12" cy="21.5" r="2.5" />
  </svg>
</template>
