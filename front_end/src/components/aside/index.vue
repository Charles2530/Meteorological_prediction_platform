<template>
  <SideBar />
</template>
<script setup lang="ts">
const SideBar = defineAsyncComponent(() => import("@c/aside/sideBar.vue"));
</script>
