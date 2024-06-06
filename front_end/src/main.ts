import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import store from "./stores";
import router from "./router";
// import pinia from "@/stores/index";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import ElementPlus from "element-plus";
import md5 from "js-md5";

const app = createApp(App);
// const userInfo = useUserInfo(pinia);
// const loginConfig = useLoginConfig();

// get<UserInfo>("/api/get_info/").then((res) => {
//   userInfo.login(res.data);
//   // @ts-ignore
//   if (router.currentRoute.value.meta.permission?.includes(userInfo.role))
//     loginConfig.showLoginPanel = false;
// });
// 将 md5 挂载到 Vue 实例的全局属性上
app.config.globalProperties.$md5 = md5;
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}
app.use(ElementPlus);
app.use(store);
app.use(router);

// import { UserInfo } from "@/types/user";
// import { useUserInfo } from "@/stores/userInfo";
// import { get } from "@/api/index";
// import { useLoginConfig } from "./stores/loginConfig";

/*全局引入echarts*/
import * as echartsComponent from "echarts";
// echarts 挂载到 Vue实例中
// Vue.prototype.$echarts = echarts; // vue2的挂载方式
app.config.globalProperties.$echarts = echartsComponent; // /vue3的挂载方式（一个用于注册能够被应用内所有组件实例访问到的全局属性的对象。）
app.mount("#app");
