<template>
  <div
    id="chart_pressure_graph"
    ref="chart_pressure_graph"
    style="height: 400px; min-width: 400px; padding: 10px; margin: 0 auto"
  ></div>
</template>
<script lang="ts" setup>
import * as echarts from "echarts";
import { get } from "@/api/index.ts";
const props = defineProps<{
  city: string;
}>();
interface pressureNode {
  time: string;
  pressure: number;
}
interface PressureChangeResponse {
  status: boolean;
  data: pressureNode[];
}
const AqiDataList = ref<pressureNode[]>([]);
watch(
  () => props.city,
  () =>
    Promise.all([fetchCityAqiChange()]).then(() => {
      renderChart_pressure_history(AqiDataList.value);
    })
);
onMounted(() =>
  Promise.all([fetchCityAqiChange()]).then(() => {
    renderChart_pressure_history(AqiDataList.value);
  })
);
const fetchCityAqiChange = async () =>
  get<PressureChangeResponse>("/api/weather/pressure/city_change/", {
    city: props.city,
  }).then((res) => {
    AqiDataList.value.splice(0, AqiDataList.value.length, ...res.data.data);
  });
let chartInstance_pressure_history: echarts.ECharts | null = null;
const renderChart_pressure_history = async (tempData: pressureNode[]) => {
  chartInstance_pressure_history = echarts.init(
    document.getElementById("chart_pressure_graph") as HTMLDivElement
  );
  let option = {
    backgroundColor: "#fefefe",
    title: [
      {
        text: "压力变化",
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
          tooltipContent += `${param.marker} ${param.seriesName}: ${temp} hPa<br/>`;
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
      min: 980,
      splitLine: { show: false },
      axisLine: {
        lineStyle: {
          color: "#000",
        },
      },
    },
    series: [
      {
        name: "压力",
        type: "line",
        smooth: true,
        symbol: "circle",
        symbolSize: 5,
        data: tempData.map((item) => item.pressure),
        itemStyle: {
          normal: {
            color: "#3398DB",
          },
        },
        lineStyle: {
          width: 2,
          shadowColor: "rgba(51,152,213,0.4)",
          shadowBlur: 5,
        },
        animationEasing: "elasticOut",
        animationDelay: function (idx: any) {
          return Math.random() * 200;
        },
      },
      {
        name: "压力数据点",
        type: "scatter",
        symbolSize: function (value: any, params: any) {
          return Math.max(10, value / 100);
        },
        data: tempData.map((item) => ({
          value: item.pressure,
          itemStyle: {
            normal: {
              color: "#f4e925",
            },
          },
        })),
        tooltip: {
          show: false,
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: "rgba(255, 255, 0, 0.5)",
            borderWidth: 1,
            borderColor: "rgba(255, 255, 0, 1)",
          },
        },
      },
    ],
  };
  chartInstance_pressure_history.setOption(option);
};
</script>