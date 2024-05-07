<template>
  <el-tabs  v-model="activeName" class="demo-tabs mx-40 rounded-2xl " @tab-click="handleClick" type="border-card">
    <el-tab-pane label="天气速览" name="first">
      <overview />
    </el-tab-pane>
    <el-tab-pane label="30日天气" name="second">
      <calendar30 />
    </el-tab-pane>
    <el-tab-pane label="空气质量" name="third">
      <aqi />
    </el-tab-pane>
    <el-tab-pane label="数据统计" name="fourth">

      <div class="chart">
        <div id="chart_one" style="
        height: 300px;
        width: 300px;
        padding: 10px;
        margin: 0 auto;
        /* align-items: center;
        justify-content: center; */
      "></div>
      </div>

    </el-tab-pane>
  </el-tabs>
</template>
<script lang="ts" setup>



import { ref, onMounted } from 'vue';
import type { TabsPaneContext } from 'element-plus';
import * as echarts from 'echarts';
/*抽屉页*/
const activeName = ref('first')
const handleClick = (tab: TabsPaneContext, event: Event) => {
  console.log(tab, event)
}
type ECharts = echarts.ECharts
let echartsInstance: Ref<ECharts | null> = ref(null)


/** 组件  **/
import overview from '@/components/weather_details/overview.vue'
import calendar30 from '@/components/weather_details/calendar30.vue'
import aqi from '@/components/weather_details/aqi.vue'
import statistics from '@/components/weather_details/statistics.vue'
const stateNavigator = ref(0) // 用于判断是否加载loading
const cityList = ref([])
const city = ref({})
let weather = ref({})
const air = ref({})
const forecast = ref([])
const preDayWeather = ref([])
const ultraviolet = ref([])
const searchShow = ref(false)


interface WeatherHisOverview {
  weather: {
    icon: number;
    temp: string;
    text: string;
  },
  city: {
    adm2: string;
    name: string;
  },
  searchShow: boolean
}





import { post, get } from "@/api/index.ts";
const get_his_overview = async () => {
  get<WeatherHisOverview>("/api/his/overview").then((res) => {
    weather.value = res.data.weather;
    city.value = res.data.city;
    searchShow.value = res.data.searchShow
  });
};

const getData = () => {
  get_his_overview();
  get
}
/*echart*/
onMounted(() => {
  // 解决echarts图表放大溢出父容器
  // 页面上的元素进行监测和调整大小操作，当被监测的元素的大小发生变化时调用
  // setTimeout(() => {
  //   const resizeOb = new ResizeObserver((entries) => {
  //     for (const entry of entries) {
  //       echarts.getInstanceByDom(entry.target).resize()
  //     }
  //   })
  //   resizeOb.observe(document.getElementById('chart_one'))
  // })
  // 通过id获取echarts元素初始化图表的容器：创建一个 echarts 实例，调用 methods 里的 initChart 进行图表初始化
  // 获取id为chart_one的dom元素给chartDom容器，init初始化一个echarts实例给myChart，需以dom元素为参数
  let chartDom = document.getElementById('chart_one')
  // console.log(chartDom)
  echartsInstance.value = echarts.init(chartDom)
  nextTick(() => {
    initChart()
  })

  // 接口获取数据后，再为echarts赋值
  // 在 ECharts 的 X 轴上显示当前日期前一周的月日
  initData()
  setTimeout(() => {
    initChart()
  }, 2000)

});
watch(echartsInstance, () => {
  console.log(echartsInstance.value)
})


function initData() {
  // 模拟数据初始化
}
// function initChart() {}
function initChart() {

  const today = new Date();
  const lastWeek = new Date(
    today.getFullYear(),
    today.getMonth(),
    today.getDate() - 6
  );
  const xAxisData = [];
  for (let i = lastWeek.getTime(); i <= today.getTime(); i += 86400000) {
    const date = new Date(i);
    xAxisData.push(
      date.toLocaleDateString('en-US', {
        month: 'numeric',
        day: 'numeric',
      })
    );
  }
  console.log(xAxisData.join(", "));

  let option = {
    grid: {
      left: '3%',
      right: '4%',
      bottom: '4%',
      top: '11%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: xAxisData,
      axisLabel: {
        formatter: '{value}',
      },
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: '{value} m³',
      },
    },
    tooltip: {
      trigger: 'axis',
      formatter: '用气日期：{b}<br />日用气量：{c}',
      backgroundColor: 'rgba(255, 255, 255, 0.8)',
      axisPointer: {
        type: 'shadow',
      },
    },
    series: [
      {
        data: [120, 200, 150, 80, 70, 110, 130],
        type: 'bar',
        showBackground: true,
        backgroundStyle: {
          color: 'rgba(180, 180, 180, 0.2)',
        },
        label: {
          normal: {
            show: true,
            position: 'top',
          },
        },
      },
    ],
  };

  console.log(option)

  // 根据 option 的值来设置 myChart 的选项
  option && echartsInstance.value.setOption(option)
}



//----------
import type { CalendarDateType, CalendarInstance } from 'element-plus'

const calendar = ref<CalendarInstance>()
const selectDate = (val: CalendarDateType) => {
  if (!calendar.value) return
  calendar.value.selectDate(val)
}


// export default {
//     mounted () {
//         // 组件挂载时，进行默认数据的初始化
//         axios.defaults.baseURL = '/myApi'
//         requestData()
//     },
//     data() {
//         return {
//             city:"上海",
//             weatherData:{},
//             todayData:{},
//             plc:"暂无数据",
//             realtime:{},
//             futureData:[]
//         }
//     },
//     watch: {
//         // 当用户输入的城市发生变化后，调用接口进行数据请求
//         city() {
//             requestData()
//         }
//     },
//     methods: {
//         requestData() {
//             let city = encodeURI(city)
//             let api = `/simpleWeather/query?city=${city}&key=cffe158caf3fe63aa2959767a503bbfe`
//             axios.get(api).then((response: { data: any; })=>{
//                 weatherData = response.data
//                 todayData = weatherData.result.future[0]
//                 realtime = weatherData.result.realtime
//                 futureData = weatherData.result.future
//                 console.log(response.data)
//             })
//         }
//     }
// }




</script>
<style>
.chart {
  width: 95%;
  height: 92%;
  background: linear-gradient(to bottom, #ffffff, #ffffff);
  margin: 0 auto;
  /* display: flex; */
  /* justify-content: center; */
}

h2 {
  text-align: center;
  margin: 0;
  font-size: 18px;
  color: #000;
}

/*  */


.demo-tabs>.el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

/* demo */
.container {
  background: linear-gradient(rgb(13, 104, 188), rgb(54, 131, 195));
}

.input {
  width: 300px;
  margin-top: 20px;
}

.today {
  font-size: 20px;
  color: white;
}

.temp {
  font-size: 79px;
  color: white;
}

.realInfo {
  color: white;
}

.future {
  margin-top: 40px;
}

.header {
  color: white;
  font-size: 27px;
}
</style>
