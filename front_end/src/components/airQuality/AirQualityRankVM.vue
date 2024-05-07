<template>
  <div class="overflow-y-auto" style="max-height: 80vh">
    <p class="text-2xl font-bold mb-4 text-center">
      中国城市空气质量排行
      <el-switch
        class="mx-4 my-2"
        v-model="Match"
        style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
        active-text="最好"
        inactive-text="最差"
        :active-action-icon="View"
        :inactive-action-icon="Hide"
      />
    </p>
    <div class="my-2">
      <div v-if="Match" class="ranking-container bg-white my-4 p-2">
        <quality-ranking :city_aqi_ranks="bestCityAqiRankings" />
      </div>
      <div v-else class="ranking-container bg-white my-4 p-2">
        <quality-ranking :city_aqi_ranks="worstCityAqiRankings" />
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { View, Hide } from "@element-plus/icons-vue";
import { get } from "@/api/index.ts";
import { AqiRankItem } from "@/types/weather";
import QualityRanking from "./QualityRanking.vue";
onMounted(() => {
  getBestAqiCityRankings();
  getWorstAqiCityRankings();
});
interface GetCityResponse {
  status: boolean;
  ranks: AqiRankItem[];
}
const bestCityAqiRankings = reactive<AqiRankItem[]>([]);
const getBestAqiCityRankings = async () => {
  get<GetCityResponse>("/api/weather/aqi/rank_best").then((res) => {
    bestCityAqiRankings.splice(
      0,
      bestCityAqiRankings.length,
      ...res.data.ranks
    );
  });
};
const worstCityAqiRankings = reactive<AqiRankItem[]>([]);
const getWorstAqiCityRankings = async () => {
  get<GetCityResponse>("/api/weather/aqi/rank_worst").then((res) => {
    worstCityAqiRankings.splice(
      0,
      worstCityAqiRankings.length,
      ...res.data.ranks
    );
  });
};

// 排行榜部分
const Match = ref(true);
</script>
