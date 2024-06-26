<template>
  <el-select v-model="selectedLocation" placeholder="请选择城市" clearable>
    <el-option
      v-for="location in locations"
      :key="location.value"
      :label="location.label"
      :value="location.value"
    ></el-option>
  </el-select>
  <el-card>
    <div
      id="chart_history_seq"
      ref="chart_history_seq"
      style="height: 200px; min-width: 400px; padding: 10px; margin: 0 auto"
    ></div>
  </el-card>
</template>
<script lang="ts" setup>
import * as echarts from "echarts";
import { get } from "@/api/index.ts";
import { china_cities } from "@/stores/cities";
const selectedLocation = ref("");
const locations = china_cities;
watch(selectedLocation, () => {
  fetchCityAqiChange();
  fetchCityTempChange();
  fetchCityHumidChange();
  fetchCityPressureChange();
  renderChart(
    TempDataList.value,
    HumidDataList.value,
    AqiDataList.value,
    PressureDataList.value
  );
});

// 初始化 ECharts 实例
let chartInstance_history: echarts.ECharts | null = null;
interface tempNode {
  time: string;
  temp: number;
}
interface humidNode {
  time: string;
  humid: number;
}
interface aqiNode {
  time: string;
  aqi: number;
}
interface pressureNode {
  time: string;
  pressure: number;
}
interface AqiChangeResponse {
  status: boolean;
  data: aqiNode[];
}
interface TempChangeResponse {
  status: boolean;
  data: tempNode[];
}
interface HumidChangeResponse {
  status: boolean;
  data: humidNode[];
}
interface PressureChangeResponse {
  status: boolean;
  data: pressureNode[];
}
const TempDataList = ref<tempNode[]>([]);
const HumidDataList = ref<humidNode[]>([]);
const AqiDataList = ref<aqiNode[]>([]);
const PressureDataList = ref<pressureNode[]>([]);
const fetchCityTempChange = async () =>
  get<TempChangeResponse>("/api/weather/temp/city_change/", {
    city: selectedLocation.value,
  }).then((res) => {
    TempDataList.value.splice(0, TempDataList.value.length, ...res.data.data);
  });

const fetchCityHumidChange = async () =>
  get<HumidChangeResponse>("/api/weather/humid/city_change/", {
    city: selectedLocation.value,
  }).then((res) => {
    HumidDataList.value.splice(0, HumidDataList.value.length, ...res.data.data);
  });

const fetchCityAqiChange = async () =>
  get<AqiChangeResponse>("/api/weather/aqi/city_change/", {
    city: selectedLocation.value,
  }).then((res) => {
    AqiDataList.value.splice(0, AqiDataList.value.length, ...res.data.data);
  });

const fetchCityPressureChange = async () =>
  get<PressureChangeResponse>("/api/weather/pressure/city_change/", {
    city: selectedLocation.value,
  }).then((res) => {
    PressureDataList.value.splice(
      0,
      PressureDataList.value.length,
      ...res.data.data
    );
  });

const renderChart = async (
  tempData: tempNode[],
  humidData: humidNode[],
  aqiData: aqiNode[],
  pressureData: pressureNode[]
) => {
  if (!chartInstance_history) {
    const chartDom_history = document.getElementById("chart_history_seq");
    chartInstance_history = echarts.init(chartDom_history);
  }
  chartInstance_history.setOption({
    visualMap: [
      {
        show: true,
        type: "continuous",
        seriesIndex: 0,
        min: 0,
        max: 400,
      },
      {
        show: false,
        type: "continuous",
        seriesIndex: 1,
        min: 0,
        max: 400,
      },
      {
        show: false,
        type: "continuous",
        seriesIndex: 2,
        min: 0,
        max: 400,
      },
      {
        show: false,
        type: "continuous",
        seriesIndex: 3,
        min: 0,
        max: 400,
      },
    ],

    title: [
      {
        top: "0%",
        left: "center",
        text: "城市温度变化趋势图",
      },
      {
        top: "23%",
        left: "center",
        text: "城市湿度变化趋势图",
      },
      {
        top: "48%",
        left: "center",
        text: "城市AQI变化趋势图",
      },
      {
        top: "77%",
        left: "center",
        text: "城市气压变化趋势图",
      },
    ],
    tooltip: {
      trigger: "axis",
    },
    legend: {
      selectedMode: "single",
      selected: {
        温度: true, // 默认显示温度系列
        湿度: false, // 默认不显示湿度系列
        AQI: false, // 默认不显示AQI系列
        气压: false, // 默认不显示气压系列
      },
    },
    xAxis: [
      {
        data: tempData.map((item) => item.time),
      },
      {
        data: humidData.map((item) => item.time),
        gridIndex: 1,
      },
      {
        data: aqiData.map((item) => item.time),
        gridIndex: 2,
      },
      {
        data: pressureData.map((item) => item.time),
        gridIndex: 3,
      },
    ],
    yAxis: [{}, { gridIndex: 1 }, { gridIndex: 2 }, { gridIndex: 3 }],
    grid: [
      {
        top: "4%", // 从顶部开始
        bottom: "10%", // 调整底部距离以留出空间给下一个图表
        containLabel: true, // 确保标签不被裁剪
      },
      {
        top: "27%", // 从上一个图表底部开始
        bottom: "53%", // 留出空间给下一个图表
        containLabel: true,
      },
      {
        top: "52%", // 从上一个图表底部开始
        bottom: "28%", // 留出底部边距
        containLabel: true,
      },
      {
        top: "77%", // 从顶部开始，紧接在最后一个网格之下
        bottom: "1%", // 留出顶部边距
        containLabel: true,
      },
    ],
    series: [
      {
        type: "line",
        showSymbol: false,
        data: tempData.map((item) => item.temp),
      },
      {
        type: "line",
        showSymbol: false,
        data: humidData.map((item) => item.humid),
        xAxisIndex: 1,
        yAxisIndex: 1,
      },
      {
        type: "line",
        showSymbol: false,
        data: aqiData.map((item) => item.aqi),
        xAxisIndex: 2,
        yAxisIndex: 2,
      },
      {
        type: "line",
        showSymbol: false,
        data: pressureData.map((item) => item.pressure),
        xAxisIndex: 3,
        yAxisIndex: 3,
      },
    ],
  });
};

onMounted(() => {
  fetchCityAqiChange();
  fetchCityTempChange();
  fetchCityHumidChange();
  fetchCityPressureChange();
  renderChart(
    TempDataList.value,
    HumidDataList.value,
    AqiDataList.value,
    PressureDataList.value
  );

  window.addEventListener("click", () => {
    if (chartInstance_history) {
      renderChart(
        TempDataList.value,
        HumidDataList.value,
        AqiDataList.value,
        PressureDataList.value
      );
      chartInstance_history.resize();
    }
  });
  window.addEventListener("resize", () => {
    if (chartInstance_history) {
      renderChart(
        TempDataList.value,
        HumidDataList.value,
        AqiDataList.value,
        PressureDataList.value
      );
      chartInstance_history.resize();
    }
  });
});
</script>
