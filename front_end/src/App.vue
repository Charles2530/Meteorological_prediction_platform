<template>
  <el-container class="bg-top-background bg-no-repeat bg-contain bg-black">
    <el-container class="no-padding">
      <el-aside width="80px">
        <Aside></Aside>
      </el-aside>
      <el-container>
        <el-header class="no-padding">
          <TopBar />
        </el-header>
        <el-main class="no-padding" style="overflow: hidden" :style="{ height: contentHeight }">
          <router-view v-slot="{ Component }">
            <transition :name="transition">
              <component :is="Component" />
            </transition>
          </router-view>
          <!-- <div
            class="content-placeholder"
            :style="{ height: contentHeight }"
          ></div> -->
        </el-main>
        <!-- <el-footer ref="footer">
          <Footer></Footer>
        </el-footer> -->
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
// const footerRef = ref<HTMLElement | null>(null);
const contentHeight = ref("calc(100vh - 60px)");

// onMounted(() => {
//   if (footerRef.value) {
//     contentHeight.value = `calc(100vh - ${footerRef.value.clientHeight}px)`;
//   }
// });
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
