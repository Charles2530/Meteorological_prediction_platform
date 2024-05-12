<template>
  <div class="topbar-index">
    <Logo />
    <NavBar />
    <div class="flex-grow"></div>
    <SearchCity />
    <UserMenu />
  </div>
</template>
<script setup lang="ts">
const Logo = defineAsyncComponent(() => import("@c/topBar/logo.vue"));
const NavBar = defineAsyncComponent(() => import("@c/topBar/navBar.vue"));
const UserMenu = defineAsyncComponent(() => import("@c/topBar/userMenu.vue"));
const SearchCity = defineAsyncComponent(
  () => import("@c/topBar/searchCity.vue")
);
</script>

<style scoped lang="scss">
.topbar-index {
  height: 6vh;
  display: flex;
  align-items: center;
  padding-right: 20px;
  border-bottom: 1px solid #4c4d4f;
  background-color: var(--bg-topBar-color);
  transition: background-color 0.2s ease;
}

.flex-grow {
  flex-grow: 1;
}
</style>
