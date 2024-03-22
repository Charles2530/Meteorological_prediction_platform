import { createRouter, createWebHashHistory } from "vue-router";
import { UserRole } from "@/types/user";
// 定义路由部分
// 网站首页
const Home = () => import("@/views/home/index.vue");
// 404页面
const Page404 = () => import("@/views/Page404.vue");
const routes = [
  {
    path: "/",
    redirect: "/home",
  },
  {
    path: "/home",
    name: "Home",
    component: Home,
    meta: {
      permission: [UserRole.Visitor, UserRole.User, UserRole.Administrator],
    },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "404Page",
    component: Page404,
    meta: {
      permission: [UserRole.Visitor, UserRole.User, UserRole.Administrator],
      transition: "404Page",
    },
  },
];
const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
