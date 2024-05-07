<template>
  <div class="bg-white p-8 rounded-lg shadow-md border-2">
    <h1 class="text-3xl font-bold">空气质量指数等级标准</h1>
    <el-row>
      <el-col :span="8" v-for="(item, index) in levels" :key="index">
        <div class="level-item bg-${item.color}">
          <div class="level-name">{{ item.name }}</div>
          <div class="level-range">{{ item.range }}</div>
          <div class="level-description">{{ item.description }}</div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts" setup>
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
</script>

<style scoped></style>
