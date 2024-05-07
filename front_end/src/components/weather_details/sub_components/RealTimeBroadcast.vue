<template>
    <div class="calendar-container">
      <!-- <el-date-picker
        v-model="currentDate"
        type="month"
        placeholder="选择月份"
        @change="handleDateChange"
      ></el-date-picker> -->
      <div class="calendar-grid">
        <div class="calendar-column" v-for="(day, index) in daysInMonth" :key="index">
          <div class="day-content">
            <div class="weather-icon">
              <img :src="day.image" alt="Weather Image">
            </div>
            <div class="temperature">{{ day.lowTemp }} ~ {{ day.highTemp }}</div>
            <div class="humidity">{{ day.humidity }}</div>
            <div class="wind-speed">{{ day.windSpeed }}</div>
            <div class="time">{{ day.time }}</div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, computed } from 'vue';
  
  interface DayInfo {
    image: string;
    lowTemp: string;
    highTemp: string;
    humidity: string;
    windSpeed: string;
    time: string;
  }
  
  export default defineComponent({
    name: 'CalendarView',
    setup() {
      // 当前选中日期
      const currentDate = ref<string>(new Date().toISOString().substr(0, 7));
  
      // 模拟每一天的信息
      const daysInMonth = computed(() => {
        const days: DayInfo[] = [];
        // 假设每一天的信息
        for (let i = 1; i <= 31; i++) { // 假设每月最多31天
          days.push({
            image: 'https://example.com/weather-image.jpg', // 替换为实际的天气图片链接
            lowTemp: '10°C', // 替换为实际的最低气温
            highTemp: '20°C', // 替换为实际的最高气温
            humidity: '50%', // 替换为实际的湿度
            windSpeed: '10m/s', // 替换为实际的风速
            time: '12:00' // 替换为实际的时间
          });
        }
        return days;
      });
  
      // 处理日期变化事件
      const handleDateChange = (date: string) => {
        currentDate.value = date;
      };
  
      return {
        currentDate,
        daysInMonth,
        handleDateChange
      };
    }
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
  }
  </style>
  