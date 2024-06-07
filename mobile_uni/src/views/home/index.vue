<!-- <template>
  <el-tabs
    v-model="activeName"
    class="demo-tabs mx-5 rounded-2xl"
    @tab-click="handleClick"
    type="border-card"
  >
  <el-tabs v-model="activeName" style="margin-left: 1%;margin-right: 1%;" class="demo-tabs mx-40 rounded-2xl"
    @tab-click="handleClick" type="border-card">
    <el-tab-pane label="天气速览" name="first">
      <overview />
    </el-tab-pane>
    <el-tab-pane label="30日天气" name="second">
      <calendar30 />
    </el-tab-pane>
    <el-tab-pane label="空气质量" name="third">
      <AirQualityVM />
    </el-tab-pane>
  </el-tabs>

</template> -->

<template>
  <!-- <div style="color: white;"> {{mapRainyWeather(weather.condition)}}</div> -->
  <!-- bg-mobile-sunny bg-mobile-rainy  bg-mobile-night bg-mobile-cloudy bg-mobile-overcast-->
  <div :class="mapRainyWeather(weather.condition)" class="bg-cover bg-no-repeat" style="height: auto;overflow: auto">
    <el-container class="background-transparent">
      <el-button class="switch-button background-transparent" size="small" type="info" :icon="Switch"
        @click="drawer = true">
        切换城市
      </el-button>
      <el-header style="height: auto;">
        <!-- <el-col :span="16"> -->
        <CurrentWeather class="weather-left md:basis-5/5" :weather="weather" :city="city" :search="searchShow">
        </CurrentWeather>
        <!-- </el-col> -->
        <!-- <el-col :span="8"> -->
        <!-- <CurrentWeatherRight class="weather-right md:basis-3/5" :weather="weather" /> -->
        <!-- </el-col> -->
      </el-header>
      <el-main style="padding: 0;">
        <el-card class="scroll"
          style="border-color: transparent;background-color: rgba(255, 255, 255, 0);border-radius: 10px;">
          <RealTimeBroadcast :city="city" />
        </el-card>
      </el-main>
      <el-footer style="height: auto;">
        <!-- <el-main style="width: 800px;"> -->
        <el-card
          style="background-color: rgba(255, 255, 255, 0.2); /* 白色背景，透明度为 50% */border-color: transparent;border-radius: 30px;margin: 30px;margin-top: -10px;">
          <BriefAqi :city="city" />
        </el-card>
        <!-- </el-main> -->

      </el-footer>
    </el-container>
  </div>
  <!-- </div> -->



  <el-drawer v-model="drawer" direction="utd" style="width: 100%;">
    <template #header="{ close, titleId, titleClass }">
      <div :id="titleId" :class="titleClass" class="drawer-header">关心的城市</div>
      <el-button class="add-button" type="info" @click="dialogVisible = true" :icon="Plus" />
    </template>
    <div>
      <el-card class="drawer-card" @click="selectCity(currentCity.city, -1)">
        <div class="drawer-card-content">
          <span>{{ currentCity.city.adm2 }}&nbsp;&nbsp;</span>
          <span>{{ currentCity.city.name }}</span>
          <span class="temperature">{{ currentCity.temp }}°C</span>
          <el-button @click="" type="" size="small" :icon="House" class="pink-button" />
        </div>
      </el-card>
      <el-card v-for="(cityItem, index) in careCitiesList" :key="index" class="drawer-card"
        @click="selectCity(cityItem.city, index)" :class="{ 'selected-card': index === selectedCityIndex }">
        <div class="drawer-card-content">
          <span>{{ cityItem.city.adm2 }}&nbsp;&nbsp;</span>
          <span>{{ cityItem.city.name }}</span>
          <span class="temperature">{{ cityItem.temp }}°C</span>
          <el-button @click="removeCity(index)" type="info" size="small" :icon="Delete" />
        </div>
      </el-card>
    </div>
  </el-drawer>

  <el-dialog v-model="dialogVisible" title="添加关心城市" width="350">
    <el-row>
      <el-col :span="1">
        <el-icon class="search-icon" />
      </el-col>
      <el-col :span="21">
        <el-autocomplete v-model="state" :fetch-suggestions="querySearch" clearable class="autocomplete-input"
          @select="handleSelect" highlight-first-item :value-key="'label'" />
      </el-col>
    </el-row>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfirm">
          确定
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>





