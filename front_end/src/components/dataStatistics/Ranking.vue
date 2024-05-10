<template>
  <div class="ranking-container bg-white my-4">
    <city-info
      v-for="(city, index) in props.city_ranks"
      :key="index"
      :city="city"
      :rank="index + 1"
    >
    </city-info>
  </div>
</template>

<script lang="ts" setup>
import CityInfo from "@c/dataStatistics/cityInfo.vue";
import { RankItem } from "@/types/weather";
const props = defineProps<{
  city_ranks: RankItem[];
}>();
</script>
