<template>
  <div class="navBar">
    <el-menu
      router
      style="height: inherit"
      :default-active="router.currentRoute.value.path"
      mode="horizontal"
      :ellipsis="false"
      background-color="536888"
      active-text-color="#ffffff"
      text-color="#ffffff"
    >
      <el-menu-item index="/home"> 首页 </el-menu-item>
      <el-menu-item index="/history"> 天气情况 </el-menu-item>
      <el-menu-item index="/statistics"> 数据分析 </el-menu-item>
      <el-menu-item index="/alarm"> 灾害订阅 </el-menu-item>
      <el-menu-item v-if="__admin" index="/manage"> 后台管理 </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import router from "@/router";
import { useUserInfo } from "@/stores/userInfo";
import { UserRole } from "@/types/user";

const userInfo = useUserInfo();
const __admin = ref(false);
watch(
  () => userInfo.role,
  () => {
    __admin.value = userInfo.role == UserRole.Administrator;
  }
);
</script>

<style scoped>
.navBar {
  height: inherit;
}
</style>
