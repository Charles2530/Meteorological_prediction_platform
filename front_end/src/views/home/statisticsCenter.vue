<template>
  <div style="max-height: fit-content; overflow: auto">
    <el-container>
      <el-main>
        <el-card>
          <el-row :gutter="20">
            <el-col :span="18">
              <el-card>
                <trendHistoryGraph />
              </el-card>
              <el-card>
                <dataList></dataList>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card> <WeatherDataRankVM /> </el-card>
            </el-col>
          </el-row>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>
<script lang="ts" setup>
import dataList from "@c/dataStatistics/dataList.vue";
import trendHistoryGraph from "@c/dataStatistics/trendHistoryGraph.vue";
import WeatherDataRankVM from "@/components/dataStatistics/WeatherDataRankVM.vue";
</script>
