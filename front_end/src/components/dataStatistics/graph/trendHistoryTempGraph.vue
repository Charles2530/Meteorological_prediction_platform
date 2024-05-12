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
const props = defineProps<{
  city: string;
}>();
interface tempNode {
  time: string;
  temp: number;
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
onMounted(() =>
  Promise.all([fetchCityTempChange()]).then(() => {
    renderChart_temp_history(TempDataList.value);
  })
);
const fetchCityTempChange = async () =>
  get<TempChangeResponse>("/api/weather/temp/city_change/", {
    city: props.city,
  }).then((res) => {
    TempDataList.value.splice(0, TempDataList.value.length, ...res.data.data);
  });
let chartInstance_temp_history: echarts.ECharts | null = null;
const renderChart_temp_history = async (tempData: tempNode[]) => {
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
        name: "温度",
        type: "line",
        smooth: true,
        showAllSymbol: true,
        symbol: "emptyCircle",
        symbolSize: 15,
        data: tempData.map((item) => item.temp),
      },
      {
        type: "bar",
        barWidth: 10,
        itemStyle: {
          borderRadius: 5,
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "#14c8d4" },
            { offset: 1, color: "#43eec6" },
          ]),
        },
        data: tempData.map((item) => item.temp),
        tooltip: {
          show: false,
        },
      },
      {
        type: "bar",
        barGap: "-100%",
        barWidth: 10,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "rgba(20,200,212,0.5)" },
            { offset: 0.2, color: "rgba(20,200,212,0.2)" },
            { offset: 1, color: "rgba(20,200,212,0)" },
          ]),
        },
        z: -12,
        data: tempData.map((item) => item.temp),
        tooltip: {
          show: false,
        },
      },
      {
        type: "pictorialBar",
        symbol: "rect",
        itemStyle: {
          color: "#0f375f",
        },
        symbolRepeat: true,
        symbolSize: [12, 4],
        symbolMargin: 1,
        z: -10,
        data: tempData.map((item) => item.temp),
        tooltip: {
          show: false,
        },
      },
    ],
  };
  chartInstance_temp_history.setOption(option);
};
</script>
