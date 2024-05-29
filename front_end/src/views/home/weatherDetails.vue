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
  <div class="common-layout" style="margin-left: 1%;margin-right: 1%;max-height:100vh;overflow: auto;">
    <el-container style="background: white">
      <el-aside width="70%">
        <el-button size="small" type="" :icon="Switch" style="margin-left: 16px" @click="drawer = true">
          切换城市
        </el-button>
        <el-container class="rounded-lg" style="background: rgb(54, 131, 195);height: 40vh;margin-top: 0px;">
          <!-- <el-col :span="16"> -->
          <CurrentWeather class="md:basis-3/5" :weather="weather" :city="city" :search="searchShow">
          </CurrentWeather>
          <!-- </el-col> -->
          <!-- <el-col :span="8"> -->
          <CurrentWeatherRight class="md:basis-2/5" :weather="weather" />
          <!-- </el-col> -->
        </el-container>
        <el-card style="min-height: 20vh;max-height: 50vh;">
          <RealTimeBroadcast :city="city"/>
        </el-card>
      </el-aside>

      <el-main style="width: 800px;">
        <el-card>
          <BriefAqi :city="city"/>
        </el-card>
        <el-card style="max-height:58vh;overflow: auto;">
          <CityRanking />
        </el-card>
      </el-main>
    </el-container>
  </div>



  <el-drawer v-model="drawer" direction="ltr" @close="handleDrawerClose">
    <template #header="{ close, titleId, titleClass }">
      <div :id="titleId" :class="titleClass" style="font-size: 20px;color:black; text-align: center;  ">关心的城市</div>
      <el-button type="info" @click="dialogVisible = true" :icon="Plus" />
    </template>
    <div>
      <el-card :style="{
        background: 'linear-gradient(rgb(13, 104, 188), rgb(54, 131, 195))', marginBottom: '10px',
        borderRadius:
          '10px', color: 'white'
      }" @click="selectCity(currentCity.city,-1)">
        <div style="display: flex; align-items: center;">
          <span>{{ currentCity.city.adm2 }}&nbsp;&nbsp;</span>
          <span>{{ currentCity.city.name }}</span>
          <span style="flex: 1; text-align: center;">{{ currentCity.temp }}°C</span>
          <el-button @click="" type="" size="small" :icon="House" style="background: pink;" />
        </div>
      </el-card>
      <el-card v-for="(cityItem, index) in careCitiesList" :key="index"
        :style="{
          background: 'linear-gradient(rgb(13, 104, 188), rgb(54, 131, 195))', marginBottom: '10px', borderRadius: '10px', color: 'white'
        }"
        @click="selectCity(cityItem.city,index)" 
        :class="{ 'selected-card': index === selectedCityIndex }">
        <div style="display: flex; align-items: center;">
          <span>{{ cityItem.city.adm2 }}&nbsp;&nbsp;</span>
          <span>{{ cityItem.city.name }}</span>
          <span style="flex: 1; text-align: center;">{{ cityItem.temp }}°C</span>
          <el-button @click="removeCity(index)" type="info" size="small" :icon="Delete" />
        </div>
      </el-card>
    </div>
  </el-drawer>

  <el-dialog v-model="dialogVisible" title="添加关心城市" width="500">
    <!-- <span>This is a message</span> -->
    <!-- <div class="flex justify-center">
      <el-card style="width: 80%;">
        <el-icon style=" display: flex; align-items: center;justify-items: center">
          <Search />
        </el-icon>
        <el-autocomplete style="width: 80%;" v-model="state" :fetch-suggestions="querySearch" clearable
          class="inline-input w-100" @select="handleSelect" highlight-first-item :value-key="'label'"
          @change="updateUserCity" />
      </el-card>
    </div> -->
    <el-row>
      <el-col :span="1">
        <el-icon style=" margin-top: 10px;">
          <Search />
        </el-icon>
      </el-col>
      <el-col :span="21">
        <el-autocomplete style="width: 100%;" v-model="state" :fetch-suggestions="querySearch" clearable
          class="inline-input w-100" @select="handleSelect" highlight-first-item :value-key="'label'"
          @change="updateUserCity" />
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
  name: '市',
  adm2: '区'
});
const currentCity = ref<careCity>()
const careCitiesList = ref<careCity[]>([])
const weather = ref({})
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
  condition: string;
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
  currentCity: careCity;
  careCitiesList: careCity[];
}
interface careCity {
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
    console.log(careCitiesList.value);
    console.log(city.value);
    // }
    // else 调用/api/current_city/接口
  });
};
const get_overview_data = async () => {
  get<WeatherData41>("/api/weather/overview/", { city: city }).then((res) => {
    weather.value = res.data.weather;
    console.log(weather.value);
  });
};
onMounted(() => {
  get_care_cities();
  get_overview_data();
});
// 抽屉
import { Delete, House, Plus } from "@element-plus/icons-vue";
const drawer = ref(false)
const drawerVisible = ref(false);

// const selectedCity = ref('');

const closeDrawer = () => {
  drawerVisible.value = false;
};

// const removeCity = (index: number) => {
//   careCitiesList.value = careCitiesList.value.filter((city) => city.id !== id);

// };
const removeCity = (index: number) => {
  if (index >= 0 && index < careCitiesList.value.length) {
    careCitiesList.value.splice(index, 1);
    // POST request
  }
};
const selectedCityIndex = ref(null);
const selectCity = (selectedCity: City,index:number) => {
  city.value = selectedCity;
  selectedCityIndex.value = index;
};
const handleDrawerClose = () => {
  // 调用刷新函数
  refreshData();
};
const refreshData = () => {
  get_overview_data();
};

// 对话框

import { ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
// import searchCity from "@/components/topBar/searchCity.vue"

const dialogVisible = ref(false)

const handleConfirm = () => {
  // 将选择的城市添加到列表中
  if (selectedCity.value) {
    cityList.value.push(selectedCity.value);
  }
  // 关闭对话框
  dialogVisible.value = false;
};

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
const tempSelectedCity = ref("");

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
  tempSelectedCity.value = item.value;
};

interface CityInfoResponse {
  success: boolean;
  reason?: string;
}
const updateUserCity = async () => {
  post<CityInfoResponse>("/api/operate/current_city", {
    city: state.value,
  }).then((res) => {
    if (res.data.success) {
      getPresentCity();
    }
  });
};
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

<!-- !!!因为涉及到组件也要使用下面的css样式，所以不要scoped不然丑 -->
<style>
.selected-card {
  /* border: 2px solid rgb(183, 255, 0); 修改为你想要的边框颜色 */
  margin-left: -20px;
  margin-right: -20px;
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

/*  */

.demo-tabs>.el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

/* demo */
.weather_container {
  background: linear-gradient(rgb(13, 104, 188), rgb(54, 131, 195));
}

.input {
  width: 300px;
  margin-top: 20px;
}

.today {
  font-size: 20px;
  color: white;
}

.temp {
  font-size: 79px;
  color: white;
}

.realInfo {
  color: white;
}

.future {
  margin-top: 40px;
}

.header {
  color: white;
  font-size: 27px;
}
</style>
