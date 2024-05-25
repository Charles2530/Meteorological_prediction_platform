<template>
  <div class="topbar-logo">
    <img :src="logo" class="topbar-logo-img" />
  </div>
</template>

<script setup lang="ts">
import logo from "@img/logo.png";
</script>

<style scoped>
.topbar-logo {
  height: 50px;
  display: flex;
  align-items: center;
}
.topbar-logo-img {
  height: inherit;
  /* min-width: max-content; */
}
</style>
