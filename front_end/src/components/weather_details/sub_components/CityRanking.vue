<template>
  <div class="common-layout rounded-lg" style="background-color: white;">
    <!-- <el-card style="width: 100%;"> -->
      <div class="text-2xl" style="margin-bottom: 20px;"><el-icon ><Histogram /></el-icon>&nbsp;&nbsp;实况排行</div>
      <hr />
      <el-tabs stretch v-model="activeName" class=" " @tab-click="handleClick">
        <el-tab-pane label="最高气温" name="first">
          <el-table :data="highestTempRankings" style="width: 100%">
            <el-table-column prop="no" label="排名" height="auto" width="70"/>
            <el-table-column prop="city" label="城市" />
            <el-table-column prop="province" label="所在省份" />
            <el-table-column prop="item" label="最高气温" />
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="最低气温" name="second">
          <el-table :data="lowestTempRankings" style="width: 100%">
            <el-table-column prop="no" label="排名" height="auto" width="70"/>
            <el-table-column prop="city" label="城市" />
            <el-table-column prop="province" label="所在省份" />
            <el-table-column prop="item" label="最低气温" />
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="24小时降水量" name="third">
          <el-table :data="precipRankings" style="width: 100%">
            <el-table-column prop="no" label="排名" height="auto"  width="70"/>
            <el-table-column prop="city" label="城市" />
            <el-table-column prop="province" label="所在省份" />
            <el-table-column prop="item" label="24小时降水量" />
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="空气质量" name="fourth">
          <el-table :data="cityAqiRankings" style="width: 100%">
            <el-table-column prop="no" label="排名" height="auto" width="70"/>
            <el-table-column prop="city" label="城市" />
            <el-table-column prop="province" label="所在省份" />
            <!-- <el-table-column prop="item" label="空气质量" /> -->
            <el-table-column prop="item" label="空气质量">
              <template #header>
                <el-row>
                  <!-- <el-col :span="12"> -->
                  空气质量&nbsp;
                  <!-- </el-col> -->
                  <!-- <span></span> -->
                  <!-- <el-col :span="12"> -->
                  <el-button size="small" type="" :icon="cityAqiIcon" @click="changeAqiOrder()" style="padding: 5px;" />
                  <!-- </el-col> -->
                </el-row>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    <!-- </el-card> -->
  </div>
</template>


<!-- <template>
  <div>
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
</template> -->
<script lang="ts" setup>
import { ref } from 'vue'
import type { RateInstance, TabsPaneContext } from 'element-plus'
import { CaretTop, CaretBottom,Histogram } from '@element-plus/icons-vue'


const activeName = ref('first')

const handleClick = (tab: TabsPaneContext, event: Event) => {
  // console.log(tab, event)
}


// 
const tableData = ref({})
// 

import { View, Hide } from "@element-plus/icons-vue";
import { get } from "@/api/index.ts";
import QualityRanking from "./QualityRanking.vue";
onMounted(() => {
  getCityRankings();
  cityAqiRankings.value = bestCityAqiRankings;

});
interface CityRankItem {
  city: string;
  province: string;
  item: string;
  no: number;
}
interface GetCityResponse {
  status: boolean;
  city_list_max_temp: CityRankItem[];
  city_list_min_temp: CityRankItem[];
  city_list_precip: CityRankItem[];
  city_list_best_aqi: CityRankItem[];
  city_list_worst_aqi: CityRankItem[];
}

const highestTempRankings = reactive<CityRankItem[]>([]);
const lowestTempRankings = reactive<CityRankItem[]>([]);
const precipRankings = reactive<CityRankItem[]>([]);
const bestCityAqiRankings = reactive<CityRankItem[]>([]);
const worstCityAqiRankings = reactive<CityRankItem[]>([]);
const showBestAqi = ref(true);
const cityAqiRankings = computed(() => {
  return showBestAqi.value ? bestCityAqiRankings : worstCityAqiRankings;
});
const cityAqiIcon = computed(() => {
  return showBestAqi.value ? 'CaretTop' : 'CaretBottom';
});
// const cityAqiButton = computed(() => {
//   return showBestAqi.value ? '最好' : '最差';
// });
const getCityRankings = async () => {
  get<GetCityResponse>("/api/weather/city_rank/").then((res) => {
    bestCityAqiRankings.splice(
      0,
      bestCityAqiRankings.length,
      ...res.data.city_list_best_aqi
    );
    worstCityAqiRankings.splice(
      0,
      worstCityAqiRankings.length,
      ...res.data.city_list_worst_aqi
    );
    highestTempRankings.splice(
      0,
      highestTempRankings.length,
      ...res.data.city_list_max_temp
    );
    lowestTempRankings.splice(
      0,
      lowestTempRankings.length,
      ...res.data.city_list_min_temp
    );
    precipRankings.splice(0, precipRankings.length, ...res.data.city_list_precip);
  });
};

const changeAqiOrder = () => {
  showBestAqi.value = !showBestAqi.value;
}

bestCityAqiRankings

// 排行榜部分
const Match = ref(true);
</script>
