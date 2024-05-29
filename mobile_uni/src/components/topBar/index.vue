<template>
  <div class="topbar-index">
    <Logo />
    <div class="sub-title">
      {{ currentCity }}
    </div>
    <div class="flex-grow"></div>
    <UserMenu />
  </div>
</template>
<script setup lang="ts">
import { post, get } from "@/api/index.ts";
onMounted(() => {
  getPresentCity();
});
const Logo = defineAsyncComponent(() => import("@c/topBar/logo.vue"));
const UserMenu = defineAsyncComponent(() => import("@c/topBar/userMenu.vue"));
const currentCity = ref("");
const getPresentCity = async () => {
  get<CityInfoResponse>("/api/current/getCityInfo/").then((res) => {
    currentCity.value = res.data.message.city;
  });
  if (!currentCity.value) {
    currentCity.value = "北京市";
  }
};
</script>

<style scoped lang="scss">
.topbar-index {
  height: 6vh;
  display: flex;
  align-items: center;
  padding-right: 20px;
  border-bottom: 1px solid #4c4d4f;
  background-color: var(--bg-topBar-color);
  transition: background-color 0.2s ease;
}
.sub-title {
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
  text-shadow: 1px 1px 2px #000000;
  margin-left: 6px;
}
.flex-grow {
  flex-grow: 1;
}
</style>
