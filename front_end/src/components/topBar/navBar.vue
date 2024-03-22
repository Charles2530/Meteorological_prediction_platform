<template>
  <div class="navBar">
    <el-menu
      router
      style="height: inherit"
      :default-active="router.currentRoute.value.path"
      mode="horizontal"
      :ellipsis="false"
    >
      <el-menu-item index="/history"> 历史记录 </el-menu-item>
      <el-menu-item index="/predict"> 数据预测 </el-menu-item>
      <el-menu-item index="/alarm"> 灾害预警 </el-menu-item>
      <el-menu-item index="/report"> 气象数据 </el-menu-item>
      <el-menu-item
        v-if="userInfo.role == UserRole.Administrator"
        index="/manage"
      >
        后台管理
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import router from "@/router";
import { useUserInfo } from "@/stores/userInfo";
import { UserRole } from "@/types/user";

const userInfo = useUserInfo();
</script>

<style scoped>
.navBar {
  height: inherit;
  padding-left: 10px;
}
</style>
