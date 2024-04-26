<template>
  <!-- 公告栏样式 -->
  <div class="clearfix">
    <img class="notification-img" :src="props.img" alt="Notification Image" />
    <span class="notification-title">{{ props.title }}</span>
    <span class="notification-city ml-2">{{ props.city }}</span>
    <div class="notification-date">{{ props.date }}</div>
    <!-- 点击跳转查看详情 -->
    <el-button type="text" class="text-sm" @click="redirectToDetails(props.id)">
      <el-icon><Link /></el-icon>
      查看详情</el-button
    >
  </div>
</template>
<script setup lang="ts">
import router from "@/router";
const props = defineProps<{
  id: number;
  img: string;
  title: string;
  date: string;
  city: string;
}>();
const redirectToDetails = (id: number) => {
  router.push({ name: "Alarm", query: { notificationId: id.toString() } });
};
</script>
<style scoped>
.clearfix {
  background-color: inherit;
}
.notification-img {
  width: 60px;
  height: 60px;
  float: left;
  margin-right: 10px;
}

.notification-title {
  font-weight: bold;
}

.notification-date {
  font-size: smaller;
  color: #888;
}
</style>
