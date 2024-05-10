<template>
  <div class="seller-info bg-white rounded-lg shadow-md border-2 mt-2">
    <div>
      <el-row>
        <el-col :span="24" class="info-section">
          <el-row :gutter="2">
            <el-col :span="4">
              <p :class="rankClass">
                <el-icon class="mr-2" size="large"><Position /> </el-icon>
                <span class="text-base font-bold">
                  {{ rank }}
                </span>
              </p>
            </el-col>
            <el-col :span="12">
              <p class="city text-lg text-center text-blue-300">
                {{ props.city.city }}
              </p>
            </el-col>
            <el-col :span="8">
              <p class="text-center">
                <el-tag :type="rankType" class="mx-2 text-lg" size="large"
                  >{{ props.city.level }} {{ props.city.norm }}</el-tag
                >
              </p>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { RankItem } from "@/types/weather";
const props = defineProps<{
  city: RankItem;
  rank: number;
}>();
const rankClass = computed(() => {
  switch (props.rank) {
    case 1:
      return "rank-first text-center";
    case 2:
      return "rank-second text-center";
    case 3:
      return "rank-third text-center";
    default:
      return "rank-other text-center";
  }
});
const rankType = computed(() => {
  switch (props.city.level) {
    case "优":
      return "success";
    case "良":
      return "primary";
    case "较差":
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
