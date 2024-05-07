<template>
  <div class="mx-auto">
    <el-row :gutter="20">
      <el-col :span="16"> <AirQualityAirQualityRankVM /> </el-col>
      <el-col :span="8">
        <!-- 中国城市空气质量排行图表
        <div
          id="chart_one"
          class="my-4"
          ref="chartContainer"
          style="width: 400px; height: 400px"
        ></div> -->
        <AirQualityAqiInstruction />
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts" setup>
import * as echarts from "echarts";

const airQualityRank = ref<any[]>([]);

// 初始化 ECharts 实例
let chartInstance: echarts.ECharts | null = null;

const fetchAirQualityRank = async () => {
  try {
    // 模拟异步请求获取城市空气质量排行数据
    const response = await fetch("/api/air-quality-rank");
    const data = await response.json();
    airQualityRank.value = data;
    renderChart();
  } catch (error) {
    console.error("Failed to fetch air quality rank:", error);
  }
};

const renderChart = () => {
  if (!chartInstance) {
    // 如果 ECharts 实例不存在，则创建
    const chartDom = document.getElementById("chart_one");
    chartInstance = echarts.init(chartDom);
  }

  // 绘制图表
  chartInstance.setOption({
    title: {
      text: "中国城市空气质量排行",
      left: "center",
      top: 20,
      textStyle: {
        fontSize: 16,
        fontWeight: "bold",
      },
    },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross",
      },
    },
    xAxis: {
      type: "category",
      data: airQualityRank.value.map((item) => item.city),
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        name: "AQI指数",
        type: "line",
        data: airQualityRank.value.map((item) => item.aqi),
        markLine: {
          data: [{ type: "average", name: "平均值" }],
        },
        itemStyle: {
          normal: {
            lineStyle: {
              width: 2,
            },
          },
        },
      },
    ],
  });
};

onMounted(() => {
  fetchAirQualityRank();
});
</script>

<style></style>
