<template>
  <el-row>
      <el-col :span="17">
        <div style="height: 100%;">
          <MapContainer ref="refMap" />
        </div>
      </el-col>
      <el-col :span="7">
        <div class="infoDiv" style="height: 100% !important; margin-right: 15px">
          <el-row>
            <el-col :span="24">
              <span style="float:left;font-weight:530;font-size:16px;color:white;margin-top: 10px;"> &nbsp;&nbsp;&nbsp;&nbsp;{{refMap?.dis_info.districtName}}</span>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <InfoColumn/>
            </el-col>
          </el-row>
        </div>
      </el-col>
  </el-row>
</template>


<script setup lang="ts">
import MapContainer, { API as MapContainerAPI } from "@c/map/MapContainer.vue";
const refMap = ref<MapContainerAPI | null>(null);

// const Map = defineAsyncComponent(() => import("@c/map/MapContainer.vue"));
const InfoColumn = defineAsyncComponent(() => import("@c/map/InfoColumn.vue"));

// const activeNames = ref(['1'])
// const handleChange = () => {
  
// }
</script>

<style scoped>
.infoDiv  {
  background:linear-gradient(to right top, rgba(26, 79, 158, 0.95),rgb(243, 179, 179, 0.95)) !important;
 /* background:radial-gradient(circle at center, #ff9966, #ff5e62); */
    /* background:radial-gradient(circle at center, #c848b9, #f962a7, #fd836e,#eda7a7); */
    /* background:linear-gradient(to right top,rgb(221,228,251),rgb(253,230,204)); */
    /* background:linear-gradient(to right top, rgb(221,228,251),rgb(237,167,167,0.5)); */
    /* background:linear-gradient(to right top, rgba(26, 79, 158, 0.6),rgb(243, 179, 179, 0.5)) !important; */
  
}

:deep(.el-collapse-item__header) {
  color: black;
  background:linear-gradient(to right top, rgba(139, 132, 219, 0.5),rgb(243, 179, 179,0.7));
  height: 35px;
  line-height: 90px;
  padding: 10px 0;
}

:deep(.el-collapse-item__content) {
  color: black;
  background:linear-gradient(to right top, rgba(26, 79, 158, 0.6),rgb(243, 179, 179, 0.5)) !important;
 /* background:radial-gradient(circle at center, #ff9966, #ff5e62); */
    /* background:radial-gradient(circle at center, #c848b9, #f962a7, #fd836e,#eda7a7); */
    /* background:linear-gradient(to right top,rgb(221,228,251),rgb(253,230,204)); */
    /* background:linear-gradient(to right top, rgb(221,228,251),rgb(237,167,167,0.5)); */
    /* background:linear-gradient(to right top, rgba(26, 79, 158, 0.6),rgb(243, 179, 179, 0.5)) !important; */
  
}


</style>


