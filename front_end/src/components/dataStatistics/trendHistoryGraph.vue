<template>
  <el-card>
    <div
      id="chart_history"
      ref="chart_history"
      style="height: 200px; min-width: 800px; padding: 10px; margin: 0 auto"
    ></div>
  </el-card>
</template>
<script lang="ts" setup>
import * as echarts from "echarts";
import { get } from "@/api/index.ts";
import throttle from "lodash/throttle";
const props = defineProps<{
  city: string;
  periods: number;
}>();
watch(
  () => props.city,
  () =>
    Promise.all([
      fetchCityAqiChange(),
      fetchCityTempChange(),
      fetchCityHumidChange(),
      fetchCityPressureChange(),
      fetchCityPrecipChange(),
      fetchCityWinSpeedChange(),
    ]).then(() => {
      renderChart(
        TempDataList.value,
        HumidDataList.value,
        AqiDataList.value,
        PressureDataList.value,
        PrecipDataList.value,
        WinSpeedDataList.value
      );
    })
);
watch(
  () => props.periods,
  () =>
    Promise.all([
      fetchCityAqiChange(),
      fetchCityTempChange(),
      fetchCityHumidChange(),
      fetchCityPressureChange(),
      fetchCityPrecipChange(),
      fetchCityWinSpeedChange(),
    ]).then(() => {
      renderChart(
        TempDataList.value,
        HumidDataList.value,
        AqiDataList.value,
        PressureDataList.value,
        PrecipDataList.value,
        WinSpeedDataList.value
      );
    })
);

let chartInstance_history: echarts.ECharts | null = null;
interface tempNode {
  time: string;
  temp: number;
}
interface humidNode {
  time: string;
  humid: number;
}
interface aqiNode {
  time: string;
  aqi: number;
}
interface pressureNode {
  time: string;
  pressure: number;
}
interface precipNode {
  time: string;
  precip: number;
}
interface winSpeedNode {
  time: string;
  winSpeed: number;
}
interface AqiChangeResponse {
  status: boolean;
  data: aqiNode[];
}
interface TempChangeResponse {
  status: boolean;
  data: tempNode[];
}
interface HumidChangeResponse {
  status: boolean;
  data: humidNode[];
}
interface PressureChangeResponse {
  status: boolean;
  data: pressureNode[];
}
interface PrecipChangeResponse {
  status: boolean;
  data: precipNode[];
}
interface WinSpeedChangeResponse {
  status: boolean;
  data: winSpeedNode[];
}
const TempDataList = ref<tempNode[]>([]);
const HumidDataList = ref<humidNode[]>([]);
const AqiDataList = ref<aqiNode[]>([]);
const PressureDataList = ref<pressureNode[]>([]);
const PrecipDataList = ref<precipNode[]>([]);
const WinSpeedDataList = ref<winSpeedNode[]>([]);
const fetchCityTempChange = throttle(
  async () =>
    get<TempChangeResponse>("/api/weather/temp/city_change/", {
      city: props.city,
      periods: props.periods,
    }).then((res) => {
      TempDataList.value.splice(0, TempDataList.value.length, ...res.data.data);
    }),
  1000
);

const fetchCityHumidChange = throttle(
  async () =>
    get<HumidChangeResponse>("/api/weather/humid/city_change/", {
      city: props.city,
      periods: props.periods,
    }).then((res) => {
      HumidDataList.value.splice(
        0,
        HumidDataList.value.length,
        ...res.data.data
      );
    }),
  1000
);

const fetchCityAqiChange = throttle(
  async () =>
    get<AqiChangeResponse>("/api/weather/aqi/city_change/", {
      city: props.city,
      periods: props.periods,
    }).then((res) => {
      AqiDataList.value.splice(0, AqiDataList.value.length, ...res.data.data);
    }),
  1000
);

const fetchCityPressureChange = throttle(
  async () =>
    get<PressureChangeResponse>("/api/weather/pressure/city_change/", {
      city: props.city,
      periods: props.periods,
    }).then((res) => {
      PressureDataList.value.splice(
        0,
        PressureDataList.value.length,
        ...res.data.data
      );
    }),
  1000
);

const fetchCityPrecipChange = throttle(
  async () =>
    get<PrecipChangeResponse>("/api/weather/precip/city_change/", {
      city: props.city,
      periods: props.periods,
    }).then((res) => {
      PrecipDataList.value.splice(
        0,
        PrecipDataList.value.length,
        ...res.data.data
      );
    }),
  1000
);

const fetchCityWinSpeedChange = throttle(
  async () =>
    get<WinSpeedChangeResponse>("/api/weather/winSpeed/city_change/", {
      city: props.city,
      periods: props.periods,
    }).then((res) => {
      WinSpeedDataList.value.splice(
        0,
        WinSpeedDataList.value.length,
        ...res.data.data
      );
    }),
  1000
);

