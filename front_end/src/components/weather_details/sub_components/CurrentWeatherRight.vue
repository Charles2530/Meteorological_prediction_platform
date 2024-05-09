<template>
  <div class="w-full text-[#333333] font-semibold text-md flex-wrap"
    >
    <div class="
        flex 
        flex-col 
        p-4 
        rounded-lg 
        relative 
        bg-[#FFFFFF] 
        shadow-[0_10px_30px_-12px_rgba(7,89,133,0.45)] 
        h-full
      ">
      <div class="flex justify-between">
        <span>天气详情</span>
        <!-- <button @click="refresh"><img class="w-6 h-6" src="@/assets/refresh.png" alt="refresh"></button> -->
      </div>
      <div class="grid grid-cols-3 gap-4 h-full mt-6">
        <template v-for="(item, index) in dispalyInfo" :key="index">
          <div v-if="item.data" class="flex flex-col text-center items-center gap-2">
            <img :src="item.icon" :alt="item.name" v-if="item.icon" class="w-6 h-6">
            <span>{{ item.name }}</span>
            <span>{{ item.data }}{{ item.unit }}</span>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
const props = defineProps({
  weather: { type: Object },
  // air: { type: Object },
  // city: { type: Object },
  // ultraviolet: { type: Array, default: [] }
})

const dispalyInfo = computed(() => {
  return [
    {
      name: '体感温度',
      icon: '../src/assets/img/weather_his/thermometer.png',
      data: props.weather.temp_feel,
      unit: '℃'
    },
    {
      name: '降水概率',
      icon: '../src/assets/img/weather_his/cloudrain.png',
      data: props.weather.precip_probability,
      unit: '%'
    },
    {
      name: '降水量',
      icon: '../src/assets/img/weather_his/cloudrain.png',
      data: props.weather.precip,
      unit: 'mm'
    },
    {
      name: '大气压强',
      icon: '../src/assets/img/weather_his/thermometer.png',
      data: props.weather.pressure,
      unit: 'hPa'
    },
    {
      name: '空气质量',
      icon: '../src/assets/img/weather_his/wind.png',
      data: props.weather.aqi,
      unit: 'AQI'
    },
    {
      name: '紫外线',
      icon: '../src/assets/img/weather_his/sunhorizon.png',
      data: props.weather.ray
    }
  ];
});


// onMounted(() => {
//   dispalyInfo.value[0].data = props.weather.temp_feel;
//   dispalyInfo.value[1].data = props.weather.precip_probability;
//   dispalyInfo.value[2].data = props.weather.precip;
//   dispalyInfo.value[3].data = props.weather.pressure;
//   dispalyInfo.value[4].data = props.weather.aqi;
//   dispalyInfo.value[5].data = props.weather.ray;
// });



// // 获取紫外线（太阳直射辐射）
// const curUltraviolet = computed(() => {
//   const curHour = (new Date).getHours()
//   return props.ultraviolet.find(item => {
//     const hour = (new Date(item.fxTime)).getUTCHours()
//     return hour === curHour
//   })?.direct
// })

// const emits = defineEmits(['refresh'])
// const refresh = () => {
//   emits('refresh', props.city, false)
// }

// const dispalyInfo = [
// {
//     name: '体感温度',
//     icon: '../src/assets/img/weather_his/thermometer.png',
//     data: 12,//props.weather.feelsLike,
//     unit: '℃'
//   },
//   {
//     name: '降水概率',
//     icon: '../src/assets/img/weather_his/cloudrain.png',
//     data: 12,//props.weather.windSpeed,
//     unit: '%'
//   },
//   {
//     name: '降水量',
//     icon: '../src/assets/img/weather_his/cloudrain.png',
//     data: 1,//props.weather.precip,
//     unit: 'mm'
//   },
//   {
//     name: '大气压强',
//     icon: '../src/assets/img/weather_his/thermometer.png',
//     data: 20,//curUltraviolet.value
//   },
//   {
//     name: '空气质量',
//     icon: '../src/assets/img/weather_his/wind.png',
//     data: "6:00",//curUltraviolet.value
//   },
//   {
//     name: '紫外线',
//     icon: '../src/assets/img/weather_his/sunhorizon.png',
//     data: 20,//curUltraviolet.value
//   }
// ]
</script>

<style scoped></style>
