<template>
  <div class="common-layout">
    <el-container class="bg-blue-500">
      <el-main class="bg-cyan-100">
        <el-calendar class="rounded-lg italic">
          <template #date-cell="{ data }">
            <el-row>
              <el-col :span="8">
                <p :class="data.isSelected ? 'is-selected text-xl' : 'text-xl'">
                  {{ data.day.split("-")[2] }}
                  <!-- {{parseInt(data.day.split("-")[2], 10)}} -->
                </p>
              </el-col>
              <el-col :span="16">
                <img class="weather-icon" src="@/assets/img/阴.png" alt="阴天" />
              </el-col>
            </el-row>
            <el-row>
              <span class="p-1 text-xl shadow-sm rounded-full"
                style="font-style: normal;font-family:'Courier New', Courier, monospace">
                <!-- {{ weatherList[data.day.split("-")[2]] }}~ {{ weatherList[data.day.split("-")[2]] }} -->
                {{ weatherTemp[0].min_temp }}~{{ weatherTemp[0].max_temp }}
                <!-- {{ aaa[data.day.split("-")[2]] }} -->
              </span>
            </el-row>
          </template>
        </el-calendar>
      </el-main>
      <el-aside class="bg-cyan-100" width="30%">
        <el-card shadow="always">
          <div class="grid-content">
            <span style="font-size: 30px"> 2024-05-10</span>
          </div>
          <hr style="height: 2px;   background: linear-gradient(to right, #dee5f8, #f4e2e2);" />
          <div style="margin-top: 30px;">
          <el-row>
            <el-col :offset="0" :span="8">
              <div class="grid-content">
                <img :src="getAssetsFile('阴.png')" style="width: 90px; height: 80px" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="grid-content">
                <span style="font-size: 36px">{{ weatherTemp[0].min_temp }}~{{ weatherTemp[0].max_temp }}℃</span>
                <span style="font-size: 20px">        阵雨</span>
                <!-- <span style="font-size: 36px">{{ getWeather(0).min_temp }}~{{ getWeather(0).max_temp }}&nbsp;</span>
                <span style="font-size: 20px">{{ getWeather(0).condition }}</span> -->
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20" style="margin-bottom: 20px !important">
            <el-col :offset="1" :span="7">
              <div class="grid-content" style=" align-items: center;">
                <span style="border: 1px solid #a5a5a5; border-radius: 10px;font-size: 20px;">天气提示</span>
              </div>
            </el-col>
            <el-col :offset="0" :span="15">
              <span style="font-size: 20px;">&nbsp{{ infos }}</span>
            </el-col>
          </el-row>
        </div>
          <div class="grid grid-cols-4 gap-4 h-full mt-6" style="font-size: 26px;">
            <template v-for="(item, index) in displayInfo" :key="index">
              <div v-if="item.data" class="flex flex-col text-center items-center gap-2">
                <img :src="item.icon" :alt="item.name" v-if="item.icon" class="w-6 h-6">
                <span>{{ item.name }}</span>
                <span>{{ item.data }}{{ item.unit }}</span>
              </div>
            </template>
          </div>
        </el-card>
      </el-aside>
    </el-container>
  </div>
</template>
<script lang="ts" setup>
import { getAssetsFile } from "@/utils/pub-use";

const city = ref({
  name: "北京市",
  adm2: "海淀区",
});
// const searchShow = ref(false);
const weatherList = ref<Weather42[]>([]);
const month = ref(5);
const infos = ref("局部多云，部分地区可能会有阵雨。温度和昨天差不多")
interface WeatherData {
  weatherList: Weather42[];
}
interface Weather42 {
  aqi: number;
  condition: string;
  max_temp: number;
  min_temp: number;
  precip: number;
  pressure: number;
  ray: string;
  sunrise_time: string;
  sunset_time: string;
  time: string;
}

import { post, get } from "@/api/index.ts";
const get_data = async () => {
  get<WeatherData>("/api/weather/30days", { city: city.value.name + city.value.adm2 }, { month: month.value }).then((res) => {
    weatherList.value = res.data.weatherList;
    console.log(weatherList.value);
  });
};


// const index: number = ref(0);
// let weather = weatherList.value[index.value];
console.log("----------------------------------------------------------------");
function getWeather(index: number) {
  return weatherList.value[index];
}

