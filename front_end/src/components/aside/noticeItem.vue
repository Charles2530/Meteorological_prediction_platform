<template>
  <div class="mx-2">
    <el-icon><Bell /></el-icon>
    <span>通知</span>
    <div class="notice-item">{{ props.content }}</div>
    <el-divider></el-divider>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  content: string;
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
