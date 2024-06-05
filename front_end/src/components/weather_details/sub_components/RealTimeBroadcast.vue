<template>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/qweather-icons@1.3.0/font/qweather-icons.css">
  <div class="common-layout" style="background:white;">
    <!-- {{ city }} -->
    <el-container>
      <el-header>
        <div id="chart_temp_perhour" ref="chart_temp_perhour" style="height: 120px;  width: 100%;  margin: 0 auto">
        </div>
      </el-header>
      <el-main style="padding: 2px;">
        <div class="calendar-container">
          <el-row :gutter="0" justify="center">
            <!-- <div style="margin: -10px;"> -->
            <!-- <el-col :span="2">
              <div class="day-content" style="margin-top: 26px;">
                <div class="temperature">天气</div>
                <div class="temperature">温度</div>
                <div class="humidity">湿度</div>
                <div class="wind-speed">风速</div>
                <div class="wind-speed">风向</div>
                <div class="time">时间</div>
              </div>
            </el-col> -->
            <!-- </div> -->
            <el-col :span="2" v-for="(day, index) in realTimeWeatherList" :key="index">
              <div class="ep-bg-purple-dark" />
              <!-- <div style="height:70% !important"> -->
              <el-card :body-style="{ padding: '0px', paddingTop: '20px', paddingBottom: '20px' }" style="width:auto"
                shadow="hover">
                <div class="info-text">{{ day.temperature }}℃</div>
                <div class="icon-couple">
                  <!-- {{day.condition_icon  }} -->
                  <!-- <i class="qi-${day.condition_icon}" style="font-size: 25px;"></i> -->
                  <i class="perhour-icon" :class="'qi-' + day.condition_icon"></i>
                  <div class="tips-text">{{ day.condition }}</div>
                </div>
                <div class="icon-couple">
                  <div style="display: flex; justify-content: center;">
                    <el-icon size="25px" class="perhour-icon"
                      :style="{ transform: `rotate(${calculateAngle(day.wind360)}deg)` }">
                      <Position />
                    </el-icon>
                  </div>
                  <div class="tips-text">{{ day.windScale }}级风</div>
                </div>
                <div class="info-text">{{ day.time }}</div>
              </el-card>
            </el-col>
          </el-row>

        </div>
      </el-main>
    </el-container>
  </div>




</template>


<script lang="ts" setup>
import * as echarts from "echarts";
import { get } from "@/api/index.ts";
import { china_cities } from "@/stores/cities";
import { SelectProps } from "element-plus/es/components/select/src/select.mjs";


const props = defineProps({
  city: { type: Object }
})
// // 定义子组件的方法
// const refresh = () => {
//   get_data();
//   renderChart(
//     realTimeWeatherList.value
//   );
// };
// // 暴露方法
// defineExpose({ refresh });


// const city = ref({
//   name: '北京市',
//   adm2: '海淀区'
// });
const realTimeWeatherList = ref<RealTimeWeather[]>([]);
const calculateAngle = (wind360: number) => wind360 + 135;
interface RealTimeWeather {
  time: string,
  condition: string,
  condition_icon: number,
  temperature: number,
  humidity: number,
  windScale: number,
  windDirection: string,
  wind360: number
}

interface RealTimeWeatherData {
  realTimeWeatherList: RealTimeWeather[];
}

const get_data = async () => {
  get<RealTimeWeatherData>("/api/weather/overview_realtime/", { city: props.city }).then((res) => {
    realTimeWeatherList.value.splice(0, realTimeWeatherList.value.length, ...res.data.realTimeWeatherList);
    // console.log("getdata")
    if (realTimeWeatherList.value.length > 12) {
      realTimeWeatherList.value = realTimeWeatherList.value.slice(0, 12);
    }
  });
};

watch(() => props.city, () => Promise.all([get_data()]).then(() => {
  renderChart(
    realTimeWeatherList.value,
  );
}));

// 初始化 ECharts 实例
let chartInstance_history: echarts.ECharts | null = null;
// interface tempNode {
//   time: string;
//   temp: number;
// }
// interface TempChangeResponse {
//   status: boolean;
//   data: tempNode[];
// }
// const TempDataList = ref<tempNode[]>([]);
// const fetchCityTempChange = async () =>
//   get<TempChangeResponse>("/api/weather/overview_realtime/temp/", {
//     city: selectedLocation.value,
//   }).then((res) => {
//     realTimeWeatherList.value.splice(0, realTimeWeatherList.value.length, ...res.data.data);
//   });

