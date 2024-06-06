<template>
  <el-container class="main-container" style="max-height: 85vh; overflow: auto">
    <el-header>
      <h1 class="title">灾害订阅</h1>
    </el-header>
    <el-row :gutter="20">
      <el-col :span="18">
        <!-- 加入搜索框(城市名) -->
        <el-select
          v-model="search"
          placeholder="选择订阅城市"
          class="input-with-select"
        >
          <el-option
            v-for="location in tableData"
            :key="location.city"
            :label="location.city"
            :value="location.city"
          ></el-option>
        </el-select>
      </el-col>
      <el-col :span="6">
        <!-- 加入搜索按钮 -->
        <el-button type="primary" @click="searchNotice" plain>
          <el-icon class="mr-3"><Search /></el-icon>
          搜索</el-button
        >
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="18">
        <el-card class="box-card" v-if="notifications.length === 0">
          <div class="clearfix">
            <span>订阅相关灾害信息 </span>
          </div>
          <div class="text item">您所订阅的区域暂无通知</div>
        </el-card>
        <el-card class="box-card" v-else>
          <div class="clearfix">
            <span>订阅相关灾害信息 </span>
          </div>
          <div
            v-for="notification in notifications"
            :key="notification.id"
            :id="'notification-' + notification.id"
            class="text item"
          >
            <noticeItem :notification="notification" />
          </div>
        </el-card>
        <el-card class="box-card">
          <div class="clearfix">
            <span>全国灾害信息速递 </span>
          </div>
          <div
            v-for="(notification, index) in global_notifications"
            :key="notification.id"
            :id="'notification-' + notification.id"
            class="text item"
          >
            <div class="text-blue-500 text-xl text-center">
              第{{ index + 1 }}条预警信息
            </div>
            <noticeItem :notification="notification" />
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="box-card">
          <div class="clearfix">
            <span>城市列表</span>
          </div>
          <el-autocomplete
            v-model="cities"
            placeholder="选择订阅城市"
            :fetch-suggestions="querySearch"
            clearable
            class="inline-input w-50"
            highlight-first-item
            :value-key="'label'"
          />
          <el-table :data="tableData" style="width: 100%">
            <el-table-column
              prop="city"
              label="城市"
              width="180"
            ></el-table-column>
            <el-table-column
              prop="status"
              label="状态"
              width="180"
            ></el-table-column>
          </el-table>
          <div class="mt-2">
            <el-button type="success" @click="subscribe" plain>
              <el-icon class="mr-3"><Plus /></el-icon>
              添加订阅</el-button
            >
            <el-button type="warning" @click="undo_subscribe" plain>
              <el-icon class="mr-3"><Minus /></el-icon>
              取消订阅</el-button
            >
          </div>
        </el-card>
        <noticeLevelList v-if="levelsLoaded" :cnt="levels" class="mt-4" />
      </el-col>
    </el-row>
  </el-container>
  <!-- 取消城市订阅的el-dialog,参考tableData数据的el-select -->
  <el-dialog
    title="取消订阅"
    v-model="undo_subscribe_dialog"
    width="30%"
    @close="undo_subscribe_dialog = false"
  >
    <!-- 取消订阅的el-select -->
    <el-text>
      <p class="text-gray-400">请选择要取消订阅的城市</p>
    </el-text>
    <el-select v-model="form.city" placeholder="请选择城市" class="my-3">
      <el-option
        v-for="item in tableData"
        :key="item.city"
        :label="item.city"
        :value="item.city"
      ></el-option>
    </el-select>
    <div class="dialog-footer">
      <el-button @click="undo_subscribe_dialog = false">取 消</el-button>
      <el-button type="primary" @click="deleteSubscribe">确 定</el-button>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { NotificationData, GetSubscribeResponse } from "@/types/weather";
