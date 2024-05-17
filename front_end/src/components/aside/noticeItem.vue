<template>
  <div class="mx-2">
    <div class="notice-item">
      <notification-header
        :id="props.id"
        :img="props.img"
        :title="props.title"
        :date="props.date"
        :city="props.city"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import notificationHeader from "@c/notice/notificationHeader.vue";
const props = defineProps<{
  id: number;
  img: string;
  title: string;
  date: string;
  city: string;
}>();
</script>

<style scoped>
.notice-item {
  margin-bottom: 20px;
  padding: 10px;
  border-radius: 5px;
  background-color: #fafafa;


  /* 
   */
   background-color: #fdaee9;
  background-color: #eaec9a;
  background-color: #edaf10;
}
</style>