<script lang="ts" setup>
import { post, get } from "@/api/index.ts";
import SearchLocation from "@/components/weather_details/sub_components/SearchLocation.vue";
import RealTimeBroadcast from "@/components/weather_details/sub_components/RealTimeBroadcast.vue";
import CurrentWeather from "@/components/weather_details/sub_components/CurrentWeather.vue";
import CurrentWeatherRight from "@/components/weather_details/sub_components/CurrentWeatherRight.vue";
import BriefAqi from '@/components/weather_details/sub_components/BriefAqi.vue';
import CityRanking from '@/components/weather_details/sub_components/CityRanking.vue';
import { Switch } from '@element-plus/icons-vue'
// const careCitiesList = ref([])
const city = ref<City>({
  name: '北京市',
  adm2: '北京'
});
const currentCity = ref<CareCity>()
const careCitiesList = ref<CareCity[]>([])
const weather = ref<Weather41>({
  aqi: 0,
  humidity: 0,
  condition: '',
  condition_icon: 0,
  precip: 0,
  precip_probability: 0,
  pressure: 0,
  ray: '',
  temp: 0,
  temp_feel: 0
});
const searchShow = ref(false)

// interface接口
interface City {
  name: string;
  adm2: string;
}
interface WeatherData41 {
  weather: Weather41;
}
interface Weather41 {
  aqi: number;
  humidity: number;
  condition: string;
  condition_icon: number;
  precip: number;
  precip_probability: number;
  pressure: number;
  ray: string;
  sunrise_time?: string;
  sunset_time?: string;
  temp: number;
  temp_feel: number;
}
interface careCitiesData {
  success: boolean;
  currentCity: CareCity;
  careCitiesList: CareCity[];
}
interface CareCity {
  city: City;
  cond_icon: string;
  temp: number;
}

const get_care_cities = async () => {
  get<careCitiesData>("/api/weather/care_cities/summary/").then((res) => {
    // if (res.data.success) {
    currentCity.value = res.data.currentCity;
    careCitiesList.value = res.data.careCitiesList;
    city.value = res.data.currentCity.city;
    // 清楚选中标记，默认指向当前城市
    selectedCityIndex.value = -1;
    // console.log(careCitiesList.value);
    // console.log(city.value);
    // }
    // else 调用/api/current_city/接口
  });
};
const get_overview_data = async () => {
  get<WeatherData41>("/api/weather/overview/", { city: city.value }).then((res) => {
    weather.value = res.data.weather;
    console.log(weather.value);
  });
};
onMounted(() => {
  get_care_cities();
  setTimeout(() => {
    get_overview_data();
  }, 300);
});

watch(city, () => {
  get_overview_data();
}, { deep: true })

// 根据天气换壁纸

const weatherMap = {
  '晴': 'bg-mobile-sunny',
  // '下雨': 'bg-mobile-rainy',
  // '夜晚': 'bg-mobile-night',
  '多云': 'bg-mobile-cloudy',
  '阴': 'bg-mobile-overcast'
};
// 根据 *雨* 的通配映射到 bg-mobile-rainy
function mapRainyWeather(chineseWeather: string): string {
  const currentTime = new Date().getHours();
  if (chineseWeather.includes('雨')) {
    return 'bg-mobile-rainy';
  } else if (currentTime >= 20 || currentTime < 5) { // 如果当前时间为晚上（20:00-06:00），返回对应的夜晚背景
    return 'bg-mobile-night';
  } else {
    return weatherMap[chineseWeather] || 'bg-mobile-sunny'; // 如果没有对应的映射，返回 'Unknown'
  }
}

