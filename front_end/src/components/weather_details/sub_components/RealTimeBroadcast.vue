<template>
  <div class="calendar-container">
    <!-- <el-date-picker
        v-model="currentDate"
        type="month"
        placeholder="选择月份"
        @change="handleDateChange"
      ></el-date-picker> -->
    <el-row :gutter="20" justify="center">
      <el-col :span="2">
        <div class="ep-bg-purple-dark" />
        <!-- <el-card style="width:auto;" shadow="hover"> -->
        <div class="day-content">
          <div class="temperature">天气</div>
          <div class="temperature">温度</div>
          <div class="humidity">湿度</div>
          <div class="wind-speed">风速</div>
          <div class="wind-speed">风向</div>
          <div class="time">时间</div>
        </div>
        <!-- </el-card> -->
      </el-col>
      <el-col :span="2" v-for="(day, index) in realTimeWeatherList" :key="index">
        <div class="ep-bg-purple-dark" />
        <el-card style="width:auto" shadow="hover">
          <div class="day-content">
            <div class="weather-icon">
              <div class="temperature">{{ day.condition }}</div>
            </div>
            <div class="temperature">{{ day.temperature }}℃</div>
            <div class="humidity">{{ day.humidity }}%</div>
            <div class="wind-speed">{{ day.windSpeed }}m/s</div>
            <div class="wind-speed">{{ day.windDirection }}</div>
            <div class="time" style="color:black;font-size: 0.6cm;">{{ day.time }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

  </div>
</template>

<!-- <template>
  <div class="calendar-container">
    <el-date-picker
        v-model="currentDate"
        type="month"
        placeholder="选择月份"
        @change="handleDateChange"
      ></el-date-picker>
    <div class="calendar-grid">
      <div class="calendar-column" v-for="(day, index) in realTimeWeatherList" :key="index">
        <div class="day-content">
          <div class="weather-icon">
            <img :src="day.condition" alt="Weather Image">
            <div class="temperature">{{ day.condition }}℃</div>
          </div>
          <div class="temperature">{{ day.temperature }}℃</div>
          <div class="humidity">{{ day.humidity }}%</div>
          <div class="wind-speed">{{ day.windSpeed }}m/s</div>
          <div class="wind-speed">{{ day.windDirection }}</div>
          <div class="time">{{ day.time }}</div>
        </div>
      </div>
    </div>
  </div>
</template> -->

<script lang="ts" setup>

const city = ref({
  name: '北京市',
  adm2: '昌平区'
});
const realTimeWeatherList = ref<RealTimeWeather[]>([]);
interface RealTimeWeather {
  time: string,
  condition: string,
  temperature: number,
  humidity: number,
  windSpeed: number,
  windDirection: string
}

interface WeatherHisOverview {
  realTimeWeatherList: RealTimeWeather[];
}

import { post, get } from "@/api/index.ts";
const get_data = async () => {
  get<WeatherHisOverview>("/api/weather/overview_realtime", {city:city.value.name + city.value.adm2}).then((res) => {
    realTimeWeatherList.value = res.data.realTimeWeatherList;
  });
};
onMounted(() => {
  get_data();
  // console.log("----------------------------------------------------------------")
  // console.log(realTimeWeatherList);
});



</script>

<style lang="scss" scoped>
.calendar-container {
  background-color: #EAF2F8;
  padding: 20px;
}

.calendar-grid {
  display: flex;
  justify-content: space-between;
}

.calendar-column {
  width: 100%;
}

.day-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
}

.weather-icon img {
  max-width: 50px;
  max-height: 50px;
}

.temperature,
.humidity,
.wind-speed,
.time {
  margin-top: 10px;
}

.temperature,
.humidity,
.wind-speed,
.time {
  font-size: 16px;
  font-family: 'Courier New', Courier, monospace
}


.el-card {
  background-color: rgb(188, 243, 243);
  margin: 0px;
  border-radius: 20px;
  // border-color: #1058e9;
}

.el-card:hover {
  margin-top: -10px;
  margin: -1px;
}
</style>