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
      <el-menu-item index="/history"> 历史记录 </el-menu-item>
      <!-- <el-menu-item index="/predict"> AI预测 </el-menu-item> -->
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
// const __admin = userInfo.role == UserRole.Administrator;
const __admin = true;
</script>

<style scoped>
.navBar {
  height: inherit;
  padding-left: 10px;
}
</style>
