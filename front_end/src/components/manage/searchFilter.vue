<template>
  <div class="p-2 space-y-4">
    <el-row>
      <el-col :span="10">
        <el-collapse v-model="filterVisible" accordion>
          <el-collapse-item title="请选择过滤参数" name="filter">
            <div class="space-y-2">
              <div class="my-2"></div>
              <el-select v-model="selectType" placeholder="请选择类型">
                <el-option label="天气数据" value="weather"></el-option>
                <el-option label="地质灾害" value="disaster"></el-option>
              </el-select>
              <el-select
                v-model="timeOption"
                placeholder="请选择时间选项"
                v-if="selectType === 'weather'"
              >
                <el-option label="按月" value="month"></el-option>
                <el-option label="按日" value="day"></el-option>
                <el-option label="按周" value="week"></el-option>
              </el-select>
              <el-date-picker
                v-model="selectedDate"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                :picker-options="pickerOptions"
                format="YYYY年MM月DD日"
              ></el-date-picker>
              <el-select v-model="selectedLocation" placeholder="请选择地点">
                <el-option
                  v-for="location in locations"
                  :key="location.value"
                  :label="location.label"
                  :value="location.value"
                ></el-option>
              </el-select>
            </div>
          </el-collapse-item>
        </el-collapse>
      </el-col>
      <el-col :span="4"></el-col>
      <el-col :span="10" class="text-right">
        <el-input
          v-model="searchQuery"
          placeholder="请输入搜索关键词"
          clearable
          @clear="handleSearch"
        >
          <template #append>
            <el-button @click="handleSearch">
              <el-icon class="mr-2"><Search></Search></el-icon>
              搜索</el-button
            >
          </template>
        </el-input>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { post } from "@/api/index";
import { china_cities } from "@/stores/cities";
const selectedDate = ref("");
const pickerOptions: any = {
  firstDayOfWeek: 1,
  disabledDate(time: Date): boolean {
    return time.getTime() > Date.now();
  },
};
const searchQuery = ref("");
const filterVisible = ref("false");
const selectType = ref("");
const timeOption = ref("");
const selectedLocation = ref("");
const locations = china_cities;
interface SearchWeatherHourlyListResponse {
  status: boolean;
  weatherHourlyList: WeatherTable[];
}
interface WeatherTable {
  time: string;
  temp: string;
  text: string;
  precip: string;
  wind360: string;
  windScale: string;
  windSpeed: string;
  humidity: string;
  pressure: string;
  aqi: string;
  category: string;
}
const weatherTable: WeatherTable[] = reactive([]);

const handleSearch = () => {
  post<SearchWeatherHourlyListResponse>("/api/manage/data/search/", {
    key: searchQuery.value,
    type: selectType.value,
    range: timeOption.value,
    time: selectedDate.value,
    address: selectedLocation.value,
  }).then((res) => {
    if (res.status) {
      weatherTable.splice(
        0,
        weatherTable.length,
        ...res.data.weatherHourlyList
      );
    }
  });
};
</script>

<style>
.el-collapse-item__header {
  padding-left: 10px;
  margin: 0%;
  height: 30px;
  border-radius: 5px;
}

.el-collapse-item__header.is-active {
  background-color: #fffff0;
}
</style>
