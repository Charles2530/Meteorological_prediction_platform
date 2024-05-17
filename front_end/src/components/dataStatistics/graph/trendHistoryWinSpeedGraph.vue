<template>
  <div
    id="chart_winSpeed_graph"
    ref="chart_winSpeed_graph"
    style="height: 400px; min-width: 400px; padding: 10px; margin: 0 auto"
  ></div>
</template>
<script lang="ts" setup>
import * as echarts from "echarts";
import { get } from "@/api/index.ts";
const props = defineProps<{
  city: string;
  periods: number;
}>();
interface winSpeedNode {
  time: string;
  winSpeed: number;
}
interface WinSpeedChangeResponse {
  status: boolean;
  data: winSpeedNode[];
}
const AqiDataList = ref<winSpeedNode[]>([]);
watch(
  () => props.city,
  () =>
    Promise.all([fetchCityAqiChange()]).then(() => {
      renderChart_winSpeed_history(AqiDataList.value);
    })
);
watch(
  () => props.periods,
  () =>
    Promise.all([fetchCityAqiChange()]).then(() => {
      renderChart_winSpeed_history(AqiDataList.value);
    })
);
onMounted(() =>
  Promise.all([fetchCityAqiChange()]).then(() => {
    renderChart_winSpeed_history(AqiDataList.value);
  })
);
const fetchCityAqiChange = async () =>
  get<WinSpeedChangeResponse>("/api/weather/winSpeed/city_change/", {
    city: props.city,
    periods: props.periods,
  }).then((res) => {
    AqiDataList.value.splice(0, AqiDataList.value.length, ...res.data.data);
  });
let chartInstance_winSpeed_history: echarts.ECharts | null = null;
const renderChart_winSpeed_history = async (tempData: winSpeedNode[]) => {
  chartInstance_winSpeed_history = echarts.init(
    document.getElementById("chart_winSpeed_graph") as HTMLDivElement
  );
  let option = {
    backgroundColor: "#fefefe",
    title: [
      {
        text: "风速变化",
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
          let winSpeed = param.value.toFixed(0);
          tooltipContent += `${param.marker} ${param.seriesName}: ${winSpeed} m/s<br/>`;
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
        name: "风速",
        type: "line",
        smooth: true,
        symbol: "circle",
        symbolSize: 5,
        data: tempData.map((item) => item.winSpeed),
        itemStyle: {
          normal: {
            color: "#3398DB",
          },
        },
        lineStyle: {
          width: 2,
          shadowColor: "rgba(51,152,213,0.4)",
          shadowBlur: 10,
          type: "dashed",
        },
        animationEasing: "elasticOut",
        animationDelay: function (idx: any) {
          return Math.random() * 200;
        },
      },
      {
        type: "bar",
        barWidth: 10,
        itemStyle: {
          normal: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: "#3398DB" },
              { offset: 1, color: "#D7E9F7" },
            ]),
          },
        },
        data: tempData.map((item) => item.winSpeed),
        z: -1,
        tooltip: {
          show: false,
        },
      },
      {
        type: "bar",
        barWidth: 10,
        barGap: "-100%",
        itemStyle: {
          normal: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: "rgba(51,152,213,1)" },
              { offset: 1, color: "rgba(51,152,213,0)" },
            ]),
          },
        },
        data: tempData.map((item) => item.winSpeed),
        z: -2,
        tooltip: {
          show: false,
        },
      },
    ],
  };
  chartInstance_winSpeed_history.setOption(option);
};
</script>
