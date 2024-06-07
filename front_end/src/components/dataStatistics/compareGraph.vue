<template>
  <el-row :gutter="2">
    <el-col :span="8">
      <el-autocomplete
        v-model="location1"
        placeholder="请选择城市1"
        :fetch-suggestions="querySearch"
        clearable
        class="inline-input w-60"
        highlight-first-item
        :value-key="'label'"
        @select="getNewCompare"
      />
    </el-col>
    <el-col :span="8"></el-col>
    <el-col :span="8">
      <el-autocomplete
        v-model="location2"
        placeholder="请选择城市2"
        :fetch-suggestions="querySearch"
        clearable
        class="inline-input w-50"
        highlight-first-item
        :value-key="'label'"
        @select="getNewCompare"
      />
    </el-col>
  </el-row>
  <el-row :gutter="2">
    <div
      id="chart_compare"
      ref="chart_compare"
      style="width: 600px; height: 400px; padding: 10px; margin: 0 auto"
    ></div>
  </el-row>
</template>
<script lang="ts" setup>
import * as echarts from "echarts";
import { get } from "@/api/index";
import { china_cities } from "@/stores/cities";
import { CityWeatherData } from "@/types/weather";
const location1 = ref("");
const location2 = ref("");

interface LabelItem {
  label: string;
  value: string;
}
const labels = ref<LabelItem[]>([]);
const querySearch = (queryString: string, cb: any) => {
  const results = queryString
    ? labels.value.filter(createFilter(queryString))
    : labels.value;
  cb(results);
};
const createFilter = (queryString: string) => {
  return (restaurant: LabelItem) => {
    return (
      restaurant.label.toLowerCase().indexOf(queryString.toLowerCase()) === 0
    );
  };
};
const loadAll = () => {
  return china_cities;
};
watch(
  () => location1,
  () => {
    if (location1.value == "") {
      getNewCompare();
    }
  }
);
watch(
  () => location2,
  () => {
    if (location2.value == "") {
      getNewCompare();
    }
  }
);
const getNewCompare = async () =>
  Promise.all([getPresentCity1(), getPresentCity2()]).then(() => {
    setTimeout(() => {
      let render1: number[] = getValueList1();
      let render2: number[] = getValueList2();
      renderChart(render1, render2);
    }, 500);
  });
