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
        showAllSymbol: true,
        symbol: "emptyCircle",
        symbolSize: 15,
        data: tempData.map((item) => item.pressure),
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
        data: tempData.map((item) => item.pressure),
        tooltip: {
          show: false,
        },
      },
    ],
  };
  chartInstance_pressure_history.setOption(option);
};
</script>
