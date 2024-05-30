<template>
  <el-autocomplete
    placeholder="切换当前城市"
    v-model="state"
    :fetch-suggestions="querySearch"
    clearable
    class="inline-input"
    @select="handleSelect"
    highlight-first-item
    :value-key="'label'"
    @change="updateUserCity"
  />
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
  get<CityInfoResponse>("/api/current/getCityInfo/").then((res) => {
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
  post<CityInfoResponse>("/api/operate/current_city/", {
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
<style scoped>
.flex {
  align-items: center;
}

.sub-title {
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
  text-shadow: 1px 1px 2px #000000;
}

.inline-input {
  max-width: 50%;
  min-width: 30%;
}

.el-autocomplete {
  border: 1px solid #bfcbd9;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  background-color: #f5f7fa;
  color: #48576a;
}

.el-autocomplete:focus {
  outline: none;
  border-color: #409eff;
}
</style>
