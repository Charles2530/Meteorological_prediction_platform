<template>
  <div class="ranking-container bg-white my-4 p-2">
    <city-info
      v-for="(city, index) in props.city_aqi_ranks"
      :key="index"
      :city="city"
      :rank="index + 1"
    >
    </city-info>
  </div>
</template>

<script lang="ts" setup>
import CityInfo from "./cityInfo.vue";
import { AqiRankItem } from "@/types/weather";
const props = defineProps<{
  city_aqi_ranks: AqiRankItem[];
}>();
</script>

<style scoped>
/* 样式 */
</style>
