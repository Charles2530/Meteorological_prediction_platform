import { createRouter, createWebHashHistory } from "vue-router";
import { userStore } from "@/store/user.ts";
// 定义路由部分
// 404页面
const Page404 = () => import("@/views/404.vue");
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
// 路由守卫
router.beforeEach((to, from, next) => {
  const store = userStore();
  if (store.token) {
    next();
  } else {
    console.log(to.path);
    if (
      routes.some((item) =>
        new RegExp("^" + item.path.split("/:")[0] + "(?:/.*)?$").test(to.path)
      )
    ) {
      next();
    } else {
      next({ name: "404Page" });
    }
  }
});

export default router;
