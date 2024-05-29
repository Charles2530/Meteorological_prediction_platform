<template>
  <div style="height: 100%;">
    <MapContainer  @getValue="getSonValue" />
  </div>
  <!-- <el-row>
      <el-col :span="17">
        <div style="height: 100%;">
          <MapContainer  @getValue="getSonValue" />
        </div>
      </el-col>
      <el-col :span="7">
        <div class="infoDiv" style="height: 100% !important; margin-right: 15px">
          <el-row>
            <el-col :span="24">
              <span style="float:left;font-weight:530;font-size:16px;color:white;margin-top: 10px;"> &nbsp;&nbsp;&nbsp;&nbsp;{{sonProName}}</span>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <InfoColumn :proName="sonProName"/>
            </el-col>
          </el-row>
        </div>
      </el-col>
  </el-row> -->
</template>


<script setup lang="ts">
import MapContainer from "@c/map/MapContainer.vue";
// const refMap = ref<MapContainerAPI | null>(null);

// const Map = defineAsyncComponent(() => import("@c/map/MapContainer.vue"));
// const InfoColumn = defineAsyncComponent(() => import("@c/map/InfoColumn.vue"));
const sonProName = ref<string>("中国");
const getSonValue = (value: string) => {
  sonProName.value = value;
}

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
</style>


