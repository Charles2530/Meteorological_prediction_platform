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
      id="chart_history"
      ref="chart_history"
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
    const chartDom_history = document.getElementById("chart_history");
    chartInstance_history = echarts.init(chartDom_history);
  }
  chartInstance_history.setOption({
    visualMap: {
      show: true,
      type: "continuous",
      seriesIndex: 0,
      min: 0,
      max: 400,
    },

    title: [
      {
        top: "0%",
        left: "center",
        text: "多指标变化趋势图",
      },
    ],
    tooltip: {
      trigger: "axis",
      formatter: function (params: any) {
        let tooltipContent = "";

        params.forEach(function (param: any) {
          switch (param.seriesName) {
            case "温度":
              tooltipContent += `${param.marker} ${param.seriesName}: ${param.value} °C<br/>`;
              break;
            case "湿度":
              tooltipContent += `${param.marker} ${param.seriesName}: ${param.value}%<br/>`;
              break;
            case "AQI":
              tooltipContent += `${param.marker} ${param.seriesName}: ${param.value}<br/>`;
              break;
            case "气压":
              tooltipContent += `${param.marker} ${param.seriesName}: ${param.value} hPa<br/>`;
              break;
            default:
              break;
          }
        });

        return tooltipContent;
      },
    },
    xAxis: {
      data: tempData.map((item) => item.time),
    },
    yAxis: {},

    grid: {
      top: "20%",
      bottom: "20%",
      left: "10%",
      right: "10%",
      containLabel: true,
    },
    legend: {
      orient: "horizontal",
      left: "right",
      top: "top",
      data: ["温度", "湿度", "AQI", "气压"],
    },

    series: [
      {
        type: "line",
        showSymbol: false,
        name: "温度",
        data: tempData.map((item) => item.temp),
      },
      {
        type: "line",
        showSymbol: false,
        name: "湿度",
        data: humidData.map((item) => item.humid),
      },
      {
        type: "line",
        showSymbol: false,
        name: "AQI",
        data: aqiData.map((item) => item.aqi),
      },
      {
        type: "line",
        showSymbol: false,
        name: "气压",
        data: pressureData.map((item) => item.pressure),
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
