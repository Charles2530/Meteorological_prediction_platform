import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import store from "./stores";
import router from "./router";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import ElementPlus from "element-plus";

const app = createApp(App);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}
app.use(ElementPlus);
app.use(store);
app.use(router);
app.mount("#app");
