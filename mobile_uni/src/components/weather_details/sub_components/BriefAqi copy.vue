<template>
  <!-- {{ city }} -->
  <div class="air-quality-indicator">
    <div class="location quality-description"> 
      空气质量
    </div>
    <!-- <div class="quality-circle">
      <div class="quality-level text-gray-200">{{ aqi_ }}</div>
    </div> -->
    <!-- <el-card style="width: 100%;"> -->
        <div id="chart_brief_aqi_bar" ref="chart_brief_aqi_bar" style="height: 220px;  width: 100%;  margin: 0 auto">
        </div>
        

    <el-tooltip effect="light">
      <template #content>
        <el-row>
          <el-col :span="24" class="rounded-lg shadow-md p-2" style="width: 40vh;">
            <el-row :gutter="2">
              <el-col :span="8">
                <p class="text-xs text-center font-bold" :style="colorClass(levelInfo.color)">
                  {{ levelInfo.name }}
                </p>
                <p class="text-xs text-center">
                  {{ levelInfo.range }}
                </p>
              </el-col>
              <el-col :span="16">
                <p class="text-center text-xs text-black">{{ levelInfo.description }}</p>
              </el-col>
            </el-row>
            <!-- </div> -->
          </el-col>
        </el-row>
      </template>
      <!-- <el-row>
        <el-col :span="9"> -->
      <el-button class="quality-description text-slate-600" style="border: none;">
        {{ category_ }}
      </el-button>
      <!-- </el-col> -->
      <!-- <el-col :span="15">
          helo
        </el-col>
      </el-row> -->
    </el-tooltip>

    <div style="margin-top: 10%;font-size: 20px">
          <el-row :gutter="30" v-for="(value, key) in pollutionList">
            <el-col :span="15">
              <div>
                {{ key }}
              </div>
            </el-col>
            <el-col :span="7">
              <div>{{ value }}</div>
            </el-col>
          </el-row>
        </div>

    <!-- </el-card> -->



    <!-- 下方显示提示信息 -->
    <!-- <div @mouseover="showHover = true" @mouseout="showHover = false" class="quality-circle">
      <div class="quality-level text-gray-200">{{ aqi }}</div>
    </div> -->
    <!-- <div class="quality-description text-slate-600 ml-2">
      {{ category.value }}
    </div> -->
    <!-- <div class="hover_container" v-if="showHover">
      <el-row>
        <el-col :span="24" class="rounded-lg shadow-md border-2 p-2">
          <el-row :gutter="2">
            <el-col :span="8">
              <p class="text-xl text-center font-bold" :style="colorClass(levelInfo.color)">
                {{ levelInfo.name }}
              </p>
              <p class="text-center text-xl">
                {{ levelInfo.range }}
              </p>
            </el-col>
            <el-col :span="16">
              <p class="text-center text-sm text-black">{{ levelInfo.description }}</p>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
    </div> -->

  </div>
</template>
<script lang="ts" setup>
import { get } from "@/api/index.ts";
// import 'qweather-icons/dist/qweather-icons.css';

const props = defineProps({
  city: { type: Object }
})


// interface AqiData {
//   aqi: number;
//   category: string;
//   pollutionList: PollutionList[];
// }
// interface PollutionList {
//   type: string;
//   value: number;
// }
const aqi_ = ref(0);
const category_ = ref("优");
const pollutionList = ref({});
//   [
//   { type: 'PM10', value: 10 },
//   { type: 'PM2.5', value: 20 },
//   { type: 'NO2', value: 10 },
//   { type: 'SO2', value: 10 },
//   { type: 'O3', value: 10 },
//   { type: 'CO', value: 10 },
// ]
/**
 * Request
 */