// 抽屉
import { Delete, House, Plus } from "@element-plus/icons-vue";
const drawer = ref(false)
const drawerVisible = ref(false);

const closeDrawer = () => {
  drawerVisible.value = false;
};

// const removeCity = (index: number) => {
//   careCitiesList.value = careCitiesList.value.filter((city) => city.id !== id);

// };

const removeCity = (index: number) => {
  if (index >= 0 && index < careCitiesList.value.length) {
    // POST request
    interface DeleteResponse {
      success: boolean;
      reason?: string;
    }
    const request: City = careCitiesList.value[index].city;
    post<DeleteResponse>("/api/weather/care_cities/del/", request).then((res) => {
      // const response = res.data;
      //   if (response.success) {
      //     ElMessage.success("已删除");
      //   } else ElMessage.error("无效的请求");
    });

    careCitiesList.value.splice(index, 1);

  }
};
const selectedCityIndex = ref(null);
const selectCity = (selectedCity: City, index: number) => {
  city.value = selectedCity;
  selectedCityIndex.value = index;
};

// 对话框
import { ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
// import searchCity from "@/components/topBar/searchCity.vue"

const tempSelectedCity = ref<City>({
  name: "",
  adm2: ""
});
const dialogVisible = ref(false)

// const temp0 = ref(0);
// const get_overview_data_1 = async () => {
//   get<WeatherData41>("/api/weather/overview/", { city: tempSelectedCity.value }).then((res) => {
//     temp0.value = res.data.weather.temp;
//   });
// };
const handleConfirm = () => {
  // 将选择的城市添加到列表中
  if (tempSelectedCity.value) {
    // POST request
    interface AddResponse {
      status: boolean;
      reason?: string;
    }
    post<AddResponse>("/api/weather/care_cities/add/", { city: tempSelectedCity.value }).then((res) => {
    console.log(tempSelectedCity.value);
      // const response = res.data;
      // if (response.status) {
      //   ElMessage.success("已添加");
      //   // 刷新重新调用接口
      // } else ElMessage.error("无效的请求");
      // get_care_cities();
    });

    setTimeout(() => {
      get_care_cities();
  }, 300);

  }
  // 关闭对话框
  dialogVisible.value = false;
};
// const temp0 = ref(0);
// get<WeatherData41>("/api/weather/overview/", { city: tempSelectedCity.value }).then((res) => {
//   temp0.value = res.data.weather.temp;
// });
// get_overview_data_1();
// const cityTemp = tempSelectedCity.value;
// const tempTemp = temp0.value
// let selectedCareCity: CareCity = {
//   city: cityTemp,
//   cond_icon: "",
//   temp: tempTemp
// }
// careCitiesList.value.push(selectedCareCity);

import { ref, onMounted } from 'vue';



import { china_cities } from "@/stores/cities";
import { CityWeatherData } from "@/types/weather";
// onMounted(() => {
//   getPresentCity();
// });
interface CityInfoResponse {
  status: boolean;
  message: CityWeatherData;
}
// const currentCity = ref("");
// const getPresentCity = async () => {
//   get<CityInfoResponse>("/api/current/getCityInfo/").then((res) => {
//     currentCity.value = res.data.message.city;
//   });
//   if (!currentCity.value) {
//     currentCity.value = "北京市";
//   }
// };
interface LabelItem {
  label: string;
  value: string;
}
const state = ref("");

const labels = ref<LabelItem[]>([]);
const querySearch = (queryString: string, cb: any) => {
  const results = queryString
    ? labels.value.filter(createFilter(queryString))
    : labels.value;
  cb(results);
};

const createFilter = (queryString: string) => {
  return (restaurant: LabelItem) => {
    return (
      restaurant.label.toLowerCase().indexOf(queryString.toLowerCase()) === 0
    );
  };
};
const loadAll = () => {
  return china_cities;
};


const handleSelect = (item: LabelItem) => {
  state.value = item.label;
  var splitStr=item.label.split(' ')
  tempSelectedCity.value.name = splitStr[0];
  tempSelectedCity.value.adm2 = splitStr[1];
};

interface CityInfoResponse {
  success: boolean;
  reason?: string;
}

onMounted(() => {
  labels.value = loadAll();
});


// const careCitiesList = ref<City[]>([
//   { id: 1, adm2: '海淀区', name: '北京', temperature: 25 },
//   { id: 2, adm2: '黄浦区', name: '上海', temperature: 28 },
//   { id: 3, adm2: '天河区', name: '广州', temperature: 30 },
// ]);
// console.log("----------------------------------------------------------------")
// console.log(weather.value);

</script>

<!-- <script lang="ts" setup>
import type { TabsPaneContext } from "element-plus";
import RealTimeBroadcast from "@/components/weather_details/sub_components/RealTimeBroadcast.vue";
import CurrentWeather from "@/components/weather_details/sub_components/CurrentWeather.vue";
import CurrentWeatherRight from "@/components/weather_details/sub_components/CurrentWeatherRight.vue";

/*抽屉页*/
const activeName = ref("first");

import overview from "@/components/weather_details/overview.vue";
import calendar30 from "@/components/weather_details/calendar30.vue";
import AirQualityVM from "@/components/airQuality/AirQualityVM.vue";
import dataStatistics from "@/components/dataStatistics/dataStatistics.vue";
</script> -->


<style scoped>
.scroll {
  /* height: calc(100vh - 285px); */
  height: auto;
  overflow: auto;
  width: 100%;
}

.scroll::-webkit-scrollbar {
  display: none;
}

/* .el-card__body {
  box-shadow: none;
  padding: 0;
} */

.background-transparent {
  background: transparent;
  border-color: transparent;
}

.max-md-bg-gradient {
  background-image: linear-gradient(to right, #67E1D2, #54A8FF);
  box-shadow: 0 10px 30px -12px rgba(7, 89, 133, 0.45);
}

.el-footer {
  padding: 0px;
}

.card-style {
  /* min-height: 20vh;
  max-height: 44vh;
  margin-bottom: 15px; */
  /* min-height: 20vh; */
  /* max-height: 1144vh; */
  /* margin-bottom: 15px; */
  /* overflow: auto; */
  /* max-width: 100%; */
}

/* style="min-height: 20vh;max-height: 44vh;margin-bottom:15px;" */

.margin-container {
  /* margin-left: 1%;
  margin-right: 1%; */
  /* max-height: 100vh; */
  /* overflow: auto; */
  border-radius: 5px;
}

.container-style {
  background: white;
}

.bg-style {
  background: rgb(54, 131, 195);
  height: 44.5vh;
}

.weather-left,
.weather-right {
  flex: 1;
}

.drawer-header {
  font-size: 20px;
  color: black;
  text-align: center;
}

.add-button {
  margin-top: 10px;
}

.drawer-card {
  background: linear-gradient(rgb(13, 104, 188), rgb(54, 131, 195));
  margin-bottom: 10px;
  border-radius: 10px;
  color: white;
  cursor: pointer;
}

.drawer-card-content {
  font-size: small;
  display: flex;
  align-items: center;
}

.temperature {
  flex: 1;
  text-align: center;
}

.pink-button {
  background: pink;
}

.search-icon {
  margin-top: 10px;
}

.selected-card {
  border: 2px solid rgb(183, 255, 0);
  /* 修改为你想要的边框颜色 */
  margin-left: -10px;
  margin-right: -10px;
}

.chart {
  width: 95%;
  height: 92%;
  background: linear-gradient(to bottom, #ffffff, #ffffff);
  margin: 0 auto;
}

h2 {
  text-align: center;
  margin: 0;
  font-size: 18px;
  color: #000;
}


/* demo */

.input {
  width: 300px;
  margin-top: 20px;
}

.temp {
  font-size: 79px;
  color: white;
}
</style>


<!-- <template>
  <div>
    <SearchCity />
  </div>
</template>

<script setup lang="ts">
const SearchCity = defineAsyncComponent(
  () => import("@c/topBar/searchCity.vue")
);
</script>

<style scoped></style> -->
