<template>
  <el-container class="panel">
    <el-main class="no-padding">
      <el-table
        :data="weatherData"
        v-loading="loading"
        class="table"
        size="small"
        table-layout="auto"
      >
        <el-table-column prop="city" label="城市"> </el-table-column>
        <el-table-column prop="temperature" label="温度 (°C)"></el-table-column>
        <el-table-column prop="humidity" label="湿度 (%)"></el-table-column>
        <el-table-column prop="windSpeed" label="风速 (m/s)"></el-table-column>
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
    </el-main>
    <el-footer class="no-padding">
      <div style="display: flex">
        <el-button type="primary" size="small" @click="refreshWeather">{{
          weatherInfo.buttons.refresh
        }}</el-button>
        <div style="flex: 1"></div>
        <el-button type="success" size="small" @click="showAddDialog">{{
          weatherInfo.buttons.add
        }}</el-button>
      </div>
    </el-footer>
  </el-container>

  <!-- Add Weather Dialog -->
  <el-dialog
    title="{{ weatherInfo.operation.addWeather }}"
    v-model="addDialogVisible"
    @close="resetAddForm"
  >
    <el-form :model="newWeatherData" ref="addForm">
      <el-form-item label="{{ weatherInfo.labels.city }}" prop="city">
        <el-input v-model="newWeatherData.city"></el-input>
      </el-form-item>
      <el-form-item
        label="{{ weatherInfo.labels.temperature }}"
        prop="temperature"
      >
        <el-input v-model.number="newWeatherData.temperature"></el-input>
      </el-form-item>
      <el-form-item label="{{ weatherInfo.labels.humidity }}" prop="humidity">
        <el-input v-model.number="newWeatherData.humidity"></el-input>
      </el-form-item>
      <el-form-item label="{{ weatherInfo.labels.windSpeed }}" prop="windSpeed">
        <el-input v-model.number="newWeatherData.windSpeed"></el-input>
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
import { ElMessage } from "element-plus";
import { post } from "@/api/index";
import throttle from "lodash/throttle";
import { WeatherData } from "@/types/weather";

const weatherData = reactive<WeatherData[]>([
  { pid: 1, city: "纽约", temperature: 25, humidity: 60, windSpeed: 3 },
  { pid: 2, city: "伦敦", temperature: 18, humidity: 70, windSpeed: 5 },
]);
const loading = ref(false);
const addDialogVisible = ref(false);
const newWeatherData = reactive<WeatherData>({
  pid: 0,
  city: "",
  temperature: 0,
  humidity: 0,
  windSpeed: 0,
});

function refreshWeather() {
  // You can implement data fetching logic here
  ElMessage.success(weatherInfo.dialogs.refresh);
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
  newWeatherData.city = "";
  newWeatherData.temperature = 0;
  newWeatherData.humidity = 0;
  newWeatherData.windSpeed = 0;
}
interface DeleteForm {
  pid: number;
}
interface DeleteResponse {
  success: boolean;
  reason?: string;
}
const deleteWeather = throttle((index: number) => {
  const request: DeleteForm = { pid: weatherData[index].pid };
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
    city: "城市",
    temperature: "温度",
    humidity: "湿度",
    windSpeed: "风速",
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
</script>

<style scoped>
.panel {
  height: 100%;
}
.no-padding {
  padding: 0px;
}
</style>