interface AqiData {
  aqi: number;
  category: string;
  CO: number;
  NO2: number;
  O3: number;
  PM10: number;
  "PM2.5": number;
  SO2: number;
}
const getPresentCityAqi = async () => {
  get<AqiData>("/api/weather/aqi/", { city: props.city }).then((res) => {
    aqi_.value = res.data.aqi;
    category_.value = res.data.category;
    const { aqi, category, ...rest } = res.data;
    pollutionList.value = rest;
  });
};



// 
const levels = [
  {
    name: "优",
    color: "green",
    range: "0-50",
    description: "空气质量令人满意，基本无空气污染。各类人群可正常活动。",
  },
  {
    name: "良",
    color: "yellow",
    range: "51-100",
    description:
      "空气质量可接受，但某些污染物可能对极少数异常敏感人群健康有较弱影响。",
  },
  {
    name: "轻度污染",
    color: "orange",
    range: "101-150",
    description:
      "易感人群症状有轻度加剧，健康人群出现刺激症状，一般人群无明显不适。",
  },
  {
    name: "中度污染",
    color: "red",
    range: "151-200",
    description: "进一步加剧易感人群症状，可能对健康人群心脏、呼吸系统有影响。",
  },
  {
    name: "重度污染",
    color: "purple",
    range: "201-300",
    description:
      "心脏病和肺病患者症状显著加剧，运动耐受力降低，健康人群普遍出现症状。",
  },
  {
    name: "严重污染",
    color: "brown",
    range: "300+",
    description:
      "健康人群运动耐受力降低，有明显强烈症状，提前采取措施保护健康。",
  },
];


const colorClass = (color: string) => {
  return {
    color: color,
  };
};
const levelInfo = computed(() => {
  for (const level of levels) {
    if (level.name === category_.value) {
      return level;
    }
  }
  return null; // 如果未找到匹配的等级，返回 null 或者其他适当的值
});

// echarts
import * as echarts from "echarts";
watch(() => props.city, () => Promise.all([getPresentCityAqi()]).then(() => {
  renderChart(
    // realTimeWeatherList.value,
  );
}));
// 初始化 ECharts 实例
let chartInstance_history: echarts.ECharts | null = null;
const renderChart = async (
  // tempData: RealTimeWeather[]
) => {
  if (!chartInstance_history) {
    const chartDom_history = document.getElementById("chart_brief_aqi_bar");
    chartInstance_history = echarts.init(chartDom_history);
  }
  chartInstance_history.setOption({
    series: [
      {
        type: 'gauge',
        startAngle: -120,
        endAngle: -60,
        center: ['50%', '50%'],
        radius: '80%',
        min: 0,
        max: 350,
        splitNumber: 7,
        axisLine: {
          lineStyle: {
            width: 17,
            color: [
              [1 / 7, 'green'],
              [2 / 7, 'yellow'],
              [3 / 7, 'orange'],
              [4 / 7, 'red'],
              [6 / 7, 'purple'],
              [1, 'brown']
            ]
            // color: [
            //   [0.125, 'green'],
            //   [0.25, 'yellow'],
            //   [0.375, 'orange'],
            //   [0.5, 'red'],
            //   [0.75, 'purple'],
            //   [1, 'brown']
            // ]
          }
        },
        pointer: {
          icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
          length: '60%',
          width: 7,
          offsetCenter: [0, '-0%'],
          itemStyle: {
            color: 'gray',
          }
        },
        axisTick: {
          length: 1,
          lineStyle: {
            color: 'auto',
            width: 1
          }
        },
        splitLine: {
          length: 3,
          lineStyle: {
            color: 'auto',
            width: 4
          }
        },
        axisLabel: {
          color: '#464646',
          fontSize: 17,
          distance: -45,
          // rotate: 'tangential',
          formatter: function (value) {
            if (value === 0) {
              return '0';
            } else if (value === 350) {
              return '350';
            }

            // if (value === 25) {
            //   return '优';
            // } else if (value === 75) {
            //   return '良';
            // } else if (value === 125) {
            //   return '轻度污染';
            // } else if (value === 175) {
            //   return '中度污染';
            // } else if (value === 250) {
            //   return '重度污染';
            // } else if (value === 350) {
            //   return '严重污染';
            // } 
            return '';
          }
        },
        title: {
          offsetCenter: [0, '-10%'],
          fontSize: 20
        },
        detail: {
          fontSize: 30,
          offsetCenter: [0, '-25%'],
          valueAnimation: true,
          formatter: function (value: number) {
            return Math.round(value) + '';
          },
          // color: 'inherit'
          color: 'black'
        },
        data: [
          {
            value: aqi_.value,
            name: ''
          }
        ]
      }
    ]
  });
};

