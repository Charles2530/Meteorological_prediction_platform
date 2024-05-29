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
          <RealTimeBroadcast />
        </el-card>
      </el-aside>

      <el-main style="width: 800px;">
        <el-card>
          <BriefAqi />
        </el-card>
        <el-card style="max-height:58vh;overflow: auto;">
          <CityRanking />
        </el-card>
      </el-main>
    </el-container>
  </div>



  <el-drawer v-model="drawer" direction="ltr">
    <template #header="{ close, titleId, titleClass }">
      <div :id="titleId" :class="titleClass" style="font-size: 20px;color:black; text-align: center;  ">关心的城市</div>
      <el-button type="info" @click="dialogVisible = true" :icon="Plus" />
    </template>
    <div>
      <el-card v-for="city in cityList" :key="city.id"
        :style="{ background: 'linear-gradient(rgb(13, 104, 188), rgb(54, 131, 195))', marginBottom: '10px', borderRadius: '10px', color: 'white' }"
        @click="selectCity(city.name)">
        <div style="display: flex; align-items: center;">
          <span>{{ city.adm2 }}&nbsp;&nbsp;</span>
          <span>{{ city.name }}</span>
          <span style="flex: 1; text-align: center;">{{ city.temperature }}°C</span>
          <el-button @click="removeCity(city.id)" type="info" size="small" :icon="Delete" />
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
        <el-button type="primary" @click="dialogVisible = false">
          确定
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>






<script lang="ts" setup>
// 抽屉
import { Delete, Plus } from "@element-plus/icons-vue";
const drawerVisible = ref(false);
const cityList = ref<City[]>([
  { id: 1, adm2: '海淀区', name: '北京', temperature: 25 },
  { id: 2, adm2: '黄浦区', name: '上海', temperature: 28 },
  { id: 3, adm2: '天河区', name: '广州', temperature: 30 },
]);
const selectedCity = ref('');

const closeDrawer = () => {
  drawerVisible.value = false;
};

const removeCity = (id: number) => {
  cityList.value = cityList.value.filter((city) => city.id !== id);
  // POST request
};

const selectCity = (name: string) => {
  selectedCity.value = name;
};


// 对话框

import { ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
// import searchCity from "@/components/topBar/searchCity.vue"

const dialogVisible = ref(false)

const handleClose = (done: () => void) => {
  ElMessageBox.confirm('Are you sure to close this dialog?')
    .then(() => {
      done()
    })
    .catch(() => {
      // catch error
    })
}

import { ref, onMounted } from 'vue';



import { china_cities } from "@/stores/cities";
import { CityWeatherData } from "@/types/weather";
onMounted(() => {
  getPresentCity();
});
interface CityInfoResponse {
  status: boolean;
  message: CityWeatherData;
}
const currentCity = ref("");
const getPresentCity = async () => {
  get<CityInfoResponse>("/api/current/getCityInfo/").then((res) => {
    currentCity.value = res.data.message.city;
  });
  if (!currentCity.value) {
    currentCity.value = "北京市";
  }
};
interface LabelItem {
  label: string;
  value: string;
}
const state = ref("");
// const city = ref("");

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

// const handleSelect = (item: LabelItem) => {
//   state.value = item.label;
//   city.value = item.value;
// };
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

/** 组件  **/
import SearchLocation from "@/components/weather_details/sub_components/SearchLocation.vue";
import RealTimeBroadcast from "@/components/weather_details/sub_components/RealTimeBroadcast.vue";
import CurrentWeather from "@/components/weather_details/sub_components/CurrentWeather.vue";
import CurrentWeatherRight from "@/components/weather_details/sub_components/CurrentWeatherRight.vue";
import BriefAqi from '@/components/airQuality/BriefAqi.vue';
import CityRanking from '@/components/weather_details/sub_components/CityRanking.vue';
import { Switch } from '@element-plus/icons-vue'
// const cityList = ref([])
const city = ref({
  name: '北京市',
  adm2: '海淀区'
});
let weather = ref({})
const air = ref({})
const forecast = ref([])
const preDayWeather = ref([])
const ultraviolet = ref([])
const searchShow = ref(false)

const drawer = ref(false)

// interface City {
//     name: string;
//     adm2: string;
// }


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
//     searchShow: boolean



import { post, get } from "@/api/index.ts";
const get_his_overview = async () => {
  get<WeatherData41>("/api/weather/overview/", city).then((res) => {
    weather.value = res.data.weather;
    console.log(weather.value);
    // city.value = res.data.city;
    // searchShow.value = res.data.searchShow
  });
};


onMounted(() => {
  get_his_overview();
});
console.log("----------------------------------------------------------------")
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
