<template>
  <div>
    <SearchCity />
  </div>
</template>

<script setup lang="ts">
const SearchCity = defineAsyncComponent(
  () => import("@c/topBar/searchCity.vue")
);
</script>

<style scoped></style>
