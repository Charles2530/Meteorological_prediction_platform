<template>
  <el-card>
    <div id="chart" style="width: 100%; height: 300px"></div>
  </el-card>
</template>

<script setup lang="ts">
import * as echarts from "echarts";
const chartRef = ref<HTMLElement | null>(null);
onMounted(() => {
  chartRef.value = document.getElementById("chart");
  console.log(chartRef.value);
  initChart();
});
const props = defineProps<{
  cnt: Array<number>; // [8, 126, 334, 323, 0]
}>();
function initChart() {
  if (!chartRef.value) return;
  const chart = echarts.init(chartRef.value);
  const option = {
    title: {
      text: "预警级别",
      left: "center",
    },
    xAxis: {
      type: "category",
      data: ["I级", "II级", "III级", "IV级", "V级"],
    },
    yAxis: {
      type: "value",
      min: 0,
      max: Math.max(...props.cnt),
    },
    series: [
      {
        name: "预警级别",
        type: "bar",
        data: props.cnt.map((item, index) => ({
          value: item,
          itemStyle: {
            color: ["#ff0000", "#ff7f00", "#ffff00", "#00bfff", "#eeeeee"][
              index
            ],
          },
        })),
        barWidth: "60%",
      },
    ],
  };
  chart.setOption(option);
}
</script>
