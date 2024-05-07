<template>
  <div class="mx-auto" style="max-height: 85vh; overflow-y: auto">
    <el-row :gutter="20">
      <el-col :span="16"> <AirQualityAirQualityRankVM /> </el-col>
      <el-col :span="8">
        <el-card>
          <BriefAqi />
        </el-card>
        <el-card>
          <div
            id="chart_aqi_change"
            class="my-4"
            ref="chart_aqi_change"
            style="height: 200px; min-width: 400px"
          ></div>
        </el-card>
        <el-card>
          <AirQualityAqiInstruction />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts" setup>
import * as echarts from "echarts";
import { get } from "@/api/index.ts";
import BriefAqi from "./BriefAqi.vue";

// 初始化 ECharts 实例
let chartInstance: echarts.ECharts | null = null;
interface aqiNode {
  time: string;
  aqi: number;
}
interface AqiChangeResponse {
  status: boolean;
  data: aqiNode[];
}

const fetchAirQualityRank = async () =>
  get<AqiChangeResponse>("/api/weather/aqi/aqi_change").then((res) => {
    renderChart(res.data.data);
  });

const renderChart = (data: aqiNode[]) => {
  if (!chartInstance) {
    // 如果 ECharts 实例不存在，则创建
    const chartDom = document.getElementById("chart_aqi_change");
    chartInstance = echarts.init(chartDom);
  }

  // 绘制图表
  chartInstance.setOption({
    // Make gradient line here
    visualMap: [
      {
        show: false,
        type: "continuous",
        seriesIndex: 0,
        min: 0,
        max: 400,
      },
    ],

    title: [
      {
        left: "center",
        text: "当前城市AQI变化趋势图",
      },
    ],
    tooltip: {
      trigger: "axis",
    },
    xAxis: [
      {
        data: data.map((item) => item.time),
      },
    ],
    yAxis: [{}],
    grid: [
      {
        bottom: "10%",
      },
      {
        top: "5%",
      },
    ],
    series: [
      {
        type: "line",
        showSymbol: false,
        data: data.map((item) => item.aqi),
      },
    ],
  });
};

onMounted(() => {
  fetchAirQualityRank();
  // 监听窗口大小变化
  window.addEventListener("click", () => {
    if (chartInstance) {
      chartInstance.resize();
    }
  });
  window.addEventListener("resize", () => {
    if (chartInstance) {
      chartInstance.resize();
    }
  });
});
</script>

<style></style>
