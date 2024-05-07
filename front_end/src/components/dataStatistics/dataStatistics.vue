<template>
  <el-row :gutter="2">
    <el-col :span="18">
      <dataList></dataList>
    </el-col>
    <el-col :span="6">
      <div class="chart">
        <div
          id="chart_one"
          style="
            height: 300px;
            width: 300px;
            padding: 10px;
            margin: 0 auto;
            /* align-items: center;
        justify-content: center; */
          "
        ></div>
      </div>
    </el-col>
  </el-row>
</template>
<script lang="ts" setup>
import dataList from "./dataList.vue";
import * as echarts from "echarts";
type ECharts = echarts.ECharts;
let echartsInstance: Ref<ECharts | null> = ref(null);
onMounted(() => {
  let chartDom = document.getElementById("chart_one");
  echartsInstance.value = echarts.init(chartDom);
  nextTick(() => {
    initChart();
  });
  setTimeout(() => {
    initChart();
  }, 2000);
});
watch(echartsInstance, () => {
  console.log(echartsInstance.value);
});
function initChart() {
  const today = new Date();
  const lastWeek = new Date(
    today.getFullYear(),
    today.getMonth(),
    today.getDate() - 6
  );
  const xAxisData = [];
  for (let i = lastWeek.getTime(); i <= today.getTime(); i += 86400000) {
    const date = new Date(i);
    xAxisData.push(
      date.toLocaleDateString("en-US", {
        month: "numeric",
        day: "numeric",
      })
    );
  }
  console.log(xAxisData.join(", "));

  let option = {
    grid: {
      left: "3%",
      right: "4%",
      bottom: "4%",
      top: "11%",
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: xAxisData,
      axisLabel: {
        formatter: "{value}",
      },
    },
    yAxis: {
      type: "value",
      axisLabel: {
        formatter: "{value} m³",
      },
    },
    tooltip: {
      trigger: "axis",
      formatter: "用气日期：{b}<br />日用气量：{c}",
      backgroundColor: "rgba(255, 255, 255, 0.8)",
      axisPointer: {
        type: "shadow",
      },
    },
    series: [
      {
        data: [120, 200, 150, 80, 70, 110, 130],
        type: "bar",
        showBackground: true,
        backgroundStyle: {
          color: "rgba(180, 180, 180, 0.2)",
        },
        label: {
          normal: {
            show: true,
            position: "top",
          },
        },
      },
    ],
  };

  console.log(option);

  option && echartsInstance.value.setOption(option);
}
</script>
