<template>
  <div class="block text-center" style="height: 220px">
    <span class="demonstration text-2xl">AI热力图</span>
    <el-carousel height="auto" autoplay :interval="graph_interval">
      <el-carousel-item
        v-for="item in demoPictures"
        :key="item"
        style="width: 300px; height: 200px"
        class="small justify-center"
      >
        <img :src="item" />
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script lang="ts" setup>
// import { get } from "@/api/index.ts";
// interface getAiGraphResponse {
//   status: string;
//   pictures: string[];
// }
// const pictures = ref<string[]>([]);
const graph_interval = ref(1000);
// onMounted(() => {
//   getPictures();
// });
const demoPictures = [
  "https://charles2530.github.io/image/background/background-dark1.jpg",
  "https://charles2530.github.io/image/background/background-light1.jpg",
];
// const getPictures = async () => {
//   try {
//     const res = await get<getAiGraphResponse>("/api/weather/ai_graph");
//     if (res.data.status) {
//       pictures.value = [...res.data.pictures, ...demoPictures];
//       await nextTick();
//       console.log(pictures.value);
//     } else {
//       ElMessage({
//         message: "获取失败",
//         type: "error",
//       });
//     }
//   } catch (error) {
//     ElMessage({
//       message: "接口请求失败",
//       type: "error",
//     });
//   }
// };
</script>

<style scoped>
.carousel-item {
  color: #475669;
  opacity: 0.75;
  margin: 0;
  text-align: center;
}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  display: flex;
  align-items: center;
  margin: 0;
  text-align: center;
  height: 100%;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
