<template>
  <el-container class="panel background-white rounded-lg">
    <el-main class="no-padding" style="overflow: hidden">
      <div class="search-container mx-4">
        <el-row>
          <el-col :span="19">
            <div class="p-2 space-y-4">
              <el-row>
                <el-col :span="10">
                  <!-- 过滤器 -->
                  <el-collapse v-model="filterVisible" accordion>
                    <el-collapse-item title="请选择过滤参数" name="filter">
                      <div class="space-y-2">
                        <div class="my-2"></div>
                        <!-- 类型选择 -->
                        <el-select
                          v-model="selectType"
                          placeholder="请选择类型"
                        >
                          <el-option
                            label="天气数据"
                            value="weather"
                          ></el-option>
                          <el-option
                            label="地质灾害"
                            value="disaster"
                          ></el-option>
                        </el-select>
                        <!-- 时间选项 -->
                        <el-select
                          v-model="timeOption"
                          placeholder="请选择时间选项"
                          v-if="selectType === 'weather'"
                        >
                          <el-option label="按月" value="month"></el-option>
                          <el-option label="按日" value="day"></el-option>
                          <el-option label="按周" value="week"></el-option>
                        </el-select>
                        <!-- 时间段选择 -->
                        <el-date-picker
                          v-model="selectedDate"
                          type="daterange"
                          range-separator="至"
                          start-placeholder="开始日期"
                          end-placeholder="结束日期"
                          :picker-options="pickerOptions"
                          format="YYYY年MM月DD日"
                        ></el-date-picker>
                        <!-- 地点选择 -->
                        <el-select
                          v-model="selectedLocation"
                          placeholder="请选择地点"
                        >
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
                  <!-- 主搜索框 -->
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
          </el-col>
          <el-col :span="5" class="mt-2">
            <el-button type="primary" size="default" @click="refreshWeather">
              <el-icon class="mr-3"><Refresh /></el-icon>
              {{ weatherInfo.buttons.refresh }}</el-button
            >
            <el-button type="success" size="default" @click="showAddDialog"
              ><el-icon class="mr-3"> <Plus></Plus> </el-icon
              >{{ weatherInfo.buttons.add }}</el-button
            >
          </el-col>
          <el-col :span="4"></el-col>
        </el-row>
      </div>
      <!-- Weather Table -->
      <div v-if="weatherData.length === 0" class="text-center mt-4">
        <h1>请点击搜索获取相关数据</h1>
      </div>
      <div v-else>
        <el-table
          :data="currentPageData"
          v-loading="loading"
          class="table mt-4 mx-4"
          stripe
          size="small"
          table-layout="auto"
        >
          <el-table-column
            prop="time"
            label="时间"
            width="200"
          ></el-table-column>
          <el-table-column
            prop="temp"
            label="温度"
            min-width="50"
          ></el-table-column>
          <el-table-column
            prop="text"
            label="天气"
            width="100"
          ></el-table-column>
          <el-table-column
            prop="precip"
            label="降水"
            min-width="50"
          ></el-table-column>
          <el-table-column
            prop="windSpeed"
            label="风速"
            min-width="50"
          ></el-table-column>
          <el-table-column
            prop="humidity"
            label="湿度"
            min-width="50"
          ></el-table-column>
          <el-table-column
            prop="pressure"
            label="气压"
            min-width="50"
          ></el-table-column>
          <el-table-column
            prop="aqi"
            label="空气质量"
            min-width="50"
          ></el-table-column>
          <el-table-column
            prop="category"
            label="类别"
            width="100"
          ></el-table-column>
          <el-table-column prop="actions" label="操作" width="200">
            <template #default="scope">
              <el-button
                type="danger"
                size="small"
                @click="deleteWeather(scope.$index)"
                >{{ weatherInfo.actions.delete }}</el-button
              >
              <el-button
                type="primary"
                size="small"
                @click="editWeather(scope.row)"
                >{{ weatherInfo.actions.edit }}</el-button
              >
            </template>
          </el-table-column>
        </el-table>
        <!-- 添加分页 -->
        <el-pagination
          style="margin-left: 25px; margin-right: 5px; margin-top: 20px"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[5, 10, 20, 50]"
          :page-size="pageSize"
          background
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
        ></el-pagination>
      </div>
    </el-main>
  </el-container>

  <!-- Add Weather Dialog -->
  <el-dialog
    :title="weatherInfo.operation.addWeather"
    v-model="addDialogVisible"
    @close="resetAddForm"
  >
    <el-form :model="newWeatherData" ref="addForm">
      <el-form-item :label="weatherInfo.labels.time" prop="time">
        <el-input v-model="newWeatherData.time"></el-input>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.temperature" prop="temp">
        <el-input v-model="newWeatherData.temp"></el-input>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.text" prop="text">
        <el-input v-model="newWeatherData.text"></el-input>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.humidity" prop="humidity">
        <el-input v-model="newWeatherData.humidity"></el-input>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.windSpeed" prop="windSpeed">
        <el-input v-model="newWeatherData.windSpeed"></el-input>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.wind360" prop="wind360">
        <el-input v-model="newWeatherData.wind360"></el-input>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.windScale" prop="windScale">
        <el-input v-model="newWeatherData.windScale"></el-input>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.pressure" prop="pressure">
        <el-input v-model="newWeatherData.pressure"></el-input>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.aqi" prop="aqi">
        <el-input v-model="newWeatherData.aqi"></el-input>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.category" prop="category">
        <el-input v-model="newWeatherData.category"></el-input>
      </el-form-item>
    </el-form>
    <template v-slot:footer>
      <el-button @click="addDialogVisible = false">{{
        weatherInfo.buttons.cancel
      }}</el-button>
      <el-button type="primary" @click="addWeather">{{
        weatherInfo.buttons.add
      }}</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { post } from "@/api/index";
