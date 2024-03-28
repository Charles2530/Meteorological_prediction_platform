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
        <el-table-column prop="city" label="城市"></el-table-column>
        <el-table-column prop="temperature" label="温度 (°C)"></el-table-column>
        <el-table-column prop="humidity" label="湿度 (%)"></el-table-column>
        <el-table-column prop="windSpeed" label="风速 (m/s)"></el-table-column>
        <el-table-column prop="actions" label="操作" width="200">
          <template #default="scope">
            <el-button type="danger" @click="deleteWeather(scope.$index)">{{
              weather.actions.delete
            }}</el-button>
            <el-button type="primary" @click="editWeather(scope.row)">{{
              weather.actions.edit
            }}</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-main>
    <el-footer class="no-padding">
      <div style="display: flex">
        <el-button type="primary" @click="refreshWeather">{{
          weather.buttons.refresh
        }}</el-button>
        <div style="flex: 1"></div>
        <el-button type="success" @click="showAddDialog">{{
          weather.buttons.add
        }}</el-button>
      </div>
    </el-footer>
  </el-container>

  <!-- Add Weather Dialog -->
  <el-dialog
    title="{{ weather.operation.addWeather }}"
    v-model="addDialogVisible"
    @close="resetAddForm"
  >
    <el-form :model="newWeatherData" ref="addForm">
      <el-form-item label="{{ weather.labels.city }}" prop="city">
        <el-input v-model="newWeatherData.city"></el-input>
      </el-form-item>
      <el-form-item label="{{ weather.labels.temperature }}" prop="temperature">
        <el-input v-model.number="newWeatherData.temperature"></el-input>
      </el-form-item>
      <el-form-item label="{{ weather.labels.humidity }}" prop="humidity">
        <el-input v-model.number="newWeatherData.humidity"></el-input>
      </el-form-item>
      <el-form-item label="{{ weather.labels.windSpeed }}" prop="windSpeed">
        <el-input v-model.number="newWeatherData.windSpeed"></el-input>
      </el-form-item>
    </el-form>
    <template v-slot:footer>
      <el-button @click="addDialogVisible = false">{{
        weather.buttons.cancel
      }}</el-button>
      <el-button type="primary" @click="addWeather">{{
        weather.buttons.add
      }}</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { ElMessage } from "element-plus";

interface WeatherData {
  city: string;
  temperature: number;
  humidity: number;
  windSpeed: number;
}

const weatherData = reactive<WeatherData[]>([
  { city: "纽约", temperature: 25, humidity: 60, windSpeed: 3 },
  { city: "伦敦", temperature: 18, humidity: 70, windSpeed: 5 },
]);

const loading = ref(false);
const addDialogVisible = ref(false);
const newWeatherData = reactive<WeatherData>({
  city: "",
  temperature: 0,
  humidity: 0,
  windSpeed: 0,
});

function refreshWeather() {
  // You can implement data fetching logic here
  ElMessage.success(weather.dialogs.refresh);
}

function showAddDialog() {
  addDialogVisible.value = true;
}

function addWeather() {
  weatherData.push({ ...newWeatherData });
  addDialogVisible.value = false;
  ElMessage.success(weather.dialogs.add);
}

function resetAddForm() {
  newWeatherData.city = "";
  newWeatherData.temperature = 0;
  newWeatherData.humidity = 0;
  newWeatherData.windSpeed = 0;
}

function deleteWeather(index: number) {
  weatherData.splice(index, 1);
  ElMessage.success(weather.dialogs.delete);
}

function editWeather(weather: WeatherData) {
  // You can implement edit functionality here
  ElMessage.info(weather.dialogs.edit);
}

const weather = {
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
  },
  dialogs: {
    delete: "天气数据已成功删除。",
    edit: "编辑功能即将推出！",
    add: "天气数据已成功添加。",
    refresh: "天气数据已刷新。",
  },
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