import noticeItem from "@c/notice/noticeItem.vue";
import { post, get } from "@/api/index.ts";
import noticeLevelList from "@/components/notice/noticeLevelList.vue";
import { china_cities } from "@/stores/cities";
interface LabelItem {
  label: string;
  value: string;
}
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
const undo_subscribe_dialog = ref(false);
const form = reactive({
  city: "",
});
const undo_subscribe = () => {
  undo_subscribe_dialog.value = true;
};
const deleteSubscribe = () => {
  undo_subscribe_dialog.value = false;
  tableData.value = tableData.value.filter((item) => item.city !== form.city);
  post<SubscribeResponse>("/api/subscribe/", { cities: form.city }).then(
    (res) => {
      console.log(res.data.success);
    }
  );
};
const all_notifications = reactive<NotificationData[]>([]);
const notifications = reactive<NotificationData[]>([]);
const global_notifications = reactive<NotificationData[]>([]);
interface NotificationResponse {
  notifications: NotificationData[];
}
const fetchNotifications = async () => {
  get<NotificationResponse>("/api/alarm_resent_notices/").then((res) => {
    global_notifications.splice(
      0,
      global_notifications.length,
      ...res.data.notifications
    );
  });
  get<NotificationResponse>("/api/alarm_notices/").then((res) => {
    notifications.splice(0, notifications.length, ...res.data.notifications);
    all_notifications.splice(
      0,
      notifications.length,
      ...res.data.notifications
    );
  });
};
onMounted(() => {
  labels.value = loadAll();
  fetchNotifications();
  getSubscribeStatus();
  routerToNoticeId();
});
const routerToNoticeId = function () {
  const params = window.location.hash.split("?");
  if (params.length > 1) {
    const query = params[1].split("=");
    if (query[0] === "notificationId") {
      const notificationId = parseInt(query[1]);
      const notificationElement = document.getElementById(
        `notification-${notificationId}`
      );
      if (notificationElement) {
        notificationElement.scrollIntoView({ behavior: "smooth" });
      }
    }
  }
};
const cities = ref("");
const tableData = ref([]);
const levels = ref([]);
interface GetAlarmLevelResponse {
  cnt: number[];
}
const getSubscribeStatus = () => {
  get<GetSubscribeResponse>("/api/subscribe/").then((res) => {
    tableData.value.splice(0, tableData.value.length, ...res.data.tableData);
  });
  get<GetAlarmLevelResponse>("/api/get_alarm_level/").then((res) => {
    console.log(res.data.cnt);
    levels.value = res.data.cnt;
  });
};
interface SubscribeResponse {
  success: string;
}
const subscribe = () => {
  if (cities.value === "") {
    ElMessage({
      message: "请输入城市名",
      type: "warning",
    });
    return;
  }
  // 完成去重功能
  for (let i = 0; i < tableData.value.length; i++) {
    console.log(tableData.value[i].city, cities.value);
    if (tableData.value[i].city === cities.value) {
      ElMessage({
        message: "已订阅该城市",
        type: "warning",
      });
      return;
    }
  }
  tableData.value.push({ city: cities.value, status: "已订阅" });
  post<SubscribeResponse>("/api/subscribe/", { cities: cities.value }).then(
    (res) => {
      console.log(res.data.success);
    }
  );
};
// search part
const search = ref("");
const searchNotice = function () {
  if (search.value === "") {
    ElMessage({
      message: "请输入城市名",
      type: "warning",
    });
    return;
  }
  // 过滤通知列表
  const filteredNotifications = all_notifications.filter((notification) =>
    notification.city.includes(search.value)
  );
  console.log(filteredNotifications);
  notifications.splice(0, notifications.length, ...filteredNotifications);
  console.log(notifications);
};
const levelsLoaded = ref(false);
watch(levels, () => {
  levelsLoaded.value = true;
});
</script>
<style scoped>
.clearfix {
  text-decoration: dashed;
  font-size: large;
  font-weight: bold;
  margin-left: 2%;
}
.main-container {
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.box-card {
  border-radius: 10px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  transition: 0.3s;
}

.box-card:hover {
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
}

.text.item {
  margin-bottom: 12px;
  background: #fff;
  padding: 10px;
  border-radius: 8px;
}

.input-with-select {
  margin-bottom: 20px;
}
</style>
