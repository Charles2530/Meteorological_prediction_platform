<template>
  <div style="position: absolute; z-index: 1; height: 100%; width: 93%;">
    <MapContainer ref="refMap" />
  </div>
  <div class="demo-collapse"  style="position: absolute; z-index: 2;  width: 25%; right: 1%">
    <el-collapse v-model="activeNames" @change="handleChange">
      <el-collapse-item name="1">
        <template #title>
			      <span style="float:left;font-weight:bold;font-size:14px;color:#2C8DF4;"> {{refMap?.dis_info.districtName}}</span>
		    </template>
        <InfoColumn/>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>


<script setup lang="ts">
import MapContainer, { API as MapContainerAPI } from "@c/map/MapContainer.vue";
const refMap = ref<MapContainerAPI | null>(null);

// const Map = defineAsyncComponent(() => import("@c/map/MapContainer.vue"));
const InfoColumn = defineAsyncComponent(() => import("@c/map/InfoColumn.vue"));
const activeNames = ref([])
const handleChange = () => {
  
}
</script>

<style scoped>
:deep(.el-collapse-item__header) {
  color: black;
  background-color: white !important;
  height: 35px;
  line-height: 90px;
  padding: 10px 0;
}

:deep(.el-collapse-item__content) {
  color: black;
  background-color: white !important;
}


</style>


