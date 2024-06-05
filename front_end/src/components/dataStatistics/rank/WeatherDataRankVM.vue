<template>
  <div>
    <p class="text-2xl font-bold mb-4 text-center">中国城市气象质量排行</p>
    <el-row :gutter="2">
      <el-col :span="1"></el-col>
      <el-col :span="11">
        <el-select v-model="norm" placeholder="请选择气象质量" size="small">
          <el-option
            v-for="item in weather_norms"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-col>
      <el-col :span="1"></el-col>
      <el-col :span="11">
        <el-switch
          v-model="Match"
          style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
          active-text="最好"
          inactive-text="最差"
          :active-action-icon="View"
          :inactive-action-icon="Hide"
        />
      </el-col>
    </el-row>
    <div class="my-2">
      <div class="ranking-container bg-white my-4 p-2">
        <NormRankings :city_ranks="CityNormRankings" :norm="norm" />
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { View, Hide } from "@element-plus/icons-vue";
import { get } from "@/api/index.ts";
import { RankItem } from "@/types/weather";
import { weather_norms } from "@/stores/weather";
import NormRankings from "@c/dataStatistics/rank/NormRanking.vue";
onMounted(() => {
  getNormCityRankings();
});
const Match = ref(true);
const norm = ref("humid");
watch(Match, () => {
  getNormCityRankings();
});
watch(norm, () => {
  getNormCityRankings();
});
interface GetCityResponse {
  status: boolean;
  ranks: RankItem[];
}
const CityNormRankings = reactive<RankItem[]>([]);
const getNormCityRankings = async () => {
  get<GetCityResponse>("/api/weather/rank/", {
    norm: norm.value,
    order_type: Match.value,
  }).then((res) => {
    CityNormRankings.splice(0, CityNormRankings.length, ...res.data.ranks);
  });
};
</script>
