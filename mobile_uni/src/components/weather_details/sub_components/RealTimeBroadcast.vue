<template>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/qweather-icons@1.3.0/font/qweather-icons.css">
  <div class="scroll-layout background-transparent">
    <el-select v-model="selectedDate" :placeholder="selectedDate" @change="handleChange" style="width: 150px;border-radius: 50px;">
    <el-option
      v-for="option in dateOptions"
      :key="option.value"
      :label="option.label"
      :value="option.value">
    </el-option>
  </el-select>
    <el-container>
      <el-header>
        <div id="chart_temp_perhour" ref="chart_temp_perhour" class="chart-container">
        </div>
      </el-header>
      <el-main style="padding-left: 0;padding-right:0;">
        <el-row :gutter="0">
          <el-col :span="2" v-for="(day, index) in realTimeWeatherList" :key="index" class="calendar-column">
            <div class="ep-bg-purple-dark" />
            <el-card :body-style="{ padding: '0px', paddingTop: '20px', paddingBottom: '20px' }" class="card-container" shadow="hover">
              <div class="info-text">{{ day.temperature }}℃</div>
              <div class="perhour-icon">
                <i :class="'qi-' + day.condition_icon" class="icon" />
                <!-- <div class="tips-text">{{ day.condition }}</div> -->
              </div>
              <div class="perhour-icon">
                <div style="display: flex; justify-content: center;">
                    <el-icon size="20px" class="wind-icon"
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
  get<RealTimeWeatherData>("/api/weather/overview_realtime/", { city: props.city,selectedDate:selectedDate.value }).then((res) => {
    realTimeWeatherList.value.splice(0, realTimeWeatherList.value.length, ...res.data.realTimeWeatherList);
    // console.log("getdata")
    if (realTimeWeatherList.value.length > 12) {
      realTimeWeatherList.value = realTimeWeatherList.value.slice(0, 12);
    }
  });
};

watch(() => props.city, () => Promise.all([get_data()]).then(() => {
  selectedDate.value=new Date().toISOString().substr(0, 10);
  renderChart(
    realTimeWeatherList.value,
  );
}));

// 日期切换选择
const selectedDate = ref(new Date().toISOString().substr(0, 10)); // 初始化为今天的日期
const dateOptions = ref([]);

function generateDateOptions() {
  const today = new Date();
  for (let i = -5; i <= 5; i++) {
    const date = new Date(today);
    date.setDate(today.getDate() + i);
    const formattedDate = formatDate(date);
    dateOptions.value.push({ label: formattedDate, value: formattedDate });
  }
}

function formatDate(date) {
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function handleChange(value) {
  console.log(selectedDate.value);
  Promise.all([get_data()]).then(() => {
    renderChart(realTimeWeatherList.value);
  });
  // 等待 300 毫秒
  setTimeout(() => {
    // 获取数据并渲染图表
    renderChart(realTimeWeatherList.value);
  }, 300);

  //   get_data().then(() => {
  //   renderChart(realTimeWeatherList.value);
  // });
}

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
      bottom: "-50%",
      left: "-3%",
      right: "-3%",
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
            { type: 'max', name: '最大值', symbol: 'circle', symbolSize: 30, itemStyle: { color: 'red' } },
            { type: 'min', name: '最小值', symbol: 'circle', symbolSize: 30, itemStyle: { color: 'blue' } }
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
  generateDateOptions();
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



<style scoped>
:deep(.el-select__wrapper ) {
  background-color: rgba(255,255,255,0);
}

:deep(.el-select__placeholder ) {
  color: black;
}

.background-transparent {
  background: transparent;
  border-color: transparent;
}

.max-md-bg-gradient {
  background-color: #67E1D2;
  box-shadow: 0 10px 30px -12px rgba(7, 89, 133, 0.45);
}

.scroll-layout {
  width: 800px;
}

.chart-container {
  height: 100px;
  width: 100%;
  margin: 0 auto;
}

.calendar-container {
  margin-top: 0vh;
  padding: 0px;
}

.calendar-grid {
  display: flex;
  justify-content: space-between;
}

.calendar-column {
  width: 100%;
}

.card-container {
  background-color: transparent;
  margin: 0px;
  border-radius: 20px;
  border-color: transparent;
  color: black;
}

.card-container:hover {
  margin-top: -10px;
  margin: -1px;
  color: wheat;
}

.perhour-icon {
  font-size: 25px;
  margin-top: 30px;
  margin-bottom: 30px;
  display: flex;
  justify-content: center;
  /* 水平居中 */
}
.icon {
  font-size: 20px;
}

.wind-icon {
  margin-bottom: 0px;
}

.tips-text {
  font-size: 10px;
  font-family: 'Courier New', Courier, monospace;
  display: flex;
  justify-content: center;
  /* 水平居中 */
}

.info-text {
  font-size: 15px;
  display: flex;
  justify-content: center;
  /* 水平居中 */
}
</style>