// --------------------Debugger --------------------
// watch(city, (newVal, oldVal) => {
//   console.log('City name changed:', newVal);
//   console.log('City name changed:', oldVal);
// });
// watch(month, (newVal, oldVal) => {
//   console.log('City name changed:', newVal);
//   console.log('City name changed:', oldVal);
// });
// watch(weatherList, (newVal, oldVal) => {
//   console.log('City name changed:', newVal);
//   console.log('City name changed:', oldVal);
// });
// watch(infos, (newVal, oldVal) => {
//   console.log('City name changed:', newVal);
//   console.log('City name changed:', oldVal);
// });
// watch(month, (newVal, oldVal) => {
//   console.log('City name changed:', newVal);
//   console.log('City name changed:', oldVal);
// });






const aaa = ref([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24, 25, 25, 29, 0, 5, 0, 0]);


const weatherTemp = [
  {
    "condition": "mid_rainy",
    "min_temp": 15,
    "max_temp": 28
  },
  {
    "condition": "night",
    "min_temp": 15,
    "max_temp": 28
  },
  {
    "condition": "sunny",
    "min_temp": 16,
    "max_temp": 27
  },
  {
    "condition": "small_rainy",
    "min_temp": 17,
    "max_temp": 28
  },
  {
    "condition": "big_rainy",
    "min_temp": 19,
    "max_temp": 30
  },
  {
    "condition": "night",
    "min_temp": 13,
    "max_temp": 25
  },
  {
    "condition": "sunny_cloudy",
    "min_temp": 21,
    "max_temp": 28
  },
  {
    "condition": "small_rainy",
    "min_temp": 14,
    "max_temp": 31
  },
  {
    "condition": "sunny_cloudy",
    "min_temp": 17,
    "max_temp": 30
  },
  {
    "condition": "mid_rainy",
    "min_temp": 21,
    "max_temp": 31
  },
  {
    "condition": "big_rainy",
    "min_temp": 14,
    "max_temp": 25
  },
  {
    "condition": "cloudy",
    "min_temp": 21,
    "max_temp": 27
  },
  {
    "condition": "big_rainy",
    "min_temp": 14,
    "max_temp": 28
  },
  {
    "condition": "mid_rainy",
    "min_temp": 15,
    "max_temp": 28
  },
  {
    "condition": "small_rainy",
    "min_temp": 21,
    "max_temp": 29
  },
  {
    "condition": "big_rainy",
    "min_temp": 20,
    "max_temp": 27
  },
  {
    "condition": "cloudy",
    "min_temp": 18,
    "max_temp": 27
  },
  {
    "condition": "small_rainy",
    "min_temp": 20,
    "max_temp": 29
  },
  {
    "condition": "cloudy",
    "min_temp": 15,
    "max_temp": 27
  },
  {
    "condition": "big_rainy",
    "min_temp": 15,
    "max_temp": 30
  },
  {
    "condition": "cloudy",
    "min_temp": 17,
    "max_temp": 25
  },
  {
    "condition": "big_rainy",
    "min_temp": 13,
    "max_temp": 25
  },
  {
    "condition": "big_rainy",
    "min_temp": 18,
    "max_temp": 29
  },
  {
    "condition": "small_rainy",
    "min_temp": 20,
    "max_temp": 27
  },
  {
    "condition": "cloudy",
    "min_temp": 17,
    "max_temp": 25
  },
  {
    "condition": "sunny_cloudy",
    "min_temp": 17,
    "max_temp": 29
  },
  {
    "condition": "mid_rainy",
    "min_temp": 18,
    "max_temp": 27
  },
  {
    "condition": "night",
    "min_temp": 21,
    "max_temp": 31
  },
  {
    "condition": "sunny_cloudy",
    "min_temp": 18,
    "max_temp": 28
  },
  {
    "condition": "small_rainy",
    "min_temp": 14,
    "max_temp": 29
  },
  {
    "condition": "night",
    "min_temp": 21,
    "max_temp": 26
  },
  {
    "condition": "small_rainy",
    "min_temp": 19,
    "max_temp": 31
  },
  {
    "condition": "mid_rainy",
    "min_temp": 21,
    "max_temp": 31
  }
];
// ------------------------------------------------------------------------------------------------
interface WeatherData41 {
    weather: Weather41;
}
interface Weather41{
    /**
     * 以百分之多少为单位
     */
    aqi: number;
    condition: string;
    /**
     * 降水量：mm
     */
    precip: number;
    /**
     * 降水概率：%
     */
    precip_probability: number;
    /**
     * 大气压强：hPa
     */
    pressure: number;
    /**
     * 中等，很强，较弱等
     */
    ray: string;
    /**
     * 示例：18:00
     */
    sunrise_time?: string;
    /**
     * 示例：18:00
     */
    sunset_time?: string;
    /**
     * ℃
     */
    temp: number;
    /**
     * ℃
     */
    temp_feel: number;
}
//     searchShow: boolean


