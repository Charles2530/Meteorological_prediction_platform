<template>
  <div class="ranking-container bg-white my-4">
    <city-info
      v-for="(city, index) in props.city_ranks"
      :key="index"
      :city="city"
      :rank="index + 1"
      :unit="getUnit(props.norm)"
    >
    </city-info>
  </div>
</template>

<script lang="ts" setup>
import CityInfo from "@c/dataStatistics/rank/cityInfo.vue";
import { RankItem } from "@/types/weather";
const props = defineProps<{
  city_ranks: RankItem[];
  norm: string;
}>();
const getUnit = (norm: string) => {
  if (norm === "temp") return "°C";
  if (norm === "pressure") return "hPa";
  if (norm === "humid") return "%";
  if (norm === "winSpeed") return "m/s";
  if (norm === "precip") return "mm";
  return "";
};
</script>
