<template>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/qweather-icons@1.3.0/font/qweather-icons.css">
  <div class="w-full font-semibold text-md flex-wrap text-white  background-transparent">
    <div class="
        flex 
        flex-col 
        relative
        h-full
      ">
      <!-- pc端的地区和时间 -->
      <div class="area-time flex flex-col py-3" style="align-items: center;">
        <div class="flex">
          <div class="">
            <span>{{ `${city.adm2} ${city.name}` }}</span>
          </div>
          <!-- <div>{{ ` ${formattedDate}` }}</div> -->
        </div>
        <div class="text-secondary">
          <!-- <slot name="search"></slot> -->
        </div>
      </div>
      <!-- pc端及移动端的天气图标及温度 -->
      <div class="
        px-2
        weather-info 
        flex 
        max-md-justify-between 
        relative 
      ">
        <div class="weather-icon max-md-relative opacity-30" style="padding-right: 12px;">
          <i :class="'qi-' + weather.condition_icon" style="font-size: 100px;"></i>
        </div>
        <div class="temperature-info flex flex-col">
          <span class="temperature">{{ `${weather.temp}°C` }}</span>
          <span >{{ weather.condition }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import QWeatherIcon from './QWeatherIcon.vue';
import { translateTime } from '@/utils/utilsFunc.js'
import { getDateToday } from '@/utils/utilsFunc.js'
import { defineEmits } from 'vue'

const search = true
const props = defineProps({
  weather: { type: Object },
  city: { type: Object },
  search: { type: Boolean }
})
let formattedDate = getDateToday()
const searchForPC = () => {
  // emit('searchShow', !props.search)
}
</script>

<style scoped>
.background-transparent{
  background: transparent;
  border-color: transparent;
}

.max-md-bg-gradient {
  background-image: linear-gradient(to right, #67E1D2, #54A8FF);
  /* box-shadow: 0 10px 30px -12px rgba(7, 89, 133, 0.45); */
}

.area-time {
  font-size: 20px;
}

.weather-info {
  margin-top: 40px;
  margin-bottom: 40px;
}

.temperature-info {
  font-size: 30px;
}

.temperature {
  font-size: 70px;
  background-clip: text;
  -webkit-background-clip: text;
  /* color: transparent; */
  /* background-image: linear-gradient(to bottom right, white 40%, ...); */
}
</style>
