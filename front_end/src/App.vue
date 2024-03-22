<template>
  <el-container class="full-screen">
    <el-header class="no-padding">
      <TopBar />
    </el-header>
    <el-container class="no-padding">
      <el-aside width="200px">
        <Aside></Aside>
      </el-aside>
      <el-container>
        <el-main class="no-padding">
          <router-view v-slot="{ Component }">
            <transition :name="transition">
              <component :is="Component" />
            </transition>
          </router-view>
        </el-main>
        <el-footer>
          <Footer></Footer>
        </el-footer>
      </el-container>
    </el-container>
  </el-container>
  <Login />
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
const route = useRoute();
const TopBar = defineAsyncComponent(() => import("@c/topBar/index.vue"));
const Aside = defineAsyncComponent(() => import("@c/aside/index.vue"));
const Footer = defineAsyncComponent(() => import("@c/footer/index.vue"));
const Login = defineAsyncComponent(() => import("@c/content/login.vue"));
const transition = computed(() => {
  return (route.meta?.transition as string) || "fade";
});
</script>

<style scoped>
.no-padding {
  padding: 0px;
}
.full-screen {
  height: 100vh;
  width: 100vw;
  background-color: #504099;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
</style>
