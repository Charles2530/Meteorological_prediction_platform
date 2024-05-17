<template>
  <div class="air-quality-indicator">
    <div class="location text-2xl">{{ cityMessage.city }}</div>
    <div class="quality-circle">
      <div class="quality-level text-gray-200">{{ cityMessage.aqi }}</div>
    </div>

    <el-tooltip effect="light">
    <template #content>    
       <el-row>
        <el-col :span="24" class="rounded-lg shadow-md p-2" style="width: 40vh;">
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
          <!-- </div> -->
        </el-col>
      </el-row> 
    </template>
    <el-button class="quality-description text-slate-600 ml-2" style="margin-top: 10px;border: none;"> {{ cityMessage.category }}</el-button>
  </el-tooltip>


  <!-- 下方显示提示信息 -->
  <!-- <div @mouseover="showHover = true" @mouseout="showHover = false" class="quality-circle">
      <div class="quality-level text-gray-200">{{ cityMessage.aqi }}</div>
    </div> -->
    <!-- <div class="quality-description text-slate-600 ml-2">
      {{ cityMessage.category }}
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
import { CityWeatherData } from "@/types/weather";
onMounted(() => {
  getPresentCityAqi();
});
interface CityInfoResponse {
  status: boolean;
  message: CityWeatherData;
}
const cityMessage = reactive<CityWeatherData>({} as CityWeatherData);
const getPresentCityAqi = async () => {
  get<CityInfoResponse>("/api/getCityInfo/").then((res) => {
    cityMessage.aqi = res.data.message.aqi;
    cityMessage.city = res.data.message.city;
    cityMessage.category = res.data.message.category;
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
    color: "blue",
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
    if (level.name === cityMessage.category) {
      return level;
    }
  }
  return null; // 如果未找到匹配的等级，返回 null 或者其他适当的值
});

</script>
<style>
.air-quality-indicator {
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.location {
  margin-bottom: 10px;
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
  font-size: 30px;
  font-weight: bold;
  z-index: 1;
}
</style>