const renderChart = async (
  tempData: RealTimeWeather[]
) => {
  if (!chartInstance_history) {
    const chartDom_history = document.getElementById("chart_temp_perhour");
    chartInstance_history = echarts.init(chartDom_history);
  }
  chartInstance_history.setOption({
    // Adjusted to have only one visualMap for all series
    visualMap: {
      show: false,
      type: "continuous",
      seriesIndex: 0, // This is now referring to the first (and only) series index that needs a visualMap
      min: 15,
      max: 30,
      color: ['red', 'blue',],// 使用内置的蓝到红的渐变色
      itemHeight: 60, // 调整图例的高度
      itemWidth: 12
    },

    title: [
      {
        top: "0%",
        left: "center",
        // text: "多指标变化趋势图",
      },
    ],
    tooltip: {
      trigger: "axis",
      formatter: function (params: any) {
        let tooltipContent = "";

        params.forEach(function (param: any, index) {
          switch (param.seriesName) {
            case "温度":
              tooltipContent += `${param.marker} ${param.seriesName}: ${param.value} °C<br/>`;
              break;
            case "湿度":
              tooltipContent += `${param.marker} ${param.seriesName}: ${param.value}%<br/>`;
              break;
            case "AQI":
              tooltipContent += `${param.marker} ${param.seriesName}: ${param.value}<br/>`;
              break;
            case "气压":
              tooltipContent += `${param.marker} ${param.seriesName}: ${param.value} hPa<br/>`;
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
      axisLabel: {//坐标轴刻度标签
        show: false
      },
      axisLine: {//坐标轴轴线
        show: false
      },
      axisTick: {//坐标轴刻度
        show: false
      }
    },
    yAxis: {
      splitLine: {//坐标轴在grid区域中的分割线
        show: false
      },
      axisLabel: {//坐标轴刻度标签
        show: false
      },

    },

    grid: {
      // top: "20%",
      // bottom: "20%",
      // left: "10%",
      // right: "10%",
      top: "10%",
      bottom: "-30%",
      left: "-2%",
      right: "-2%",
      containLabel: true,
    },
    // legend: {
    //   orient: "horizontal",
    //   left: "right",
    //   top: "top",
    //   data: ["温度", "湿度", "AQI", "气压"],
    // },

    series: [
      {
        type: "line",
        showSymbol: false,
        name: "温度",
        data: tempData.map((item) => item.temperature),
        markPoint: {
          data: [
            // { type: 'max', name: '最大值' },
            // { type: 'min', name: '最小值' }
            { type: 'max', name: '最大值', symbol: 'circle', symbolSize: 25, itemStyle: { color: 'red' } },
            { type: 'min', name: '最小值', symbol: 'circle', symbolSize: 25, itemStyle: { color: 'blue' } }
          ]

        },
        smooth: true // 这里设置平滑曲线
      }
    ],
  });
};
// onMounted(() => Promise.all([get_data()]).then(() => {
//   // get_data();
//   renderChart(
//     realTimeWeatherList.value
//   );

//   // window.addEventListener("click", () => {
//   //   if (chartInstance_history) {
//   //     renderChart(
//   //       realTimeWeatherList.value
//   //     );
//   //     chartInstance_history.resize();
//   //   }
//   // });
//   // window.addEventListener("resize", () => {
//   //   if (chartInstance_history) {
//   //     renderChart(
//   //       realTimeWeatherList.value
//   //     );
//   //     chartInstance_history.resize();
//   //   }
//   // });
// }));
onMounted(() => Promise.all([get_data()]).then(() => {
  console.log(realTimeWeatherList.value);
  setTimeout(() => {
    renderChart(
      realTimeWeatherList.value
    );
  }, 1000);
  // renderChart(
  //   realTimeWeatherList.value
  // );
  window.addEventListener("click", () => {
    if (chartInstance_history) {
      renderChart(
        realTimeWeatherList.value
      );
      chartInstance_history.resize();
    }
  });
  window.addEventListener("resize", () => {
    if (chartInstance_history) {
      renderChart(
        realTimeWeatherList.value
      );
      chartInstance_history.resize();
    }
  });
}));
</script>


<style lang="scss" scoped>
.calendar-container {
  margin-top: 2vh;
  padding: 0px;
}

.calendar-grid {
  display: flex;
  justify-content: space-between;
}

.calendar-column {
  width: 100%;
}

.day-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0px;
}

.weather-icon img {
  max-width: 50px;
  max-height: 50px;
}

.temperature,
.humidity,
.wind-speed,
.time {
  margin-top: 10px;
}

.icon-couple {
  margin-top: 12px;
  margin-bottom: 12px;
}

.perhour-icon {
  font-size: 25px;
  margin-bottom: 10px;
  display: flex;
  justify-content: center;
  /* 水平居中 */
}

.tips-text {
  font-size: 14px;
  font-family: 'Courier New', Courier, monospace;
  display: flex;
  justify-content: center;
  /* 水平居中 */
}

.info-text {
  font-size: 25x;
  display: flex;
  justify-content: center;
  /* 水平居中 */
}

.el-card {
  // background-color: rgb(188, 243, 243);
  background-color: transparent;
  /* 设置背景色为透明 */
  padding: 0px;
  margin: 0px;
  border-radius: 20px;
  border-color: transparent;
  // color: #5d617a;
  color: black;
}

.el-card:hover {
  margin-top: -10px;
  margin: -1px;
  color: #409EFF;
}
</style>