// onMounted(() => {
//   getPresentCityAqi();
// });
onMounted(() => Promise.all([getPresentCityAqi()]).then(() => {
  setTimeout(() => {
    renderChart(
      // realTimeWeatherList.value
    );
  }, 1000);
  // renderChart(
  //   realTimeWeatherList.value
  // );
  window.addEventListener("click", () => {
    if (chartInstance_history) {
      renderChart(
        // realTimeWeatherList.value
      );
      chartInstance_history.resize();
    }
  });
  window.addEventListener("resize", () => {
    if (chartInstance_history) {
      renderChart(
        // realTimeWeatherList.value
      );
      chartInstance_history.resize();
    }
  });
}));


// option = {
//   series: [
//     {
//       type: 'gauge',
//       startAngle: -150,
//       endAngle: -30,
//       center: ['50%', '75%'],
//       radius: '90%',
//       min: 0,
//       max: 400,
//       splitNumber: 16,
//       axisLine: {
//         lineStyle: {
//           width: 30,
//           color: [
//             [0.125, 'green'],
//             [0.25, 'yellow'],
//             [0.375, 'orange'],
//             [0.5, 'red'],
//             [0.75, 'purple'],
//             [1, 'brown']          
//           ]
//         }
//       },
//       pointer: {
//         icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
//         length: '60%',
//         width: 20,
//         offsetCenter: [0, '-0%'],
//         itemStyle: {
//           color: 'auto',
//         }
//       },
//       axisTick: {
//         length: 3,
//         lineStyle: {
//           color: 'auto',
//           width: 2
//         }
//       },
//       splitLine: {
//         length: 10,
//         lineStyle: {
//           color: 'auto',
//           width: 5
//         }
//       },
//       axisLabel: {
//         color: '#464646',
//         fontSize: 20,
//         distance: -60,
//         rotate: 'tangential',
//          formatter: function (value) {
//           if (value === 25) {
//             return '优';
//           } else if (value === 75) {
//             return '良';
//           } else if (value === 125) {
//             return '轻度污染';
//           } else if (value === 175) {
//             return '中度污染';
//           } else if (value === 250) {
//             return '重度污染';
//           } else if (value === 350) {
//             return '严重污染';
//           } 
//           return '';
//         }
//       },
//       title: {
//         offsetCenter: [0, '-10%'],
//         fontSize: 20
//       },
//       detail: {
//         fontSize: 30,
//         offsetCenter: [0, '-35%'],
//         valueAnimation: true,
//         formatter: function (value: number) {
//           return Math.round(value) + '';
//         },
//         color: 'inherit'
//       },
//       data: [
//         {
//           value: 50,
//           name: ''
//         }
//       ]
//     }
//   ]
// };


</script>
<style>
.air-quality-indicator {
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.location {
  /* margin-bottom: 10px; */
}

.quality-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background-image: linear-gradient(to right,
      #0019d4,
      #4c72af,
      #07daff,
      #22ff6c,
      #51ff21f6);
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.quality-level {
  font-size: 40px;
  font-weight: bold;
  z-index: 1;
}

.quality-description {
  /* font-size: 30px; */
  font-size: 25px;
  font-weight: bold;
  z-index: 1;
}


.air-quality-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.air-quality-card {
  background-color: transparent;
  border: none;
  box-shadow: none;
  margin-bottom: 10px;
}
</style>
