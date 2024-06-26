<template>
  <div
    class="info_container"
    style="min-height: 85vh; max-height: 85vh; overflow: auto"
  >
    <el-card class="color2" shadow="always">
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="grid-content">
            <span style="font-size: 12px">{{ proInfo.weather.time }}更新</span>
          </div>
        </el-col>
        <el-col :offset="0" :span="12">
          <div class="grid-content">
            <span
              class="font1"
              style="
                border: 1px solid #ffffff;
                border-radius: 10px;
                float: right !important;
              "
              >&nbsp;&nbsp;AQI：{{ proInfo.weather.airAQI }}
              {{ proInfo.weather.air }}&nbsp;&nbsp;</span
            >
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="20" style="height: 80px">
        <el-col :offset="3" :span="6">
          <div class="grid-content">
            <img
              :src="getAssetsFileIcon(proInfo.weather.icoid + '.png')"
              style="width: 60px; height: 60px"
            />
          </div>
        </el-col>
        <el-col :span="15">
          <div class="grid-content">
            <span style="font-size: 44px"
              >{{ proInfo.weather.tem }}℃&nbsp;</span
            >
            <span style="font-size: 22px">{{ proInfo.weather.condition }}</span>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="20" style="margin-bottom: 20px !important">
        <el-col :offset="1" :span="22">
          <div class="grid-content">
            <span
              class="font1"
              style="border: 1px solid #a5a5a5; border-radius: 10px"
              >&nbsp;&nbsp;天气提示&nbsp;&nbsp;</span
            >
            <span class="font1">&nbsp{{ proInfo.weather.infos }}</span>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :offset="1" :span="7">
          <div class="grid-content" style="text-align: center">
            <span class="font1">{{ proInfo.weather.wind }}级</span>
            <br />
            <span class="font1">{{ proInfo.weather.windDir }}</span>
          </div>
        </el-col>
        <el-col :offset="1" :span="7" style="text-align: center">
          <div class="grid-content">
            <span class="font1">{{ proInfo.weather.hum }}%</span>
            <br />
            <span class="font1">相对湿度</span>
          </div>
        </el-col>
        <el-col :offset="0" :span="7" style="text-align: center">
          <div class="grid-content">
            <span class="font1">{{ proInfo.weather.ray }}</span>
            <br />
            <span class="font1">紫外线</span>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-card class="color2">
      <el-row :gutter="10" style="margin-bottom: 0px !important">
        <el-col :offset="8" :span="8">
          <div class="grid-content">
            <span style="font-size: 16px">地理概况</span>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :offset="1" :span="22">
          <div class="grid-content">
            <span style="font-size: 13px">{{ proInfo.geography }}</span>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-card class="color2">
      <el-table
        :data="proInfo.hazardTable"
        size:mini
        max-height="240"
        style="font-size: 14px; font-weight: 500"
        :row-style="{ height: '40px' }"
      >
        <el-table-column
          prop="place"
          label="地点"
          width="140"
          :show-overflow-tooltip="true"
        />
        <el-table-column prop="level" label="等级" width="80">
          <template #default="scope">
            <span
              class="font1"
              style="border: 1px solid #a5a5a5; border-radius: 10px"
              >&nbsp;&nbsp;&nbsp;{{ scope.row.level }}&nbsp;&nbsp;&nbsp;</span
            >
          </template>
        </el-table-column>
        <el-table-column prop="type" label="灾害类型" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { getAssetsFileIcon } from "@/utils/pub-use";
import { get } from "@/api/index";
import { ProInfo } from "@/types/weather";
import { ref, watch } from "vue";

const proInfo = ref({
  weather: {
    icoid: "150",
    time: "2024-04-10 17:33", //时间
    tem: "18", //温度
    condition: "阴", //晴雨状况
    infos: "今晚多云。明天晴，比今天热很多，空气一般。", //详细天气状况
    wind: "2", //风力等级
    windDir: "无持续风向", //风向
    hum: "70", //相对湿度
    ray: "中等", //紫外线
    air: "污染严重", //空气质量状况
    airAQI: "91", //空气质量指数
    visibility: "9km", //能见度
    rainfall: "0.0mm", //降水量
    pressure: "1006hPa", //大气压
  },
  geography:
    "河南省地势西高东低、北坦南凹，北、西、南三面有太行山、伏牛山、桐柏山、大别山四大山脉呈半环形分布， 中部和东部为辽阔的黄淮海冲积平原，西南部为南阳盆地。境内有黄河、淮河、卫河、汉水四大水系。大地构造跨华北板块和扬子板块，地层发育齐全，土壤分布大致以秦岭—淮河一线为界。",
  hazardTable: [
    {
      place: "葫芦岛市，辽宁省",
      level: "蓝",
      type: "大风",
    },
    {
      place: "朝阳市，辽宁省",
      level: "蓝",
      type: "大风",
    },
    {
      place: "锦州市，辽宁省",
      level: "蓝",
      type: "大风",
    },
    {
      place: "松原市，辽宁省",
      level: "黄",
      type: "森林火险",
    },
  ],
});

const props = defineProps<{
  proName: string;
}>(); // 定义 props

const proName = ref("中国");

// 监听 propName 的变化
watch(
  () => props.proName,
  () => {
    proName.value = props.proName;
    getProInfo();
  }
);

onMounted(() => {
  getProInfo();
});

const getProInfo = async () => {
  console.log(proName.value);
  get<ProInfo>("/api/getProInfo/", { proName: proName.value }).then((res) => {
    proInfo.value = res.data;
  });
};
</script>

<style scoped>
* {
  color: white !important;
}

.el-row {
  margin-bottom: 15px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.font1 {
  font-size: 14px;
}

.color2 {
  /* background:radial-gradient(circle at center, #ff9966, #ff5e62); */
  background-color: rgb(255, 255, 255, 0);
  width: 90%;
  margin: auto;
  margin-top: 2%;
  border-color: rgb(187, 168, 217, 0.7);
}

:deep(.el-table) {
  background-color: rgba(232, 232, 232, 0.03);
  --el-table-row-hover-bg-color: rgba(232, 232, 232, 0.1);
}

:deep(.el-table tr) {
  background-color: rgba(232, 232, 232, 0.03);
}

:deep(.el-table th.el-table__cell) {
  background-color: rgba(232, 232, 232, 0.03);
  color: rgb(219, 219, 219);
}

.info_container::-webkit-scrollbar {
  width: 10px;
  height: 8px;
}

::-webkit-scrollbar-button {
  display: none;
}

::-webkit-scrollbar-track {
  background-color: rgba(70, 166, 255, 0.1);
  display: none;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(105, 105, 105, 0.4);
  border: 2px solid transparent;
  border-radius: 6px;
  background-clip: padding-box;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.5);
}
</style>