const renderChart = async (
  tempData: tempNode[],
  humidData: humidNode[],
  aqiData: aqiNode[],
  pressureData: pressureNode[],
  precipData: precipNode[],
  winSpeedData: winSpeedNode[]
) => {
  if (!chartInstance_history) {
    const chartDom_history = document.getElementById("chart_history");
    chartInstance_history = echarts.init(chartDom_history);
  }
  const maxTemp = Math.max(...tempData.map((item) => item.temp));
  const minTemp = Math.min(...tempData.map((item) => item.temp));
  const maxHumid = Math.max(...humidData.map((item) => item.humid));
  const minHumid = Math.min(...humidData.map((item) => item.humid));
  const maxAqi = Math.max(...aqiData.map((item) => item.aqi));
  const minAqi = Math.min(...aqiData.map((item) => item.aqi));
  const maxPressure = Math.max(...pressureData.map((item) => item.pressure));
  const minPressure = Math.min(...pressureData.map((item) => item.pressure));
  const maxPrecip = Math.max(...precipData.map((item) => item.precip));
  const minPrecip = Math.min(...precipData.map((item) => item.precip));
  const maxWinSpeed = Math.max(...winSpeedData.map((item) => item.winSpeed));
  const minWinSpeed = Math.min(...winSpeedData.map((item) => item.winSpeed));

  const scaledTempData = tempData.map(
    (item) => (item.temp - minTemp) / (maxTemp - minTemp)
  );
  const scaledHumidData = humidData.map(
    (item) => (item.humid - minHumid) / (maxHumid - minHumid)
  );
  const scaledAqiData = aqiData.map(
    (item) => (item.aqi - minAqi) / (maxAqi - minAqi)
  );
  const scaledPressureData = pressureData.map(
    (item) => (item.pressure - minPressure) / (maxPressure - minPressure)
  );
  const scaledPrecipData = precipData.map(
    (item) => (item.precip - minPrecip) / (maxPrecip - minPrecip)
  );
  const scaledWinSpeedData = winSpeedData.map(
    (item) => (item.winSpeed - minWinSpeed) / (maxWinSpeed - minWinSpeed)
  );

  const yAxis = {
    type: "value",
    axisLabel: {
      formatter: function (value: any) {
        return value.toFixed(4) * 100 + "%";
      },
    },
  };

  chartInstance_history.setOption({
    visualMap: {
      show: true,
      type: "continuous",
      seriesIndex: 0,
      min: 0,
      max: 1,
    },
    title: [
      {
        top: "0%",
        left: "center",
        text: "天气变化趋势总览",
      },
    ],
    tooltip: {
      trigger: "axis",
      formatter: function (params: any) {
        let tooltipContent = "";
        tooltipContent += `${params[0].axisValue}<br/>`;
        params.forEach(function (param: any) {
          switch (param.seriesName) {
            case "温度":
              let temp = (param.value * (maxTemp - minTemp) + minTemp).toFixed(
                0
              );
              tooltipContent += `${param.marker} ${param.seriesName}: ${temp} °C<br/>`;
              break;
            case "湿度":
              let humid = (
                param.value * (maxHumid - minHumid) +
                minHumid
              ).toFixed(0);
              tooltipContent += `${param.marker} ${param.seriesName}: ${humid} %<br/>`;
              break;
            case "AQI":
              let aqi = (param.value * (maxAqi - minAqi) + minAqi).toFixed(0);
              tooltipContent += `${param.marker} ${param.seriesName}: ${aqi}<br/>`;
              break;
            case "气压":
              let pressure = (
                param.value * (maxPressure - minPressure) +
                minPressure
              ).toFixed(2);
              tooltipContent += `${param.marker} ${param.seriesName}: ${pressure} hPa<br/>`;
              break;
            case "降水量":
              let precip = (param.value * (maxPrecip - minPrecip)).toFixed(1);
              tooltipContent += `${param.marker} ${param.seriesName}: ${precip} mm<br/>`;
              break;
            case "风速":
              let winSpeed = (
                param.value *
                (maxWinSpeed - minWinSpeed)
              ).toFixed(0);
              tooltipContent += `${param.marker} ${param.seriesName}: ${winSpeed} m/s<br/>`;
              break;
            default:
              break;
          }
        });

        return tooltipContent;
      },
    },
    xAxis: {
      data: tempData.map((item) => item.time),
    },
    yAxis: yAxis,
    grid: {
      top: "25%",
      bottom: "5%",
      left: "10%",
      right: "10%",
      containLabel: true,
    },
    legend: {
      selectedMode: "single",
      orient: "horizontal",
      left: "right",
      top: "top",
      data: ["温度", "湿度", "AQI", "气压", "降水量", "风速"],
    },
    series: [
      {
        type: "line",
        showSymbol: false,
        name: "温度",
        data: scaledTempData,
      },
      {
        type: "line",
        showSymbol: false,
        name: "湿度",
        data: scaledHumidData,
      },
      {
        type: "line",
        showSymbol: false,
        name: "AQI",
        data: scaledAqiData,
      },
      {
        type: "line",
        showSymbol: false,
        name: "气压",
        data: scaledPressureData,
      },
      {
        type: "line",
        showSymbol: false,
        name: "降水量",
        data: scaledPrecipData,
      },
      {
        type: "line",
        showSymbol: false,
        name: "风速",
        data: scaledWinSpeedData,
      },
    ],
  });
};

onMounted(() =>
  Promise.all([
    fetchCityAqiChange(),
    fetchCityTempChange(),
    fetchCityHumidChange(),
    fetchCityPressureChange(),
    fetchCityPrecipChange(),
    fetchCityWinSpeedChange(),
  ]).then(() => {
    renderChart(
      TempDataList.value,
      HumidDataList.value,
      AqiDataList.value,
      PressureDataList.value,
      PrecipDataList.value,
      WinSpeedDataList.value
    );
  })
);

window.addEventListener("resize", () => {
  if (chartInstance_history) {
    chartInstance_history.resize();
  }
});

window.addEventListener("click", () => {
  if (chartInstance_history) {
    renderChart(
      TempDataList.value,
      HumidDataList.value,
      AqiDataList.value,
      PressureDataList.value,
      PrecipDataList.value,
      WinSpeedDataList.value
    );
    chartInstance_history.resize();
  }
});

window.addEventListener("resize", () => {
  if (chartInstance_history) {
    renderChart(
      TempDataList.value,
      HumidDataList.value,
      AqiDataList.value,
      PressureDataList.value,
      PrecipDataList.value,
      WinSpeedDataList.value
    );
    chartInstance_history.resize();
  }
});
</script>
