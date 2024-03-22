import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import store from "./stores";
import router from "./router";
import pinia from "@/stores/index";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import ElementPlus from "element-plus";

const app = createApp(App);
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

// get<UserInfo>("/api/getInfo").then((res) => {
//   userInfo.login(res.data);
//   // @ts-ignore
//   if (router.currentRoute.value.meta.permission?.includes(userInfo.role))
//     loginConfig.showLoginPanel = false;
// });

app.mount("#app");
