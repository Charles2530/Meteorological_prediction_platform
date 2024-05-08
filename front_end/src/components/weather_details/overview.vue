<template>
    <el-container class="container rounded-lg">
        <CurrentWeather class="md:basis-3/5 " :weather="weather" :city="city" :search="searchShow">
            <!-- @searchShow="changeSearchShow" -->
            <!-- <template v-slot:search>
              <div class="text-[#333333]">
                <SearchLocation :show="searchShow" @searchShow="changeSearchShow" @search="locationBySearch" />
              </div>
            </template> -->
        </CurrentWeather>
        <CurrentWeatherRight class="md:basis-2/5" :weather="weather" />
        <!-- @refresh="weatherInfo"  -->
    </el-container>
    <el-container class="">
        <RealTimeBroadcast/>
    </el-container>
</template>
<script lang="ts" setup>



import { ref, onMounted } from 'vue';

/** 组件  **/
import SearchLocation from '@/components/weather_details/sub_components/SearchLocation.vue'
import CurrentWeather from '@/components/weather_details/sub_components/CurrentWeather.vue';
import CurrentWeatherRight from '@/components/weather_details/sub_components/CurrentWeatherRight.vue';
import Forecast from '@/components/weather_details/sub_components/Forecast.vue'
import RealTimeBroadcast from '@/components/weather_details/sub_components/RealTimeBroadcast.vue'
const stateNavigator = ref(0) // 用于判断是否加载loading
const cityList = ref([])
const city = ref({
    name: '北京市',
    adm2: '昌平区'
});
let weather = ref({})
const air = ref({})
const forecast = ref([])
const preDayWeather = ref([])
const ultraviolet = ref([])
const searchShow = ref(false)


// interface City {
//     name: string;
//     adm2: string;
// }


interface WeatherHisOverview {
    weather: Weather;
}
interface Weather{
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



import { post, get } from "@/api/index.ts";
const get_his_overview = async () => {
    get<WeatherHisOverview>("/api/weather/overview/", city).then((res) => {
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
console.log("----------------------------------------------------------------")
// console.log(weather.value);

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


.demo-tabs>.el-tabs__content {
    padding: 32px;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
}

/* demo */
.container {
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