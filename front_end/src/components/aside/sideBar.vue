<template>
  <div>
    <el-menu
      class="el-menu-vertical-demo rounded-lg"
      :default-active="activeMenu"
      background-color="#fff"
      text-color="#000"
      active-text-color="#ffd04b"
    >
      <el-sub-menu index="1">
        <template #title>
          <el-icon class="el-icon-menu"><Menu></Menu></el-icon>
          <strong class="nav-title text-md">网站公告</strong>
        </template>
      </el-sub-menu>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
const activeMenu = ref("0");
</script>

<style scoped>
.el-menu-vertical-demo {
  width: 60px;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
  background-color: #fff;
  overflow: hidden;
  transition: width 0.3s ease;
}
.el-menu-vertical-demo .el-sub-menu {
  width: 250px; /* Set the width of the submenu to match the collapsed state */
}
.el-menu-vertical-demo:hover {
  width: 250px; /* Set the width to the expanded state on hover */
}
.el-icon-menu,
.el-icon-notice,
.el-icon-location {
  margin-right: 20px;
  color: red;
}
.nav-title:hover {
  text-decoration: underline;
  cursor: pointer;
  transform: scale(1.05);
  transition: all 0.2s ease-in-out;
  color: red;
}
.el-icon-style {
  font-size: 20px;
  margin-right: 20px;
}
.nav-title {
  color: #666;
  padding-left: 3px;
  font-style: normal !important;
}
</style>
