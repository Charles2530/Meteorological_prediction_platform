<template>
  <el-container class="panel background-white rounded-lg">
    <el-main class="no-padding">
      <div class="search-container mx-4">
        <el-row>
          <el-col :span="16">
            <div class="p-2 space-y-4">
              <el-row :gutter="20">
                <el-col :span="6">
                  <el-select v-model="selectType" placeholder="请选择数据类型">
                    <el-option label="天气数据" value="weather"></el-option>
                    <el-option label="地质灾害" value="disaster"></el-option>
                  </el-select>
                </el-col>
                <el-col :span="12">
                  <el-date-picker
                    v-model="selectedDate"
                    type="daterange"
                    range-separator="至"
                    start-placeholder="开始日期"
                    end-placeholder="结束日期"
                    :picker-options="pickerOptions"
                    format="YYYY年MM月DD日"
                    clearable
                    style="width: 100%"
                  ></el-date-picker>
                </el-col>
                <el-col :span="6">
                  <el-select
                    v-model="selectedLocation"
                    placeholder="请选择城市"
                    clearable
                  >
                    <el-option
                      v-for="location in locations"
                      :key="location.value"
                      :label="location.label"
                      :value="location.value"
                    ></el-option>
                  </el-select>
                </el-col>
              </el-row>
            </div>
          </el-col>
          <el-col :span="8" class="mt-2">
            <el-button type="info" size="default" plain @click="handleSearch">
              <el-icon class="mr-2"><Search></Search></el-icon>
              点击搜索
            </el-button>
            <el-button
              type="primary"
              size="default"
              plain
              @click="refreshWeather"
            >
              <el-icon class="mr-3"><Refresh /></el-icon>
              {{ weatherInfo.buttons.refresh }}</el-button
            >
            <el-button
              type="success"
              size="default"
              plain
              @click="showAddDialog"
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
        <div style="margin: 0 auto">
          <el-divider></el-divider>
          <!-- 居中显示 -->
          <div class="text-center mt-4">
            <h1 class="text-gray-500" style="font-size: 25px">天气数据</h1>
          </div>
        </div>
        <el-table
          :data="currentPageData"
          v-loading="loading"
          class="table mt-4 mx-4"
          highlight-current-row
          stripe
          size="small"
          table-layout="auto"
          border
          fit
        >
          <el-table-column
            prop="time"
            label="时间"
            width="200"
          ></el-table-column>
          <el-table-column
            prop="city"
            label="城市"
            width="100"
            :formatter="(row: CityWeatherData) => {
                return locations.find((location) => location.value === row.city)?.label||row.city;
                }"
          ></el-table-column>
          <el-table-column
            prop="temp"
            label="温度"
            min-width="50"
            :formatter="(row: CityWeatherData) => row.temp==undefined?'没有该数据':`${row.temp}°C`"
          ></el-table-column>
          <el-table-column
            prop="text"
            label="天气"
            width="100"
            :formatter="(row: CityWeatherData) => row.text==''?'没有该数据':row.text"
          ></el-table-column>
          <el-table-column
            prop="precip"
            label="降水"
            min-width="50"
            :formatter="(row: CityWeatherData) => row.precip==undefined?'没有该数据':`${row.precip}mm`"
          ></el-table-column>
          <el-table-column
            prop="windSpeed"
            label="风速"
            min-width="50"
            :formatter="(row: CityWeatherData) => row.windSpeed==undefined?'没有该数据':`${row.windSpeed}m/s`"
          ></el-table-column>
          <el-table-column
            prop="humidity"
            label="湿度"
            min-width="50"
            :formatter="(row: CityWeatherData) => row.humidity==undefined?'没有该数据':`${row.humidity}%`"
          ></el-table-column>
          <el-table-column
            prop="pressure"
            label="气压"
            min-width="50"
            :formatter="(row: CityWeatherData) => row.pressure==undefined?'没有该数据':`${row.pressure}hPa`"
          ></el-table-column>
          <el-table-column
            prop="aqi"
            label="空气质量"
            min-width="50"
            :formatter="(row: CityWeatherData) => row.aqi==undefined?'没有该数据':`${row.aqi}`"
          ></el-table-column>
          <el-table-column
            prop="category"
            label="类别"
            min-width="100"
            :formatter="(row: CityWeatherData) => row.category=='' ?'没有该数据':row.category"
          ></el-table-column>
          <el-table-column prop="actions" label="操作" width="200">
            <template #default="scope">
              <el-button
                type="danger"
                size="small"
                @click="deleteWeather(scope.$index)"
              >
                <el-icon class="mr-2"><Delete></Delete></el-icon>
                {{ weatherInfo.actions.delete }}</el-button
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
    <el-form
      :model="newWeatherData"
      ref="addForm"
      size="small"
      label-width="100px"
      inline
    >
      <el-form-item :label="weatherInfo.labels.time" prop="time">
        <el-date-picker
          v-model="newWeatherData.time"
          type="datetime"
          placeholder="选择时间"
          style="width: 10rem"
          format="YYYY-MM-DD HH:mm:ss"
          value-format="YYYY-MM-DD HH:mm:ss"
        ></el-date-picker>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.city" prop="city">
        <el-select
          v-model="newWeatherData.city"
          placeholder="请选择城市"
          style="width: 10rem"
          size="small"
          clearable
        >
          <el-option
            v-for="location in locations"
            :key="location.value"
            :label="location.label"
            :value="location.value"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.temperature" prop="temp">
        <el-input-number
          v-model="newWeatherData.temp"
          :min="-50"
          :max="50"
          :step="0.1"
          :formatter="(value:number) => `${value}°C`"
          style="width: 10rem"
        ></el-input-number>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.text" prop="text">
        <el-select
          v-model="newWeatherData.text"
          placeholder="请选择天气"
          style="width: 10rem"
          size="small"
          clearable
        >
          <el-option
            v-for="weather in weathers"
            :key="weather.value"
            :label="weather.label"
            :value="weather.value"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.precip" prop="precip">
        <el-input-number
          v-model="newWeatherData.precip"
          :min="0"
          :max="100"
          :step="1"
          :formatter="(value:number) => `${value}mm`"
          style="width: 10rem"
        ></el-input-number>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.humidity" prop="humidity">
        <el-input-number
          v-model="newWeatherData.humidity"
          :min="0"
          :max="100"
          :step="1"
          :formatter="(value:number) => `${value}%`"
          style="width: 10rem"
        ></el-input-number>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.windSpeed" prop="windSpeed">
        <el-input-number
          v-model="newWeatherData.windSpeed"
          :min="0"
          :max="100"
          :step="0.1"
          :formatter="(value:number) => `${value}m/s`"
          style="width: 10rem"
        ></el-input-number>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.wind360" prop="wind360">
        <el-input-number
          v-model="newWeatherData.wind360"
          :min="0"
          :max="360"
          :step="1"
          :formatter="(value:number) => `${value}°`"
          style="width: 10rem"
        ></el-input-number>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.windScale" prop="windScale">
        <el-input-number
          v-model="newWeatherData.windScale"
          :min="0"
          :max="12"
          :step="1"
          :formatter="(value:number) => `${value}级`"
          style="width: 10rem"
        ></el-input-number>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.pressure" prop="pressure">
        <el-input-number
          v-model="newWeatherData.pressure"
          :min="800"
          :max="1100"
          :step="1"
          :formatter="(value:number) => `${value}hPa`"
          style="width: 10rem"
        ></el-input-number>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.aqi" prop="aqi">
        <el-input-number
          v-model="newWeatherData.aqi"
          :min="0"
          :max="500"
          :step="1"
          style="width: 10rem"
        ></el-input-number>
      </el-form-item>
      <el-form-item :label="weatherInfo.labels.category" prop="category">
        <el-select
          v-model="newWeatherData.category"
          placeholder="请选择空气质量等级"
          style="width: 10rem"
          size="small"
          clearable
        >
          <el-option
            v-for="level in aqi_level"
            :key="level.value"
            :label="level.label"
            :value="level.value"
          ></el-option>
        </el-select>
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
import { weather, aqi_level } from "@/stores/weather";
import throttle from "lodash/throttle";
import { CityWeatherData } from "@/types/weather";
/* 搜索 */
const selectedDate = ref("");
const pickerOptions: any = {
  firstDayOfWeek: 1,
  disabledDate(time: Date): boolean {
    return time.getTime() > Date.now();
  },
};
const selectType = ref("");
const selectedLocation = ref("");
const locations = china_cities;
const weathers = weather;
interface SearchWeatherHourlyListResponse {
  status: boolean;
  weatherHourlyList: CityWeatherData[];
}
const weatherData: CityWeatherData[] = reactive([]);
const handleSearch = () => {
  post<SearchWeatherHourlyListResponse>("/api/manage/data/search/", {
    type: selectType.value,
    time: selectedDate.value,
    address: selectedLocation.value,
  }).then((res) => {
    if (res.status) {
      weatherData.splice(0, weatherData.length, ...res.data.weatherHourlyList);
    }
  });
};
const loading = ref(false);
const addDialogVisible = ref(false);
const newWeatherData = reactive<CityWeatherData>({
  time: "",
  city: "",
  temp: undefined,
  text: "",
  precip: undefined,
  wind360: undefined,
  windScale: undefined,
  windSpeed: undefined,
  humidity: undefined,
  pressure: undefined,
  aqi: undefined,
  category: "",
});

