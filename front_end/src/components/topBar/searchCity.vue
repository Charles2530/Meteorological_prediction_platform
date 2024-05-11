<template>
  <div class="flex gap-4">
    <div class="sub-title my-2 text-sm text-white">
      当前城市 {{ cityMessage.city }}
    </div>
    <el-autocomplete
      v-model="state"
      :fetch-suggestions="querySearch"
      clearable
      class="inline-input w-50"
      @select="handleSelect"
      highlight-first-item
      :value-key="'label'"
    />
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { china_cities } from "@/stores/cities";
import { get } from "@/api/index.ts";
import { CityWeatherData } from "@/types/weather";
onMounted(() => {
  getPresentCity();
});
interface CityInfoResponse {
  status: boolean;
  message: CityWeatherData;
}
const cityMessage = reactive<CityWeatherData>({} as CityWeatherData);
const getPresentCity = async () => {
  get<CityInfoResponse>("/api/getCityInfo/").then((res) => {
    cityMessage.city = res.data.message.city;
  });
};
interface RestaurantItem {
  value: string;
  label: string;
}

const state = ref("");
const city = ref("");

const restaurants = ref<RestaurantItem[]>([]);
const querySearch = (queryString: string, cb: any) => {
  const results = queryString
    ? restaurants.value.filter(createFilter(queryString))
    : restaurants.value;
  cb(results);
};

const createFilter = (queryString: string) => {
  return (restaurant: RestaurantItem) => {
    return (
      restaurant.label.toLowerCase().indexOf(queryString.toLowerCase()) === 0
    );
  };
};
const loadAll = () => {
  return china_cities;
};

const handleSelect = (item: RestaurantItem) => {
  state.value = item.label;
  city.value = item.value;
  console.log(state.value);
  console.log(item);
};

onMounted(() => {
  restaurants.value = loadAll();
});
</script>
