<template>
  <el-card class="box-card">
    <div>
      <notificationHeader
        :img="notification.img"
        :title="notification.title"
        :date="notification.date"
      />
    </div>
    <div class="notification-content">
      <div class="notification-text">
        {{ notification.content }}
      </div>
    </div>
    <div class="notification-instruction">
      <span>预警说明：</span>
      {{ notification.instruction }}
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import { ElCard } from "element-plus";
import { NotificationData } from "@/types/weather";
import notificationHeader from "./notificationHeader.vue";

const props = defineProps<{
  notification: NotificationData;
}>();

const notification = ref(props.notification);
</script>

<style scoped>
.notification-img {
  width: 40px;
  height: 40px;
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

.notification-text {
  margin-top: 10px;
  margin-bottom: 10px;
}

.notification-instruction {
  font-style: italic;
  border-radius: 3px;
  background-color: #f0f0f0;
  padding: 10px;
}
</style>
