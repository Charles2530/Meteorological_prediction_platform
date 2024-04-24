<template>
  <div class="mx-2">
    <div class="notice-item">
      <notification-header
        :id="props.id"
        :img="props.img"
        :title="props.title"
        :date="props.date"
      />
    </div>

    <!-- <el-divider></el-divider> -->
  </div>
</template>

<script setup lang="ts">
import notificationHeader from "@c/notice/notificationHeader.vue";
const props = defineProps<{
  id: number;
  img: string;
  title: string;
  date: string;
}>();
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
