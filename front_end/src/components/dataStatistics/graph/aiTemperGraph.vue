<template>
  <div class="block text-center" style="height: 270px">
    <span class="demonstration text-2xl">AI热力图</span>
    <el-select v-model="videoSrc" placeholder="请选择">
      <el-option
        label="温度"
        :value="TemperaturePath"
        value-key="temperature"
      ></el-option>
      <el-option
        label="湿度"
        :value="HumidityPath"
        value-key="humidity"
      ></el-option>
      <el-option
        label="气压"
        :value="PressurePath"
        value-key="pressure"
      ></el-option>
    </el-select>
    <div>
      <video
        ref="videoPlayer"
        :src="videoSrc"
        controls
        @ended="onVideoEnded"
        autoplay
      ></video>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import videoPath from "@/assets/media/weather_forecast.mp4";
import HumidityPath from "@/assets/media/humidity.mp4";
import TemperaturePath from "@/assets/media/temperature.mp4";
import PressurePath from "@/assets/media/windSpeed.mp4";

const videoSrc = ref(TemperaturePath);
const videoPlayer = ref<HTMLVideoElement | null>(null);
const isPlaying = ref(false);

const onVideoEnded = () => {
  if (videoPlayer.value) {
    videoPlayer.value.currentTime = 0;
    videoPlayer.value.play().catch((error) => {
      console.error("Error attempting to play", error);
    });
  }
};

onMounted(() => {
  if (videoPlayer.value) {
    videoPlayer.value
      .play()
      .then(() => {
        isPlaying.value = true;
      })
      .catch((error) => {
        console.error("Error attempting to play", error);
      });
  }
});
</script>

<style scoped>
video {
  width: 100%;
  height: auto;
}

button {
  margin-top: 10px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
