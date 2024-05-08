<template>
  <div
    class="my-modal-parent"
    @mouseover="showNoticeItems = true"
    @mouseleave="showNoticeItems = false"
  >
    <el-menu
      class="el-menu-vertical-demo rounded-lg"
      :default-active="activeMenu"
      text-color="#000"
      active-text-color="#ffd04b"
    >
      <el-sub-menu index="1">
        <template #title>
          <el-icon class="el-icon-menu"><Menu></Menu></el-icon>
          <strong class="nav-title text-md">订阅预警速递</strong>
        </template>
        <el-menu-item-group v-show="showNoticeItems">
          <notice-item
            v-for="(notice, index) in notifications"
            :key="index"
            :id="notice.id"
            :img="notice.img"
            :title="notice.title"
            :date="notice.date"
            :city="notice.city"
          >
          </notice-item>
        </el-menu-item-group>
      </el-sub-menu>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import { NotificationNotice } from "@/types/weather";
import noticeItem from "./noticeItem.vue";
import { get } from "@/api/index.ts";
const showNoticeItems = ref(false);
const activeMenu = ref("0");
const notifications = reactive<NotificationNotice[]>([]);
interface NotificationResponse {
  notifications: NotificationNotice[];
}
const getNotices = async () => {
  get<NotificationResponse>("/api/alarm_notices_brief/").then((res) => {
    notifications.splice(0, notifications.length, ...res.data.notifications);
  });
};
onMounted(() => {
  getNotices();
});
// const notices = [
//   "公告1：欢迎来到我们的网站！",
//   "公告2：请注意网站最新动态。",
//   "公告3：如有任何问题，请及时联系我们的客服。",
// ];
</script>

<style scoped>
.el-menu-vertical-demo {
  width: 60px;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
  /* background-color: #313c5c; */
  /* opacity: 0.8; */
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
.my-modal-parent {
  position: fixed;
  z-index: 999999;
}
.notice-item:hover {
  background-color: #e0e0e0;
  cursor: pointer;
}
</style>
