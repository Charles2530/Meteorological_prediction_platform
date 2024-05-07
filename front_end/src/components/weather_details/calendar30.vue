import CurrentWeather from './sub_components/CurrentWeather.vue';
<template>
    <div class="common-layout mx-10">
        <el-container class="bg-blue-500">
            <el-main class="bg-pink-100">
                <el-calendar class=" rounded-lg  italic">
                    <template #date-cell="{ data }">
                        <p :class="data.isSelected ? 'is-selected' : ''">
                            {{ data.day.split('-')[2] }} <!-- 只显示日期部分 -->
                            <img class="weather-icon" src="@/assets/img/阴.png" alt="阴天">

                            <!-- <div  class="weather-icon">{{ " 18-20℃ " }}</div> -->
                            <span class="p-1 text-xl bg-blue-100 shadow-sm rounded-full">{{ "18-20℃" }}</span>
                        </p>
                    </template>
                </el-calendar>
            </el-main>
            <el-aside class="bg-yellow-50" width="20%">
                <CurrentWeather class="md:basis-3/5" :weather="weather" :city="city" :search="searchShow"> </CurrentWeather>
            </el-aside>

        </el-container>
    </div>
</template>
<script lang="ts" setup>
import CurrentWeather from '@/components/weather_details/sub_components/CurrentWeather.vue';
const weather = ref({
    icon: 404,
    temp: 20,
    text: "cloud"
});
const city = ref({
    name: '北京市',
    adm2: '昌平区'
});
const searchShow = ref(false)
</script>
<!-- <script>
export default {
  mounted() {
    console.log(this.data); // 在这里打印出 data 的值
  }
}
</script> -->

<style>
.is-selected {
    color: #1989fa;
}

/* .date-cell {
  position: relative;
  display: inline-block;
} */

.weather-icon {
    position: relative;
    bottom: 60px;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    /* 调整图片宽度 */
    height: 60px;
    /* 调整图片高度 */
}
</style>