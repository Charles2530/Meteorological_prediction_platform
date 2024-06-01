<template>
  <div style="max-height: fit-content; overflow: auto">
    <el-container>
      <el-main>
        <el-card>
          <el-row :gutter="20">
            <el-col :span="18">
              <el-card>
                <!-- <el-select
                  v-model="selectedLocation"
                  placeholder="请选择城市"
                  clearable
                >
                  <el-option
                    v-for="location in locations"
                    :key="location.value"
                    :label="location.label"
                    :value="location.value"
                  ></el-option>
                </el-select> -->
                <el-autocomplete
                  v-model="selectedLocation"
                  placeholder="请选择城市"
                  :fetch-suggestions="querySearch"
                  clearable
                  class="inline-input w-50"
                  highlight-first-item
                  :value-key="'label'"
                />
                <div class="slider-demo-block">
                  <span class="demonstration">时间维度</span>
                  <el-slider v-model="periods" />
                </div>

                <trendHistoryGraph
                  :city="selectedLocation"
                  :periods="periods"
                />
              </el-card>
              <el-card>
                <el-row :gutter="2">
                  <el-col :span="12">
                    <el-card>
                      <trendHistoryTempGraph
                        :city="selectedLocation"
                        :periods="periods"
                      />
                    </el-card>
                  </el-col>
                  <!-- </el-row>
                <el-row :gutter="2"> -->
                  <el-col :span="12">
                    <el-card>
                      <trendHistoryAqiGraph
                        :city="selectedLocation"
                        :periods="periods"
                      />
                    </el-card>
                  </el-col>
                </el-row>
                <el-row :gutter="2">
                  <el-col :span="12">
                    <el-card class="mt-3">
                      <trendHistoryHumidGraph
                        :city="selectedLocation"
                        :periods="periods"
                      />
                    </el-card>
                  </el-col>
                  <el-col :span="12">
                    <el-card class="mt-3">
                      <trendHistoryPrecipGraph
                        :city="selectedLocation"
                        :periods="periods"
                      />
                    </el-card>
                  </el-col>
                </el-row>
                <!-- <el-row :gutter="2">
                  <el-col :span="12">
                    <el-card>
                      <trendHIstoryPressureGraph :city="selectedLocation" :periods="periods"/>
                    </el-card>
                  </el-col>
                  <el-col :span="12">
                    <el-card>
                      <trendHistoryWinSpeedGraph :city="selectedLocation" :periods="periods"/>
                    </el-card>
                  </el-col>
                </el-row> -->
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card>
                <compareGraph />
              </el-card>
              <el-card>
                <aiTemperGraph />
              </el-card>
              <el-card class="mt-2">
                <WeatherDataRankVM />
              </el-card>
            </el-col>
          </el-row>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>
<script lang="ts" setup>
import trendHistoryTempGraph from "@/components/dataStatistics/graph/trendHistoryTempGraph.vue";
import trendHistoryGraph from "@c/dataStatistics/trendHistoryGraph.vue";
import trendHistoryAqiGraph from "@/components/dataStatistics/graph/trendHistoryAqiGraph.vue";
import trendHIstoryPressureGraph from "@/components/dataStatistics/graph/trendHIstoryPressureGraph.vue";
import trendHistoryHumidGraph from "@/components/dataStatistics/graph/trendHistoryHumidGraph.vue";
import trendHistoryWinSpeedGraph from "@/components/dataStatistics/graph/trendHistoryWinSpeedGraph.vue";
import trendHistoryPrecipGraph from "@/components/dataStatistics/graph/trendHistoryPrecipGraph.vue";
import compareGraph from "@/components/dataStatistics/compareGraph.vue";
import WeatherDataRankVM from "@c/dataStatistics/rank/WeatherDataRankVM.vue";
import { china_cities } from "@/stores/cities";
import aiTemperGraph from "@c/dataStatistics/graph/aiTemperGraph.vue";
const city = ref("");
const selectedLocation = ref("北京市");
const periods = ref(30);
const locations = china_cities;
interface LabelItem {
  label: string;
  value: string;
}
const labels = ref<LabelItem[]>([]);
const querySearch = (queryString: string, cb: any) => {
  const results = queryString
    ? labels.value.filter(createFilter(queryString))
    : labels.value;
  cb(results);
};
const handleSelect = (item: LabelItem) => {
  selectedLocation.value = item.label;
  city.value = item.value;
};
const loadAll = () => {
  return china_cities;
};
const createFilter = (queryString: string) => {
  return (restaurant: LabelItem) => {
    return (
      restaurant.label.toLowerCase().indexOf(queryString.toLowerCase()) === 0
    );
  };
};
onMounted(() => {
  labels.value = loadAll();
});
</script>

<style scoped>
.slider-demo-block {
  /* max-width: 600px; */
  display: flex;
  align-items: center;
}
/* .slider-demo-block .el-slider {
  margin-top: 0;
  margin-left: 12px;
} */
.demonstration {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  line-height: 44px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 0;
  margin-left: 20px;
}
.slider-demo-block .demonstration + .el-slider {
  flex: 0 0 90%;
}
</style>
