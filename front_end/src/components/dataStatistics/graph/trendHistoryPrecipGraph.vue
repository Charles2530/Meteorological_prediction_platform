<template>
  <div
    id="chart_precip_graph"
    ref="chart_precip_graph"
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
interface precipNode {
  time: string;
  precip: number;
}
interface PrecipChangeResponse {
  status: boolean;
  data: precipNode[];
}
const AqiDataList = ref<precipNode[]>([]);
watch(
  () => props.city,
  () =>
    Promise.all([fetchCityAqiChange()]).then(() => {
      renderChart_precip_history(AqiDataList.value);
    })
);
watch(
  () => props.periods,
  () =>
    Promise.all([fetchCityAqiChange()]).then(() => {
      renderChart_precip_history(AqiDataList.value);
    })
);
onMounted(() =>
  Promise.all([fetchCityAqiChange()]).then(() => {
    renderChart_precip_history(AqiDataList.value);
  })
);
const fetchCityAqiChange = throttle(
  async () =>
    get<PrecipChangeResponse>("/api/weather/precip/city_change/", {
      city: props.city,
      periods: props.periods,
    }).then((res) => {
      AqiDataList.value.splice(0, AqiDataList.value.length, ...res.data.data);
    }),
  1000
);
let chartInstance_precip_history: echarts.ECharts | null = null;
const renderChart_precip_history = async (tempData: precipNode[]) => {
  if (chartInstance_precip_history === null)
    chartInstance_precip_history = echarts.init(
      document.getElementById("chart_precip_graph") as HTMLDivElement
    );
  let option = {
    backgroundColor: "#fefefe",
    title: [
      {
        text: "降水变化",
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
          let winSpeed = param.value.toFixed(0);
          tooltipContent += `${param.marker} ${param.seriesName}: ${winSpeed} mm<br/>`;
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
        name: "降水",
        type: "line",
        smooth: true,
        showAllSymbol: true,
        symbol: "emptyCircle",
        symbolSize: 15,
        data: tempData.map((item) => item.precip),
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
        data: tempData.map((item) => item.precip),
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
        data: tempData.map((item) => item.precip),
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
        data: tempData.map((item) => item.precip),
        tooltip: {
          show: false,
        },
      },
    ],
  };
  chartInstance_precip_history.setOption(option);
};
</script>