let weather = ref<Weather41>({
aqi: 0,
condition: "",
precip: 0,
precip_probability: 0,
pressure: 0,
ray: "",
temp: 0,
temp_feel: 0
})
const get_his_overview = async () => {
    get<WeatherData41>("/api/weather/overview/", city).then((res) => {
        weather.value = res.data.weather;
        console.log(weather.value);
        // city.value = res.data.city;
        // searchShow.value = res.data.searchShow
    });
};

// const getData = () => {
//     get_his_overview();
//     get
// }
onMounted(() => {
    get_his_overview();
});


const displayInfo = computed(() => {
  return  [
    {
      name: '降水量',
      icon: '../src/assets/img/weather_his/cloudrain.png',
      data: weather.value.precip,
      unit: 'mm'
    },
    {
      name: '大气压强',
      icon: '../src/assets/img/weather_his/thermometer.png',
      data: weather.value.pressure,
      unit: 'hPa'
    },
    {
      name: '空气质量',
      icon: '../src/assets/img/weather_his/wind.png',
      data: weather.value.aqi,
      unit: 'AQI'
    },
    {
      name: '紫外线',
      icon: '../src/assets/img/weather_his/sunhorizon.png',
      data: weather.value.ray
    },
    {
      name: '日出时间',
      icon: '../src/assets/img/weather_his/sunhorizon.png',
      data: weather.value.sunrise_time
    },
    {
      name: '日落时间',
      icon: '../src/assets/img/weather_his/sunhorizon.png',
      data: weather.value.sunset_time
    }
  ];
});

// ------------------------------------------------------------------------------------------------
// function displayInfo(index: number) {
//   let weather = getWeather(index);
//   return [
//     {
//       name: '降水量',
//       icon: '../src/assets/img/weather_his/cloudrain.png',
//       data: weather.precip,
//       unit: 'mm'
//     },
//     {
//       name: '大气压强',
//       icon: '../src/assets/img/weather_his/thermometer.png',
//       data: weather.pressure,
//       unit: 'hPa'
//     },
//     {
//       name: '空气质量',
//       icon: '../src/assets/img/weather_his/wind.png',
//       data: weather.aqi,
//       unit: 'AQI'
//     },
//     {
//       name: '紫外线',
//       icon: '../src/assets/img/weather_his/sunhorizon.png',
//       data: weather.ray
//     },
//     {
//       name: '日出时间',
//       icon: '../src/assets/img/weather_his/sunhorizon.png',
//       data: weather.sunrise_time
//     },
//     {
//       name: '日落时间',
//       icon: '../src/assets/img/weather_his/sunhorizon.png',
//       data: weather.sunset_time
//     }
//   ];
// }


// onMounted(() => {
//   get_data();
//   // console.log("----------------------------------------------------------------")
//   // console.log(realTimeWeatherList);
// });

// const displayInfo = [
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
//   },
//   {
//     name: '日出时间',
//     icon: '../src/assets/img/weather_his/cloudrain.png',
//     data: 12,//props.weather.windSpeed,
//     unit: '%'
//   },
//   {
//     name: '日落时间',
//     icon: '../src/assets/img/weather_his/cloudrain.png',
//     data: 12,//props.weather.windSpeed,
//     unit: '%'
//   }
// ]
</script>

<!-- <script>
export default {
  mounted() {
    console.log(this.data); // 在这里打印出 data 的值
  }
}
</script> -->

<style scoped>
.is-selected {
  color: #1989fa;
}

/* .date-cell {
  position: relative;
  display: inline-block;
} */

.weather-icon {
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  /* 调整图片宽度 */
  height: 40px;
  /* 调整图片高度 */
}

/* from 首页 */
/* .grid-content {
  border-radius: 4px;
  min-height: 36px;
} */

/* .font1 {
  font-size: 14px;
} */

.el-card {
  background-color: rgb(240, 240, 250);
  /* margin: 0px; */
  margin-top: 30px;
  border-radius: 20px;
  font-family: 'Courier New', Courier, monospace
}

.el-calendar {
  background: linear-gradient(to right, #dee5f8, #f4e2e2);
  border-radius: 20px;
  font-family: 'Courier New', Courier, monospace
}
</style>
