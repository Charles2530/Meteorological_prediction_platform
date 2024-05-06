<template>
  <el-container style="height: 100%">
    <el-aside width="70px" style="height: 100%">
      <el-menu
        collapse
        style="height: 100%"
        router
        :default-active="router.currentRoute.value.path"
      >
        <el-menu-item index="/manage/user" route="/manage/user">
          <el-icon><User /></el-icon>
          <template #title> {{ manage.user.title }} </template>
        </el-menu-item>
        <el-menu-item index="/manage/data" route="/manage/data">
          <el-icon><PieChart /></el-icon>
          <template #title> {{ manage.data.title }} </template>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main
      class="no-padding"
      style="overflow-y: hidden; background-color: #bde3ff"
    >
      <router-view v-slot="{ Component }">
        <transition name="fade">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { useUserInfo } from "@/stores/userInfo";
import { useLoginConfig } from "@/stores/loginConfig";
import { UserRole } from "@/types/user.ts";
import { User } from "@element-plus/icons-vue";
import router from "@/router";

const permission = [UserRole.Administrator];
const userInfo = useUserInfo();
const themeConfig = useLoginConfig();
const manage = {
  user: {
    title: "用户管理",
  },
  data: {
    title: "数据管理",
  },
};
onMounted(() => {
  if (!permission.includes(userInfo.role)) themeConfig.showLoginPanel = true;
});
</script>

<style scoped>
.menu {
  height: calc(100vh - var(--el-header-height));
}
.flex-grow {
  flex-grow: 1;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