function refreshWeather() {
  // You can implement data fetching logic here
  handleSearch();
  ElMessage({
    message: weatherInfo.dialogs.refresh,
    type: "success",
  });
}

function showAddDialog() {
  addDialogVisible.value = true;
}
interface addWeatherResponse {
  status: boolean;
  reason?: string;
}
function addWeather() {
  if (newWeatherData.time === "" || newWeatherData.city === "") {
    ElMessage.error("请填写完整信息！时间和城市不能为空。");
    return;
  }
  weatherData.push({ ...newWeatherData });
  addDialogVisible.value = false;
  console.log({ ...newWeatherData });
  post<addWeatherResponse>(
    "/api/manage/data/weather_add/",
    newWeatherData
  ).then((res) => {
    const response = res.data;
    if (!response.status) {
      ElMessage.error("添加失败！");
    } else {
      ElMessage.success(weatherInfo.dialogs.add);
    }
  });
}

function resetAddForm() {
  newWeatherData.time = "";
  newWeatherData.city = "";
  newWeatherData.temp = undefined;
  newWeatherData.text = "";
  newWeatherData.precip = undefined;
  newWeatherData.wind360 = undefined;
  newWeatherData.windScale = undefined;
  newWeatherData.windSpeed = undefined;
  newWeatherData.humidity = undefined;
  newWeatherData.pressure = undefined;
  newWeatherData.aqi = undefined;
  newWeatherData.category = "";
}
interface DeleteForm {
  time: string;
  city: string;
}
interface DeleteResponse {
  success: boolean;
  reason?: string;
}
const deleteWeather = throttle((index: number) => {
  const request: DeleteForm = {
    time: weatherData[index].time,
    city: weatherData[index].city,
  };
  weatherData.splice(index, 1);
  post<DeleteResponse>("/api/manage/data/delete/", request).then((res) => {
    const response = res.data;
    if (response.success) {
      ElMessage.success(weatherInfo.dialogs.delete);
    } else ElMessage.error(weatherInfo.invaild);
  });
}, 500);

const weatherInfo = {
  labels: {
    time: "时间",
    city: "城市",
    temperature: "温度",
    text: "天气",
    precip: "降水量",
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
const splicePage = (data: CityWeatherData[]) => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = currentPage.value * pageSize.value;
  return data.slice(start, end);
};
const currentPageData = ref<CityWeatherData[]>([]);
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
