<template>
  <div class="flex gap-4">
    <div class="sub-title my-2 text-sm text-white">
      当前城市 {{ currentCity }}
    </div>
    <el-autocomplete
      v-model="state"
      :fetch-suggestions="querySearch"
      clearable
      class="inline-input w-50"
      @select="handleSelect"
      highlight-first-item
      :value-key="'label'"
      @change="updateUserCity"
    />
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { china_cities } from "@/stores/cities";
import { post, get } from "@/api/index.ts";
import { CityWeatherData } from "@/types/weather";
onMounted(() => {
  getPresentCity();
});
interface CityInfoResponse {
  status: boolean;
  message: CityWeatherData;
}
const currentCity = ref("");
const getPresentCity = async () => {
  get<CityInfoResponse>("/api/getCityInfo/").then((res) => {
    currentCity.value = res.data.message.city;
  });
  if (!currentCity.value) {
    currentCity.value = "北京市";
  }
};
interface LabelItem {
  label: string;
  value: string;
}
const state = ref("");
const city = ref("");

const labels = ref<LabelItem[]>([]);
const querySearch = (queryString: string, cb: any) => {
  const results = queryString
    ? labels.value.filter(createFilter(queryString))
    : labels.value;
  cb(results);
};

const createFilter = (queryString: string) => {
  return (restaurant: LabelItem) => {
    return (
      restaurant.label.toLowerCase().indexOf(queryString.toLowerCase()) === 0
    );
  };
};
const loadAll = () => {
  return china_cities;
};

const handleSelect = (item: LabelItem) => {
  state.value = item.label;
  city.value = item.value;
};
interface CityInfoResponse {
  success: boolean;
  reason?: string;
}
const updateUserCity = async () => {
  post<CityInfoResponse>("/api/operate/current_city", {
    city: state.value,
  }).then((res) => {
    if (res.data.success) {
      getPresentCity();
    }
  });
};
onMounted(() => {
  labels.value = loadAll();
});
</script>
