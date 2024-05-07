<template>
  <div class="seller-info bg-white p-8 rounded-lg shadow-md border-2">
    <div class="rank-display">
      <p class="rank-text" :class="rankClass">
        <el-icon class="mr-2"><Position /></el-icon>
        {{ rank }}
      </p>
    </div>
    <div>
      <el-row>
        <el-col :span="24" class="info-section">
          <el-row :gutter="2">
            <el-col :span="6">
              <p class="city text-xl text-center text-blue-300">
                {{ props.city.city }}
              </p>
            </el-col>
            <el-col :span="6">
              <p class="aqi text-xl text-center">AQI: {{ props.city.aqi }}</p>
            </el-col>
            <el-col :span="12">
              <p class="category text-xl text-center text-green-700">
                空气质量:
                <el-tag :type="rankType" class="mx-2">{{
                  props.city.category
                }}</el-tag>
              </p>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { AqiRankItem } from "@/types/weather";
const props = defineProps<{
  city: AqiRankItem;
  rank: number;
}>();
const rankClass = computed(() => {
  switch (props.rank) {
    case 1:
      return "rank-first";
    case 2:
      return "rank-second";
    case 3:
      return "rank-third";
    default:
      return "rank-other";
  }
});
const rankType = computed(() => {
  switch (props.city.category) {
    case "优":
      return "success";
    case "良":
      return "primary";
    case "轻度污染":
      return "warning";
    default:
      return "danger";
  }
});
</script>

<style scoped>
.seller-info {
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.rank-display {
  flex-basis: 10%;
  text-align: center;
}

.rank-text {
  font-size: 32px;
  font-weight: bold;
}

.rank-first {
  color: #ef4806;
}

.rank-second {
  color: #f5a623;
}

.rank-third {
  color: #f8e71c;
}

.rank-other {
  color: #555;
}
</style>
