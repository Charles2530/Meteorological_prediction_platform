<template>
  <div class="block text-center" style="height: 220px">
    <span class="demonstration text-2xl">AI热力图</span>
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

const videoSrc = videoPath;
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
