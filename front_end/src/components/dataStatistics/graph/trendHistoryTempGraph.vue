<template>
  <div
    id="chart_temp_graph"
    ref="chart_temp_graph"
    style="height: 400px; min-width: 400px; padding: 10px; margin: 0 auto"
  ></div>
</template>
<script lang="ts" setup>
import * as echarts from "echarts";
import { get } from "@/api/index.ts";
import throttle from "lodash/throttle";
const props = defineProps<{
  city: string;
  periods: number;
}>();
interface tempNode {
  time: string;
  temp: number;
  maxTemp: number;
  minTemp: number;
}
interface TempChangeResponse {
  status: boolean;
  data: tempNode[];
}
const TempDataList = ref<tempNode[]>([]);
watch(
  () => props.city,
  () =>
    Promise.all([fetchCityTempChange()]).then(() => {
      renderChart_temp_history(TempDataList.value);
    })
);
watch(
  () => props.periods,
  () =>
    Promise.all([fetchCityTempChange()]).then(() => {
      renderChart_temp_history(TempDataList.value);
    })
);
addEventListener("resize", () => {
  if (chartInstance_temp_history !== null) chartInstance_temp_history.resize();
});
onMounted(() =>
  Promise.all([fetchCityTempChange()]).then(() => {
    renderChart_temp_history(TempDataList.value);
  })
);
const fetchCityTempChange = throttle(
  async () =>
    get<TempChangeResponse>("/api/weather/temp/city_change/details/", {
      city: props.city,
      periods: props.periods,
    }).then((res) => {
      TempDataList.value.splice(0, TempDataList.value.length, ...res.data.data);
    }),
  1000
);
let chartInstance_temp_history: echarts.ECharts | null = null;
const renderChart_temp_history = async (tempData: tempNode[]) => {
  if (chartInstance_temp_history === null)
    chartInstance_temp_history = echarts.init(
      document.getElementById("chart_temp_graph") as HTMLDivElement
    );
  let option = {
    backgroundColor: "#fefefe",
    title: [
      {
        text: "温度变化",
        left: "center",
        top: "top",
        textStyle: {
          color: "#000",
        },
      },
    ],
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow",
      },
      formatter: function (params: any) {
        let tooltipContent = "";
        tooltipContent += `${params[0].axisValue}<br/>`;
        params.forEach(function (param: any) {
          let temp = param.value.toFixed(0);
          tooltipContent += `${param.marker} ${param.seriesName}: ${temp} °C<br/>`;
        });
        return tooltipContent;
      },
    },
    xAxis: {
      data: tempData.map((item) => item.time),
      axisLine: {
        lineStyle: {
          color: "#000",
        },
      },
    },
    yAxis: {
      splitLine: { show: false },
      axisLine: {
        lineStyle: {
          color: "#000",
        },
      },
    },
    series: [
      {
        name: "平均温度",
        type: "line",
        smooth: true,
        showSymbol: true,
        symbolSize: 15,
        itemStyle: {
          color: "#f4e925",
          lineStyle: {
            width: 2,
            type: "solid",
          },
        },
        data: tempData.map((item) => item.temp),
      },
      {
        name: "最高温度",
        type: "line",
        color: "#ff6347",
        smooth: true,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "#ff6347" },
            { offset: 1, color: "#ffcccb" },
          ]),
        },
        symbol: "triangle",
        symbolSize: 10,
        data: tempData.map((item) => item.maxTemp),
      },
      {
        name: "最低温度",
        type: "line",
        color: "#4682b4",
        smooth: true,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "#4682b4" },
            { offset: 1, color: "#b0e2ff" },
          ]),
        },
        symbol: "square",
        symbolSize: 10,
        data: tempData.map((item) => item.minTemp),
      },
    ],
  };
  chartInstance_temp_history.setOption(option);
};
</script>
