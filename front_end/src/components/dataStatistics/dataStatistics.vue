<template>
  <div style="max-height: 700px; overflow: auto">
    <div class="mx-4 mb-4">
      <trendHistoryGraph />
    </div>
    <dataList></dataList>
  </div>
</template>
<script lang="ts" setup>
import dataList from "./dataList.vue";
import trendHistoryGraph from "./trendHistoryGraph.vue";
</script>
