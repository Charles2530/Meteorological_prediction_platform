import { createRouter, createWebHashHistory } from "vue-router";
// 定义路由部分
// 404页面
const Page404 = () => import("@/views/Page404.vue");
const routes = [
  {
    path: "/404",
    name: "404Page",
    component: Page404,
  },
];
const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
