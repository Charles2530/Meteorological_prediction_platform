import { createRouter, createWebHashHistory } from "vue-router";
import { UserRole } from "@/types/user";
// 网站首页
const Home = () => import("@/views/home/index.vue");
// 历史记录
const History = () => import("@/views/home/weatherDetails.vue");
// 灾害订阅
const Alarm = () => import("@/views/home/alarmView.vue");
// 用户页面
const User = () => import("@/views/home/personalCenter.vue");
// 404页面
const Page404 = () => import("@/views/Page404.vue");
const routes = [
  {
    path: "/",
    redirect: "/home",
    children: [
      {
        path: "/home",
        name: "Home",
        component: Home,
        meta: {
          permission: [UserRole.Visitor, UserRole.User, UserRole.Administrator],
        },
      },
      {
        path: "/user",
        name: "user",
        component: User,
        meta: {
          permission: [UserRole.User, UserRole.Administrator],
        },
      },
      {
        path: "/history",
        name: "History",
        component: History,
        meta: {
          permission: [UserRole.Visitor, UserRole.User, UserRole.Administrator],
        },
      },
      {
        path: "/alarm",
        name: "Alarm",
        component: Alarm,
        meta: {
          permission: [UserRole.Visitor, UserRole.User, UserRole.Administrator],
        },
      },
    ],
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

router.beforeEach((to, from, next) => {
  if (
    routes.some((item) =>
      new RegExp("^" + item.path.split("/:")[0] + "(?:/.*)?$").test(to.path)
    )
  ) {
    next();
  } else {
    next({ name: "404Page" });
  }
});

export default router;
