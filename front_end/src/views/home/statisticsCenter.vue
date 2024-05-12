<template>
  <div style="max-height: fit-content; overflow: auto">
    <el-container>
      <el-main>
        <el-card>
          <el-row :gutter="20">
            <el-col :span="18">
              <el-card>
                <el-select
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
                </el-select>
                <trendHistoryGraph :city="selectedLocation" />
              </el-card>
              <el-card>
                <el-row :gutter="2">
                  <el-col :span="12">
                    <el-card>
                      <trendHistoryTempGraph :city="selectedLocation" />
                    </el-card>
                  </el-col>
                  <el-col :span="12">
                    <el-card>
                      <trendHistoryAqiGraph :city="selectedLocation" />
                    </el-card>
                  </el-col>
                </el-row>
                <el-row :gutter="2">
                  <el-col :span="12">
                    <el-card>
                      <trendHistoryWinSpeedGraph :city="selectedLocation" />
                    </el-card>
                  </el-col>
                  <el-col :span="12">
                    <el-card>
                      <trendHistoryPrecipGraph :city="selectedLocation" />
                    </el-card>
                  </el-col>
                </el-row>
                <el-row :gutter="2">
                  <el-col :span="12">
                    <el-card>
                      <trendHIstoryPressureGraph :city="selectedLocation" />
                    </el-card>
                  </el-col>
                  <el-col :span="12">
                    <el-card>
                      <trendHistoryHumidGraph :city="selectedLocation" />
                    </el-card>
                  </el-col>
                </el-row>
              </el-card>
            </el-col>
            <el-col :span="6"> </el-col>
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
import { china_cities } from "@/stores/cities";
const selectedLocation = ref("");
const locations = china_cities;
</script>
