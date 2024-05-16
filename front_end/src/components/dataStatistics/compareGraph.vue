<template>
  <el-row :gutter="2">
    <el-col :span="8">
      <el-select
        v-model="location1"
        placeholder="请选择城市1"
        clearable
        @change="getNewCompare"
      >
        <el-option
          v-for="location in locations"
          :key="location.value"
          :label="location.label"
          :value="location.value"
        ></el-option>
      </el-select>
    </el-col>
    <el-col :span="8"></el-col>
    <el-col :span="8">
      <el-select
        v-model="location2"
        placeholder="请选择城市2"
        clearable
        @change="getNewCompare"
      >
        <el-option
          v-for="location in locations"
          :key="location.value"
          :label="location.label"
          :value="location.value"
        ></el-option>
      </el-select>
    </el-col>
  </el-row>
  <el-row :gutter="2">
    <div
      id="chart_compare"
      ref="chart_compare"
      style="width: 400px; height: 400px; padding: 10px; margin: 0 auto"
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
const getNewCompare = async () =>
  Promise.all([getPresentCity1(), getPresentCity2()]).then(() => {
    console.log(cityMessage1.value);
    console.log(cityMessage2.value);
    renderChart(getValueList1(), getValueList2());
  });
interface CityInfoResponse {
  status: boolean;
  message: CityWeatherData;
}
const cityMessage1 = ref<CityWeatherData>({} as CityWeatherData);
const cityMessage2 = ref<CityWeatherData>({} as CityWeatherData);
let chartInstance_compare: echarts.ECharts | null = null;
const getPresentCity1 = async () => {
  get<CityInfoResponse>("/api/getCityInfo/", {
    city: location1.value,
  }).then((res) => {
    console.log(res.data.message);
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
    console.log("city1", cityMessage1.value);
  });
};
const getPresentCity2 = async () => {
  get<CityInfoResponse>("/api/getCityInfo/", {
    city: location2.value,
  }).then((res) => {
    console.log(res.data.message);
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
    console.log("city2", cityMessage2.value);
  });
};
const locations = china_cities;
const getKeyList = function () {
  let keyList: string[] = [];
  keyList.push("温度");
  keyList.push("降水");
  keyList.push("风速");
  keyList.push("风级");
  keyList.push("风速");
  keyList.push("湿度");
  keyList.push("气压");
  keyList.push("AQI");
  console.log(keyList);
  return keyList;
};
const getValueList1 = function () {
  console.log("get", cityMessage2);
  let valueList: any[] = [];
  let temp_json = {
    name: "温度",
    value: cityMessage1.value.temp || 0,
    sum: 30,
  };
  let precip_json = {
    name: "降水量",
    value: cityMessage1.value.precip || 0,
    sum: 30,
  };
  let wind360_json = {
    name: "风速",
    value: cityMessage1.value.wind360 || 0,
    sum: 20,
  };
  let windScale_json = {
    name: "风级",
    value: cityMessage1.value.windScale || 0,
    sum: 10,
  };
  let windSpeed_json = {
    name: "风速",
    value: cityMessage1.value.windSpeed || 0,
    sum: 10,
  };
  let humidity_json = {
    name: "湿度",
    value: cityMessage1.value.humidity || 0,
    sum: 10,
  };
  let pressure_json = {
    name: "气压",
    value: cityMessage1.value.pressure || 0,
    sum: 10,
  };
  let aqi_json = {
    name: "AQI",
    value: cityMessage1.value.aqi || 0,
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
  console.log(valueList);
  return valueList;
};
const getValueList2 = function () {
  console.log("get", cityMessage2);
  let valueList: any[] = [];
  let temp_json = {
    name: "温度",
    value: cityMessage2.value.temp || 0,
    sum: 30,
  };
  let precip_json = {
    name: "降水量",
    value: cityMessage2.value.precip || 0,
    sum: 30,
  };
  let wind360_json = {
    name: "风速",
    value: cityMessage2.value.wind360 || 0,
    sum: 20,
  };
  let windScale_json = {
    name: "风级",
    value: cityMessage2.value.windScale || 0,
    sum: 20,
  };
  let windSpeed_json = {
    name: "风速",
    value: cityMessage2.value.windSpeed || 0,
    sum: 20,
  };
  let humidity_json = {
    name: "湿度",
    value: cityMessage2.value.humidity || 0,
    sum: 20,
  };
  let pressure_json = {
    name: "气压",
    value: cityMessage2.value.pressure || 0,
    sum: 20,
  };
  let aqi_json = {
    name: "AQI",
    value: cityMessage2.value.aqi || 0,
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
  console.log(valueList);
  return valueList;
};
onMounted(() =>
  Promise.all([getPresentCity1(), getPresentCity2()]).then(() => {
    console.log(cityMessage1, cityMessage2);
    renderChart(getValueList1(), getValueList2());
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
      data: ["城市A", "城市B"],
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
      formatter: "{b} : {c}",
    },
    xAxis: [
      {
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
        gridIndex: 2,
        show: true,
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
