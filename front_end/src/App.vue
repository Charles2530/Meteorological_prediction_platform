<template>
  <el-container class="full-screen">
    <el-container class="no-padding">
      <el-aside width="100px">
        <Aside></Aside>
      </el-aside>
      <el-container>
        <el-header class="no-padding">
          <TopBar />
        </el-header>
        <el-main class="no-padding">
          <router-view v-slot="{ Component }">
            <transition :name="transition">
              <component :is="Component" />
            </transition>
          </router-view>
          <div
            class="content-placeholder"
            :style="{ height: contentHeight }"
          ></div>
        </el-main>
        <el-footer ref="footer">
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
const footerRef = ref<HTMLElement | null>(null);
const contentHeight = ref("calc(100vh - 0px)");

onMounted(() => {
  if (footerRef.value) {
    contentHeight.value = `calc(100vh - ${footerRef.value.clientHeight}px)`;
  }
});
</script>

<style scoped>
.no-padding {
  padding: 0px;
}
.full-screen {
  /* height: 200vw;
  width: 100vw; */
  background-color: #504099;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.content-placeholder {
  height: 0;
}
</style>
