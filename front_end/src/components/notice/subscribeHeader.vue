<template>
  <div class="clearfix">
    <img class="notification-img" :src="props.img" alt="Notification Image" />
    <span class="notification-title">{{ props.title }}</span>
    <div class="notification-date">{{ props.date }}</div>
  </div>
</template>
<script setup lang="ts">
const props = defineProps<{
  img: string;
  title: string;
  date: string;
}>();
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
</style>
