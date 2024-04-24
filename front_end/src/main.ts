import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import store from "./stores";
import router from "./router";
import pinia from "@/stores/index";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import ElementPlus from "element-plus";
import md5 from "js-md5";

const app = createApp(App);
// 将 md5 挂载到 Vue 实例的全局属性上
app.config.globalProperties.$md5 = md5;
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}
app.use(ElementPlus);
app.use(store);
app.use(router);

import { UserInfo } from "@/types/user";
import { useUserInfo } from "@/stores/userInfo";
import { get } from "@/api/index";
import { useLoginConfig } from "./stores/loginConfig";

const userInfo = useUserInfo(pinia);
const loginConfig = useLoginConfig();

get<UserInfo>("/api/getInfo").then((res) => {
  userInfo.login(res.data);
  // @ts-ignore
  if (router.currentRoute.value.meta.permission?.includes(userInfo.role))
    loginConfig.showLoginPanel = false;
});

app.mount("#app");
