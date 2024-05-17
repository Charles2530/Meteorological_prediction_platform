<template>
  <div
    id="chart_humid_graph"
    ref="chart_humid_graph"
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
interface humidNode {
  time: string;
  humid: number;
}
interface HumidChangeResponse {
  status: boolean;
  data: humidNode[];
}
const AqiDataList = ref<humidNode[]>([]);
watch(
  () => props.city,
  () =>
    Promise.all([fetchCityAqiChange()]).then(() => {
      renderChart_humid_history(AqiDataList.value);
    })
);
watch(
  () => props.periods,
  () =>
    Promise.all([fetchCityAqiChange()]).then(() => {
      renderChart_humid_history(AqiDataList.value);
    })
);
onMounted(() =>
  Promise.all([fetchCityAqiChange()]).then(() => {
    renderChart_humid_history(AqiDataList.value);
  })
);
const fetchCityAqiChange = async () =>
  get<HumidChangeResponse>("/api/weather/humid/city_change/", {
    city: props.city,
    periods: props.periods,
  }).then((res) => {
    AqiDataList.value.splice(0, AqiDataList.value.length, ...res.data.data);
  });
let chartInstance_humid_history: echarts.ECharts | null = null;
const renderChart_humid_history = async (tempData: humidNode[]) => {
  if (chartInstance_humid_history === null)
    chartInstance_humid_history = echarts.init(
      document.getElementById("chart_humid_graph") as HTMLDivElement
    );
  let option = {
    backgroundColor: "#fefefe",
    title: [
      {
        text: "湿度变化",
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
          tooltipContent += `${param.marker} ${param.seriesName}: ${temp} %<br/>`;
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
        name: "湿度",
        type: "bar",
        symbol: "circle",
        symbolSize: function (val: any) {
          return val / 5;
        },
        itemStyle: {
          normal: {
            color: function (params: any) {
              if (params.data > 80) {
                return "#ff0000";
              } else if (params.data > 60) {
                return "#ff9900";
              } else if (params.data > 40) {
                return "#ffff00";
              } else if (params.data > 20) {
                return "#009900";
              } else {
                return "#003fef";
              }
            },
          },
        },
        data: tempData.map((item) => item.humid),
        position: "right",
      },
    ],
  };
  chartInstance_humid_history.setOption(option);
};
</script>
