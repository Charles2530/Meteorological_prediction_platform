<template>
  <div class="navBar">
    <el-menu
      router
      style="display: flex; justify-content: space-around; height: inherit"
      :default-active="router.currentRoute.value.path"
      mode="horizontal"
      :ellipsis="false"
      background-color="536888"
      active-text-color="#ffffff"
      text-color="#ffffff"
    >
      <el-menu-item index="/home"> <el-icon><Guide /></el-icon>天气速览 </el-menu-item>
      <el-menu-item index="/map"> <el-icon><MapLocation /></el-icon>地图 </el-menu-item>
      <!-- <el-menu-item index="/weather"> 天气情况 </el-menu-item> -->
      <el-menu-item index="/user"> <el-icon><UserFilled /></el-icon>我的 </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import router from "@/router";
</script>

<style scoped>
.navBar {
  height: inherit;
}
</style>
