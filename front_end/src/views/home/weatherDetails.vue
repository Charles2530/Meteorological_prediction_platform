<template>
<el-tabs  v-model="activeName" class="demo-tabs mx-40 rounded-2xl " @tab-click="handleClick" type="border-card">
    <el-tab-pane label="天气速览" name="first">
      <overview />
    </el-tab-pane>
    <el-tab-pane label="30日天气" name="second">
      <calendar30 />
    </el-tab-pane>
    <el-tab-pane label="空气质量" name="third">
      <AirQualityVM />
    </el-tab-pane>
    <el-tab-pane label="数据统计" name="fourth">
      <dataStatistics />
    </el-tab-pane>
  </el-tabs>
</template>
<script lang="ts" setup>
import { ref, onMounted } from "vue";
import type { TabsPaneContext } from "element-plus";
import * as echarts from "echarts";
/*抽屉页*/
const activeName = ref("first");
const handleClick = (tab: TabsPaneContext, event: Event) => {
  console.log(tab, event);
};
type ECharts = echarts.ECharts;
let echartsInstance: Ref<ECharts | null> = ref(null);

/** 组件  **/
import overview from '@/components/weather_details/overview.vue'
import calendar30 from '@/components/weather_details/calendar30.vue'
import aqi from '@/components/weather_details/aqi.vue'
import statistics from '@/components/weather_details/statistics.vue'
import SearchLocation from "@/components/raw/SearchLocation.vue";
import CurrentWeather from "@/components/raw/CurrentWeather.vue";
import AirQuality from "@/components/raw/AirQuality.vue";
import AirQualityVM from "@/components/airQuality/AirQualityVM.vue";
import dataStatistics from "@/components/dataStatistics/dataStatistics.vue";
import Forecast from "@/components/raw/Forecast.vue";
const stateNavigator = ref(0); // 用于判断是否加载loading
const cityList = ref([]);
const city = ref({});
const weather = ref({});
const air = ref({});
const forecast = ref([]);
const preDayWeather = ref([]);
const ultraviolet = ref([]);
const searchShow = ref(false);

//----------
import type { CalendarDateType, CalendarInstance } from "element-plus";

const calendar = ref<CalendarInstance>();
const selectDate = (val: CalendarDateType) => {
  if (!calendar.value) return;
  calendar.value.selectDate(val);
};

// export default {
//     mounted () {
//         // 组件挂载时，进行默认数据的初始化
//         axios.defaults.baseURL = '/myApi'
//         requestData()
//     },
//     data() {
//         return {
//             city:"上海",
//             weatherData:{},
//             todayData:{},
//             plc:"暂无数据",
//             realtime:{},
//             futureData:[]
//         }
//     },
//     watch: {
//         // 当用户输入的城市发生变化后，调用接口进行数据请求
//         city() {
//             requestData()
//         }
//     },
//     methods: {
//         requestData() {
//             let city = encodeURI(city)
//             let api = `/simpleWeather/query?city=${city}&key=cffe158caf3fe63aa2959767a503bbfe`
//             axios.get(api).then((response: { data: any; })=>{
//                 weatherData = response.data
//                 todayData = weatherData.result.future[0]
//                 realtime = weatherData.result.realtime
//                 futureData = weatherData.result.future
//                 console.log(response.data)
//             })
//         }
//     }
// }
</script>
<style>
.chart {
  width: 95%;
  height: 92%;
  background: linear-gradient(to bottom, #ffffff, #ffffff);
  margin: 0 auto;
  /* display: flex; */
  /* justify-content: center; */
}

h2 {
  text-align: center;
  margin: 0;
  font-size: 18px;
  color: #000;
}

/*  */

.demo-tabs > .el-tabs__content {
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
