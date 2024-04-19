<template>
  <el-container class="main-container">
    <el-header>
      <h1 class="title">灾害订阅</h1>
    </el-header>
    <el-row :gutter="20">
      <el-col :span="18">
        <el-card class="box-card">
          <div class="clearfix">
            <span class="">灾害信息</span>
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
      </el-col>

      <el-col :span="6">
        <el-card class="box-card">
          <div class="clearfix">
            <span>城市列表</span>
          </div>
          <el-input
            v-model="cities"
            placeholder="输入城市名"
            class="input-with-select"
          ></el-input>
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
          <el-button type="primary" @click="subscribe">订阅</el-button>
        </el-card>
      </el-col>
    </el-row>
  </el-container>
</template>

<script setup lang="ts">
import { NotificationData } from "@/types/weather";
import noticeItem from "@c/notice/noticeItem.vue";
import { post, get } from "@/api/index.ts";

const notifications_example = ref<NotificationData[]>([
  {
    id: 1,
    img: "https://ts1.cn.mm.bing.net/th/id/R-C.5b318dcf92724f1b99c194f891602f06?rik=eg7%2f2A2FtTorZA&riu=http%3a%2f%2fappdata.langya.cn%2fuploadfile%2f2020%2f0722%2f20200722090230374.jpg&ehk=DTXD%2bpXZoXFP8PBVpZeox9lN%2f5eoUhdebZg6f1gIPs0%3d&risl=&pid=ImgRaw&r=0",
    title: "内蒙古通辽市扎鲁特旗气象台发布大风蓝色预警[IV级/一般]",
    date: "2024-04-12T12:09:08",
    content:
      "内蒙古通辽市扎鲁特旗气象台2024年04月12日12时09分发布大风蓝色预警信号:24小时内扎鲁特旗可能受大风影响，平均风力可达6级以上，或者阵风7级以上;或者已经受大风影响，平均风力为6~7级，或者阵风7~8级并可能持续。",
    instruction: "请有关单位和人员做好防范准备。",
  },
]);
const notifications = reactive<NotificationData[]>([]);
interface NotificationResponse {
  notifications: NotificationData[];
}
const fetchNotifications = async () => {
  get<NotificationResponse>("/api/alarm_notices").then((res) => {
    notifications.splice(
      0,
      notifications.length + notifications_example.value.length,
      ...notifications_example.value,
      ...res.data.notifications
    );
  });
  //   get<NotificationResponse>("/api/alarm_notices").then((res) => {
  //     notifications.splice(0, notifications.length, ...res.data.notifications);
  //   });
};
onMounted(() => {
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
      console.log(notificationId);
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
const tableData = ref([
  { city: "北京", status: "已订阅" },
  { city: "上海", status: "已订阅" },
]);
interface GetSubscribeResponse {
  tableData: { city: string; status: string }[];
}
const getSubscribeStatus = () => {
  get<GetSubscribeResponse>("/api/subscribe").then((res) => {
    tableData.value.splice(0, tableData.value.length, ...res.data.tableData);
  });
};
interface SubscribeResponse {
  success: string;
}
const subscribe = () => {
  tableData.value.push({ city: cities.value, status: "已订阅" });
  post<SubscribeResponse>("/api/subscribe", { cities: cities.value }).then(
    (res) => {
      console.log(res.data.success);
    }
  );
};
</script>

<style scoped>
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

el-button {
  margin-top: 20px;
}
</style>