interface CityInfoResponse {
  status: boolean;
  message: CityWeatherData;
}
const cityMessage1 = ref<CityWeatherData>({} as CityWeatherData);
const cityMessage2 = ref<CityWeatherData>({} as CityWeatherData);
let chartInstance_compare: echarts.ECharts | null = null;
const getPresentCity1 = async () => {
  if (location1.value == "") {
    return;
  }
  get<CityInfoResponse>("/api/getCityInfo/", {
    city: location1.value,
  }).then((res) => {
    cityMessage1.value.time = res.data.message.time;
    cityMessage1.value.city = res.data.message.city;
    cityMessage1.value.temp = res.data.message.temp;
    cityMessage1.value.text = res.data.message.text;
    cityMessage1.value.precip = res.data.message.precip;
    cityMessage1.value.wind360 = res.data.message.wind360;
    cityMessage1.value.windScale = res.data.message.windScale;
    cityMessage1.value.windSpeed = res.data.message.windSpeed;
    cityMessage1.value.humidity = res.data.message.humidity;
    cityMessage1.value.pressure = res.data.message.pressure;
    cityMessage1.value.aqi = res.data.message.aqi;
    cityMessage1.value.category = res.data.message.category;
  });
};
const getPresentCity2 = async () => {
  if (location2.value == "") {
    return;
  }
  get<CityInfoResponse>("/api/getCityInfo/", {
    city: location2.value,
  }).then((res) => {
    cityMessage2.value.time = res.data.message.time;
    cityMessage2.value.city = res.data.message.city;
    cityMessage2.value.temp = res.data.message.temp;
    cityMessage2.value.text = res.data.message.text;
    cityMessage2.value.precip = res.data.message.precip;
    cityMessage2.value.wind360 = res.data.message.wind360;
    cityMessage2.value.windScale = res.data.message.windScale;
    cityMessage2.value.windSpeed = res.data.message.windSpeed;
    cityMessage2.value.humidity = res.data.message.humidity;
    cityMessage2.value.pressure = res.data.message.pressure;
    cityMessage2.value.aqi = res.data.message.aqi;
    cityMessage2.value.category = res.data.message.category;
  });
};
const getKeyList = function () {
  let keyList: string[] = [];
  keyList.push("温度");
  keyList.push("降水");
  keyList.push("风向");
  keyList.push("风级");
  keyList.push("风速");
  keyList.push("湿度");
  keyList.push("气压");
  keyList.push("AQI");
  return keyList;
};
const getValueList1 = function () {
  let valueList: any[] = [];
  let temp_json = {
    name: "温度",
    // value: cityMessage1.value.temp || 0,
    value:
      (
        cityMessage1.value.temp /
        (cityMessage1.value.temp + cityMessage2.value.temp)
      ).toFixed(2) || 0.5,
    sum: 30,
  };
  let precip_json = {
    name: "降水量",
    // value: cityMessage1.value.precip || 0,
    value:
      (
        cityMessage1.value.precip /
        (cityMessage1.value.precip + cityMessage2.value.precip)
      ).toFixed(2) || 0.5,
    sum: 30,
  };
  let wind360_json = {
    name: "风向",
    // value: cityMessage1.value.wind360 || 0,
    value:
      (
        cityMessage1.value.wind360 /
        (cityMessage1.value.wind360 + cityMessage2.value.wind360)
      ).toFixed(2) || 0.5,
    sum: 20,
  };
  let windScale_json = {
    name: "风级",
    // value: cityMessage1.value.windScale || 0,
    value:
      (
        cityMessage1.value.windScale /
        (cityMessage1.value.windScale + cityMessage2.value.windScale)
      ).toFixed(2) || 0.5,
    sum: 10,
  };
  let windSpeed_json = {
    name: "风速",
    // value: cityMessage1.value.windSpeed || 0,
    value:
      (
        cityMessage1.value.windSpeed /
        (cityMessage1.value.windSpeed + cityMessage2.value.windSpeed)
      ).toFixed(2) || 0.5,
    sum: 10,
  };
  let humidity_json = {
    name: "湿度",
    // value: cityMessage1.value.humidity || 0,
    value:
      (
        cityMessage1.value.humidity /
        (cityMessage1.value.humidity + cityMessage2.value.humidity)
      ).toFixed(2) || 0.5,
    sum: 10,
  };
  let pressure_json = {
    name: "气压",
    // value: cityMessage1.value.pressure || 0,
    value:
      (
        cityMessage1.value.pressure /
        (cityMessage1.value.pressure + cityMessage2.value.pressure)
      ).toFixed(2) || 0.5,
    sum: 10,
  };
  let aqi_json = {
    name: "AQI",
    // value: cityMessage1.value.aqi || 0,
    value:
      (
        cityMessage1.value.aqi /
        (cityMessage1.value.aqi + cityMessage2.value.aqi)
      ).toFixed(2) || 0.5,
    sum: 10,
  };
  valueList.push(temp_json);
  valueList.push(precip_json);
  valueList.push(wind360_json);
  valueList.push(windScale_json);
  valueList.push(windSpeed_json);
  valueList.push(humidity_json);
  valueList.push(pressure_json);
  valueList.push(aqi_json);
  return valueList;
};
const getValueList2 = function () {
  let valueList: any[] = [];
  let temp_json = {
    name: "温度",
    // value: cityMessage2.value.temp || 0,
    value:
      (
        cityMessage2.value.temp /
        (cityMessage1.value.temp + cityMessage2.value.temp)
      ).toFixed(2) || 0.5,
    sum: 20,
  };
  let precip_json = {
    name: "降水量",
    // value: cityMessage2.value.precip || 0,
    value:
      (
        cityMessage2.value.precip /
        (cityMessage1.value.precip + cityMessage2.value.precip)
      ).toFixed(2) || 0.5,
    sum: 20,
  };
  let wind360_json = {
    name: "风向",
    // value: cityMessage2.value.wind360 || 0,
    value:
      (
        cityMessage2.value.wind360 /
        (cityMessage1.value.wind360 + cityMessage2.value.wind360)
      ).toFixed(2) || 0.5,
    sum: 20,
  };
  let windScale_json = {
    name: "风级",
    // value: cityMessage2.value.windScale || 0,
    value:
      (
        cityMessage2.value.windScale /
        (cityMessage1.value.windScale + cityMessage2.value.windScale)
      ).toFixed(2) || 0.5,
    sum: 20,
  };
  let windSpeed_json = {
    name: "风速",
    // value: cityMessage2.value.windSpeed || 0,
    value:
      (
        cityMessage2.value.windSpeed /
        (cityMessage1.value.windSpeed + cityMessage2.value.windSpeed)
      ).toFixed(2) || 0.5,
    sum: 20,
  };
  let humidity_json = {
    name: "湿度",
    // value: cityMessage2.value.humidity || 0,
    value:
      (
        cityMessage2.value.humidity /
        (cityMessage1.value.humidity + cityMessage2.value.humidity)
      ).toFixed(2) || 0.5,
    sum: 20,
  };
  let pressure_json = {
    name: "气压",
    // value: cityMessage2.value.pressure || 0,
    value:
      (
        cityMessage2.value.pressure /
        (cityMessage1.value.pressure + cityMessage2.value.pressure)
      ).toFixed(2) || 0.5,
    sum: 20,
  };
  let aqi_json = {
    name: "AQI",
    // value: cityMessage2.value.aqi || 0,
    value:
      (
        cityMessage2.value.aqi /
        (cityMessage1.value.aqi + cityMessage2.value.aqi)
      ).toFixed(2) || 0.5,
    sum: 20,
  };
  valueList.push(temp_json);
  valueList.push(precip_json);
  valueList.push(wind360_json);
  valueList.push(windScale_json);
  valueList.push(windSpeed_json);
  valueList.push(humidity_json);
  valueList.push(pressure_json);
  valueList.push(aqi_json);
  return valueList;
};
onMounted(() =>
  Promise.all([getPresentCity1(), getPresentCity2()]).then(() => {
    labels.value = loadAll();
    setTimeout(() => {
      renderChart(getValueList1(), getValueList2());
    }, 1000);
  })
);
const renderChart = async (data1: number[], data2: number[]) => {
  const colorLeft = ["#3DA1FF", "#2749FC"];
  const colorRight = ["#FB857D", "#F6504A"];
  if (!chartInstance_compare) {
    const chartDom_compare = document.getElementById("chart_compare");
    chartInstance_compare = echarts.init(chartDom_compare);
  }
  const option = {
    title: {
      text: "城市数据比较",
      left: "center",
      textStyle: {
        fontWeight: "bold",
      },
    },
    legend: {
      top: "5%",
      right: "10%",
      itemWidth: 50,
      itemHeight: 22,
      itemGap: 40,
      orient: "horizontal",
      icon: "circle",
      textStyle: {
        color: "#fff",
        fontSize: 14,
      },
    },
    grid: [
      {
        show: false,
        left: "2%",
        top: "10%",
        bottom: "8%",
        width: "40%",
      },
      {
        show: false,
        left: "50%",
        top: "10%",
        bottom: "8%",
        width: "0%",
      },
      {
        show: false,
        right: "2%",
        top: "10%",
        bottom: "8%",
        width: "40%",
      },
    ],
    tooltip: {
      show: true,
      formatter: function (params: any) {
        let tooltipContent = "";
        console.log(params);
        let originalValue = params.data;
        // if (params.seriesName === "城市1") {
        if (originalValue.name === "温度") {
          originalValue = (
            originalValue.value *
            (cityMessage1.value.temp + cityMessage2.value.temp)
          ).toFixed(0);
        } else if (originalValue.name === "降水量") {
          originalValue = (
            originalValue.value *
            (cityMessage1.value.precip + cityMessage2.value.precip)
          ).toFixed(0);
        } else if (originalValue.name === "风向") {
          originalValue = (
            originalValue.value *
            (cityMessage1.value.wind360 + cityMessage2.value.wind360)
          ).toFixed(0);
        } else if (originalValue.name === "风级") {
          originalValue = (
            originalValue.value *
            (cityMessage1.value.windScale + cityMessage2.value.windScale)
          ).toFixed(0);
        } else if (originalValue.name === "风速") {
          originalValue = (
            originalValue.value *
            (cityMessage1.value.windSpeed + cityMessage2.value.windSpeed)
          ).toFixed(0);
        } else if (originalValue.name === "湿度") {
          originalValue = (
            originalValue.value *
            (cityMessage1.value.humidity + cityMessage2.value.humidity)
          ).toFixed(0);
        } else if (originalValue.name === "气压") {
          originalValue = (
            originalValue.value *
            (cityMessage1.value.pressure + cityMessage2.value.pressure)
          ).toFixed(0);
        } else if (originalValue.name === "AQI") {
          originalValue = (
            originalValue.value *
            (cityMessage1.value.aqi + cityMessage2.value.aqi)
          ).toFixed(0);
        }
        // } else if (params.seriesName === "城市2") {
        // }
        tooltipContent += `${params.marker} ${params.name}: ${originalValue}<br/>`;
        return tooltipContent;
      },
    },
    xAxis: [
      {
        min: 0,
        max: 1,
        type: "value",
        inverse: true,
        axisLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        position: "bottom",
        axisLabel: {
          show: false,
        },
        splitLine: {
          show: false,
        },
      },
      {
        gridIndex: 1,
        show: false,
      },
      {
        min: 0,
        max: 1,
        gridIndex: 2,
        show: false,
        type: "value",
        inverse: false,
        axisLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        position: "bottom",
        axisLabel: {
          show: true,
        },
        splitLine: {
          show: false,
        },
      },
    ],
    yAxis: [
      {
        gridIndex: 0,
        triggerEvent: true,
        show: true,
        inverse: true,
        data: getKeyList(),
        axisLine: {
          show: false,
        },
        splitLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        axisLabel: {
          show: false,
        },
      },
      {
        gridIndex: 1,
        type: "category",
        inverse: true,
        position: "left",
        axisLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        axisLabel: {
          show: true,
          interval: 0,
          align: "auto",
          verticalAlign: "middle",
        },
        data: getKeyList(),
      },
      {
        gridIndex: 2,
        triggerEvent: true,
        show: true,
        inverse: true,
        data: getKeyList(),
        axisLine: {
          show: false,
        },
        splitLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        axisLabel: {
          show: false,
        },
      },
    ],
    series: [
      {
        type: "bar",
        gridIndex: 0,
        borderRadius: [10, 0, 0, 10],
        xAxisIndex: 0,
        yAxisIndex: 0,
        data: data1,
        barWidth: 20,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(
            0,
            0,
            1,
            0,
            [
              {
                offset: 0,
                color: colorLeft[0],
              },
              {
                offset: 1,
                color: colorLeft[1],
              },
            ],
            false
          ),
        },
        label: {
          show: false,
          position: "insideRight",
        },
      },
      {
        type: "bar",
        xAxisIndex: 2,
        yAxisIndex: 2,
        gridIndex: 2,
        showBackground: true,
        borderRadius: [0, 10, 10, 0],
        data: data2,
        barWidth: 20,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(
            0,
            0,
            1,
            0,
            [
              {
                offset: 0,
                color: colorRight[0],
              },
              {
                offset: 1,
                color: colorRight[1],
              },
            ],
            false
          ),
        },
        label: {
          show: false,
          position: "insideLeft",
        },
      },
    ],
  };
  chartInstance_compare.setOption(option);
};
addEventListener(
  "resize",
  function () {
    chartInstance_compare.resize();
  },
  false
);
</script>
<style lang="scss" scoped>
#chart_compare {
  position: relative;
  width: 100%;
  height: 100%;
  background: #ffffff;
  border-radius: 0.5rem;
  .title {
    position: absolute;
    top: 0;
    left: 1rem;
    font-size: 1.13rem;
    font-weight: bold;
    color: #333333;
    .title-left {
      display: inline-block;
      width: 0.25rem;
      height: 1rem;
      background: linear-gradient(180deg, #3ea2ff 0%, #2746fc 100%);
      border-radius: 0.13rem;
      margin-right: 1rem;
    }
  }
  .footer-name {
    position: absolute;
    bottom: 0;
    color: #333333;
    font-size: 0.88rem;
    width: 100%;
    p {
      display: inline-block;
      width: 50%;
      padding: 0 3rem;
    }
    p:nth-of-type(1) {
      text-align: right;
    }
  }
}
</style>
