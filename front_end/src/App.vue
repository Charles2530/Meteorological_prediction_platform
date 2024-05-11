<template>
  <el-container class="bg-top-background bg-no-repeat bg-contain bg-black">
    <el-header class="no-padding">
      <TopBar />
    </el-header>
    <el-main
      class="no-padding"
      style="overflow: auto"
      :style="{ height: contentHeight }"
    >
      <router-view v-slot="{ Component }">
        <component :is="Component" />
      </router-view>
    </el-main>
  </el-container>
  <Login />
</template>

<script setup lang="ts">
const TopBar = defineAsyncComponent(() => import("@c/topBar/index.vue"));
const Login = defineAsyncComponent(() => import("@c/content/login.vue"));

const contentHeight = ref("calc(100vh - 60px)");
</script>

<style scoped>
.no-padding {
  padding: 0px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.content-placeholder {
  height: 0;
}
</style>
