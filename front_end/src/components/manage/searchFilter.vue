<template>
  <div class="p-4 space-y-4">
    <el-row>
      <el-col :span="10">
        <!-- 过滤器 -->
        <el-collapse v-model="filterVisible" accordion>
          <el-collapse-item title="请选择过滤参数" name="filter">
            <div class="space-y-2">
              <!-- 类型选择 -->
              <el-select v-model="selectType" placeholder="请选择类型">
                <el-option label="天气数据" value="weather"></el-option>
                <el-option label="地质灾害" value="disaster"></el-option>
              </el-select>
              <!-- 时间选项 -->
              <el-select
                v-model="timeOption"
                placeholder="请选择时间选项"
                v-if="selectType === 'weather'"
              >
                <el-option label="按月" value="month"></el-option>
                <el-option label="按日" value="day"></el-option>
                <el-option label="按周" value="week"></el-option>
              </el-select>
              <!-- 时间段选择 -->
              <el-date-picker
                v-model="selectedDate"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                format="yyyy-MM-dd"
                clearable
              ></el-date-picker>
              <!-- 地点选择 -->
              <el-select v-model="selectedLocation" placeholder="请选择地点">
                <el-option
                  v-for="location in locations"
                  :key="location.value"
                  :label="location.label"
                  :value="location.value"
                ></el-option>
              </el-select>
            </div>
          </el-collapse-item>
        </el-collapse>
      </el-col>
      <el-col :span="4"></el-col>
      <el-col :span="10" class="text-right">
        <!-- 主搜索框 -->
        <el-input
          v-model="searchQuery"
          placeholder="请输入搜索关键词"
          clearable
          @clear="handleSearch"
        >
          <template #append>
            <el-button @click="handleSearch">
              <el-icon class="mr-2"><Search></Search></el-icon>
              搜索</el-button
            >
          </template>
        </el-input>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
const searchQuery = ref("");
const filterVisible = ref("false");
const selectType = ref("");
const timeOption = ref("");
const selectedDate = ref("");
const selectedLocation = ref("");
const locations = [
  { label: "北京", value: "beijing" },
  { label: "上海", value: "shanghai" },
  { label: "广东", value: "guangdong" },
  { label: "深圳", value: "shenzhen" },
  { label: "杭州", value: "hangzhou" },
  { label: "成都", value: "chengdu" },
  { label: "武汉", value: "wuhan" },
  { label: "西安", value: "xian" },
  { label: "重庆", value: "chongqing" },
  { label: "南京", value: "nanjing" },
  { label: "苏州", value: "suzhou" },
  { label: "天津", value: "tianjin" },
  { label: "厦门", value: "xiamen" },
  { label: "青岛", value: "qingdao" },
  { label: "大连", value: "dalian" },
  { label: "宁波", value: "ningbo" },
  { label: "无锡", value: "wuxi" },
  { label: "福州", value: "fuzhou" },
  { label: "济南", value: "jinan" },
  { label: "长沙", value: "changsha" },
  { label: "郑州", value: "zhengzhou" },
  { label: "合肥", value: "hefei" },
  { label: "南昌", value: "nanchang" },
  { label: "贵阳", value: "guiyang" },
  { label: "昆明", value: "kunming" },
  { label: "兰州", value: "lanzhou" },
  { label: "银川", value: "yinchuan" },
  { label: "西宁", value: "xining" },
  { label: "拉萨", value: "lasa" },
  { label: "乌鲁木齐", value: "wulumuqi" },
  { label: "呼和浩特", value: "huhehaote" },
  { label: "南宁", value: "nanning" },
  { label: "海口", value: "haikou" },
  { label: "台北", value: "taibei" },
  { label: "香港", value: "xianggang" },
  { label: "澳门", value: "aomen" },
];

const handleSearch = () => {
  // 处理搜索逻辑，可以调用 API
  console.log("搜索关键词:", searchQuery.value);
};

const handleFilter = () => {
  // 处理过滤器逻辑，可以调用 API
  console.log("时间选项:", timeOption.value);
  console.log("选定日期范围:", selectedDate.value);
  console.log("选定地点:", selectedLocation.value);
};
</script>

<style>
/* 在这里使用 scoped 标签来限制样式仅适用于当前组件 */

/* 修改标题样式 */
.el-collapse-item__header {
  font-family: sans-serif; /* 将 YourCustomFont 替换为您想要应用的字体名称 */
  padding-left: 10px; /* 左边留出 10 像素的空间 */
  margin: 0%; /* 设置标题的外边距为 0% */
  height: 30px; /* 设置标题的宽度为 2 像素 */
  border-radius: 5px; /* 设置边框圆角为 5 像素 */
}

/* 可选：修改标题激活时的样式 */
.el-collapse-item__header.is-active {
  background-color: #fffff0; /* 修改激活时的背景颜色 */
}
</style>
