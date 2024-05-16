<template>
  <div
    id="chart_aqi_graph"
    ref="chart_aqi_graph"
    style="height: 400px; min-width: 400px; padding: 10px; margin: 0 auto"
  ></div>
</template>
<script lang="ts" setup>
import * as echarts from "echarts";
import { get } from "@/api/index.ts";
const props = defineProps<{
  city: string;
}>();
interface aqiNode {
  time: string;
  aqi: number;
}
interface AqiChangeResponse {
  status: boolean;
  data: aqiNode[];
}
const AqiDataList = ref<aqiNode[]>([]);
watch(
  () => props.city,
  () =>
    Promise.all([fetchCityAqiChange()]).then(() => {
      renderChart_aqi_history(AqiDataList.value);
    })
);
onMounted(() =>
  Promise.all([fetchCityAqiChange()]).then(() => {
    renderChart_aqi_history(AqiDataList.value);
  })
);
const fetchCityAqiChange = async () =>
  get<AqiChangeResponse>("/api/weather/aqi/city_change/", {
    city: props.city,
  }).then((res) => {
    AqiDataList.value.splice(0, AqiDataList.value.length, ...res.data.data);
  });
let chartInstance_aqi_history: echarts.ECharts | null = null;
const renderChart_aqi_history = async (tempData: aqiNode[]) => {
  chartInstance_aqi_history = echarts.init(
    document.getElementById("chart_aqi_graph") as HTMLDivElement
  );
  let option = {
    backgroundColor: "#fefefe",
    title: [
      {
        text: "Aqi变化",
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
          let aqi = param.value.toFixed(0);
          tooltipContent += `${param.marker} ${param.seriesName}: ${aqi}<br/>`;
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
        name: "AQI",
        type: "scatter",
        smooth: true,
        showAllSymbol: true,
        symbol: "circle",
        symbolSize: function (value: any) {
          return value / 3;
        },
        itemStyle: {
          normal: {
            color: function (color: any) {
              if (color.data.value > 60) {
                return "#ff4500";
              } else if (color.data.value > 30) {
                return "#f5a623";
              } else {
                return "#1e90ff";
              }
            },
            borderColor: "rgba(255,255,255,1)",
            borderWidth: 3,
          },
        },
        tooltip: {
          show: true,
          formatter: function (params: any) {
            return `${params.name}<br/>AQI指数: ${params.value}`;
          },
        },
        data: tempData.map((item) => ({
          value: item.aqi,
        })),
        animationEasing: "bounceIn4",
      },
      //   {
      //     type: "bar",
      //     barWidth: 10,
      //     itemStyle: {
      //       borderRadius: 5,
      //       color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
      //         { offset: 0, color: "#14c8d4" },
      //         { offset: 1, color: "#43eec6" },
      //       ]),
      //     },
      //     data: tempData.map((item) => item.aqi),
      //     tooltip: {
      //       show: false,
      //     },
      //   },
      //   {
      //     type: "bar",
      //     barGap: "-100%",
      //     barWidth: 10,
      //     itemStyle: {
      //       color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
      //         { offset: 0, color: "rgba(20,200,212,0.5)" },
      //         { offset: 0.2, color: "rgba(20,200,212,0.2)" },
      //         { offset: 1, color: "rgba(20,200,212,0)" },
      //       ]),
      //     },
      //     z: -12,
      //     data: tempData.map((item) => item.aqi),
      //     tooltip: {
      //       show: false,
      //     },
      //   },
      //   {
      //     type: "pictorialBar",
      //     symbol: "rect",
      //     itemStyle: {
      //       color: "#0f375f",
      //     },
      //     symbolRepeat: true,
      //     symbolSize: [12, 4],
      //     symbolMargin: 1,
      //     z: -10,
      //     data: tempData.map((item) => item.aqi),
      //     tooltip: {
      //       show: false,
      //     },
      //   },
    ],
  };
  chartInstance_aqi_history.setOption(option);
};
</script>
