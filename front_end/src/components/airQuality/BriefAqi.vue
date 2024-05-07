<template>
  <div class="air-quality-indicator">
    <div class="location text-2xl">{{ cityMessage.city }}</div>
    <div class="quality-circle">
      <div class="quality-level text-gray-200">{{ cityMessage.aqi }}</div>
    </div>
    <div class="quality-description text-slate-600 ml-2">
      {{ cityMessage.category }}
    </div>
  </div>
</template>
<script lang="ts" setup>
import { get } from "@/api/index.ts";
import { CityWeatherData } from "@/types/weather";
onMounted(() => {
  getPresentCityAqi();
});
interface CityInfoResponse {
  status: boolean;
  message: CityWeatherData;
}
const cityMessage = reactive<CityWeatherData>({} as CityWeatherData);
const getPresentCityAqi = async () => {
  get<CityInfoResponse>("/api/getCityInfo").then((res) => {
    cityMessage.aqi = res.data.message.aqi;
    cityMessage.city = res.data.message.city;
    cityMessage.category = res.data.message.category;
  });
};
</script>
<style>
.air-quality-indicator {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.location {
  margin-bottom: 10px;
}

.quality-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background-image: linear-gradient(
    to right,
    #0019d4,
    #4c72af,
    #07daff,
    #22ff6c,
    #51ff21f6
  );
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.quality-level {
  font-size: 40px;
  font-weight: bold;
  z-index: 1;
}
.quality-description {
  font-size: 30px;
  font-weight: bold;
  z-index: 1;
}
</style>