import { china_cities } from "@/stores/cities";
import throttle from "lodash/throttle";
import { WeatherData } from "@/types/weather";
/* 搜索 */
const selectedDate = ref("");
const pickerOptions: any = {
  firstDayOfWeek: 1, // 设置一周的第一天为周一
  disabledDate(time: Date): boolean {
    // 禁止选择未来日期
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
const weatherData: WeatherTable[] = reactive([]);
const handleSearch = () => {
  // 处理搜索逻辑，可以调用 API
  post<SearchWeatherHourlyListResponse>("/api/manage/data/search", {
    key: searchQuery.value,
    type: selectType.value,
    range: timeOption.value,
    time: selectedDate.value,
    address: selectedLocation.value,
  }).then((res) => {
    // console.log(res);
    if (res.status) {
      weatherData.splice(0, weatherData.length, ...res.data.weatherHourlyList);
    }
  });
};
const loading = ref(false);
const addDialogVisible = ref(false);
const newWeatherData = reactive<WeatherTable>({
  time: "",
  temp: "",
  text: "",
  precip: "",
  wind360: "",
  windScale: "",
  windSpeed: "",
  humidity: "",
  pressure: "",
  aqi: "",
  category: "",
});

function refreshWeather() {
  // You can implement data fetching logic here
  ElMessage({
    message: weatherInfo.dialogs.refresh,
    type: "success",
  });
}

function showAddDialog() {
  addDialogVisible.value = true;
}

function addWeather() {
  weatherData.push({ ...newWeatherData });
  addDialogVisible.value = false;
  ElMessage.success(weatherInfo.dialogs.add);
}

function resetAddForm() {
  newWeatherData.time = "";
  newWeatherData.temp = "";
  newWeatherData.text = "";
  newWeatherData.precip = "";
  newWeatherData.wind360 = "";
  newWeatherData.windScale = "";
  newWeatherData.windSpeed = "";
  newWeatherData.humidity = "";
  newWeatherData.pressure = "";
  newWeatherData.aqi = "";
  newWeatherData.category = "";
}
interface DeleteForm {
  time: string;
}
interface DeleteResponse {
  success: boolean;
  reason?: string;
}
const deleteWeather = throttle((index: number) => {
  const request: DeleteForm = { time: weatherData[index].time };
  weatherData.splice(index, 1);
  post<DeleteResponse>("/api/manage/data/delete", request).then((res) => {
    const response = res.data;
    if (response.success) {
      ElMessage.success(weatherInfo.dialogs.delete);
    } else ElMessage.error(weatherInfo.invaild);
  });
}, 500);

function editWeather(weather: WeatherData) {
  // You can implement edit functionality here
  console.log(weather);
  ElMessage.info(weatherInfo.dialogs.edit);
}

const weatherInfo = {
  labels: {
    time: "时间",
    temperature: "温度",
    text: "天气",
    humidity: "湿度",
    windSpeed: "风速",
    wind360: "风向",
    windScale: "风力",
    pressure: "气压",
    aqi: "空气质量",
    category: "类别",
  },
  actions: {
    delete: "删除",
    edit: "编辑",
  },
  buttons: {
    refresh: "刷新",
    add: "添加",
    cancel: "取消",
  },
  operation: {
    addWeather: "添加天气数据",
    deleteWeather: "删除天气数据",
  },
  dialogs: {
    delete: "天气数据已成功删除。",
    edit: "编辑功能即将推出！",
    add: "天气数据已成功添加。",
    refresh: "天气数据已刷新。",
  },
  invaild: "无效的请求！",
};
/* 分页功能 */
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);
const handleSizeChange = (val: number) => {
  pageSize.value = val;
};
const handleCurrentChange = (val: number) => {
  currentPage.value = val;
};
const splicePage = (data: WeatherTable[]) => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = currentPage.value * pageSize.value;
  return data.slice(start, end);
};
const currentPageData = ref<WeatherTable[]>([]);
watch(weatherData, () => {
  total.value = weatherData.length;
  currentPageData.value = splicePage(weatherData);
});
watch(currentPage, () => {
  currentPageData.value = splicePage(weatherData);
});
watch(pageSize, () => {
  currentPageData.value = splicePage(weatherData);
});
</script>

<style scoped>
.panel {
  height: 100%;
}
.panel.background-white {
  background-color: white !important;
}
.no-padding {
  padding: 0px;
}
.search-container {
  position: relative;
  background-color: white; /* 背景颜色 */
  z-index: 999; /* 确保在页面上方 */
  border-radius: 8px; /* 圆角边框 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 添加阴影 */
}

/* Search Container */
.search-container {
  position: relative;
  background-color: white; /* 背景颜色 */
  z-index: 999; /* 确保在页面上方 */
  padding: 20px; /* 添加一些内边距 */
  border-radius: 8px; /* 圆角边框 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影 */
}

/* Input inside Search Container */
.search-container input {
  width: 100%; /* 宽度100% */
  padding: 10px; /* 内边距 */
  border: 1px solid #ccc; /* 边框 */
  border-radius: 4px; /* 圆角边框 */
  outline: none; /* 去除输入框默认轮廓 */
  transition: border-color 0.2s ease; /* 添加过渡效果 */
}
</style>
