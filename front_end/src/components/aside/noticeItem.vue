<template>
  <div class="mx-2">
    <el-icon><Bell /></el-icon>
    <span>通知</span>
    <div class="notice-item">
      <notification-header
        :img="props.img"
        :title="props.title"
        :date="props.date"
      />
    </div>
    <!-- 点击跳转查看详情 -->
    <el-button type="text" class="text-sm" @click="redirectToDetails(props.id)">
      <el-icon><Link /></el-icon>
      查看详情</el-button
    >
    <el-divider></el-divider>
  </div>
</template>

<script setup lang="ts">
import notificationHeader from "@c/notice/notificationHeader.vue";
import router from "@/router";
const props = defineProps<{
  id: number;
  img: string;
  title: string;
  date: string;
}>();
const redirectToDetails = (id: number) => {
  router.push({ name: "Alarm", query: { notificationId: id.toString() } });
};
</script>

<style scoped>
.notice-item {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f0f0f0;
}
</style>
