<template>
  <el-container
    class="flex-container bg-top-background bg-no-repeat bg-contain bg-black"
  >
    <el-header class="no-padding">
      <TopBar />
    </el-header>
    <el-main class="main-page">
      <router-view v-slot="{ Component }">
        <component :is="Component" />
      </router-view>
    </el-main>
    <el-footer>
      <NavBar />
    </el-footer>
  </el-container>
  <Login />
</template>

<script setup lang="ts">
const TopBar = defineAsyncComponent(() => import("@c/topBar/index.vue"));
const Login = defineAsyncComponent(() => import("@c/content/login.vue"));
const NavBar = defineAsyncComponent(() => import("@c/topBar/navBar.vue"));
</script>

<style scoped>
.flex-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.main-page {
  box-sizing: border-box;
  height: calc(100vh - 92px);
  overflow-y: scroll;
  overflow-x: hidden;
}
.no-padding {
  padding: 0px;
}
.no-padding-main {
  padding: 0px;
  /* overflow: auto;
  max-height: 85vh; */
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.content-placeholder {
  height: 0;
}
</style>
