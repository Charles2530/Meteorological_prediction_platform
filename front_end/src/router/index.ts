import { createRouter, createWebHashHistory } from "vue-router";
import { UserRole } from "@/types/user";
// 定义路由部分
// 网站首页
const Home = () => import("@/views/home/index.vue");
// 历史记录
const History = () => import("@/views/home/weatherDetails.vue");
// AI预测
const Predict = () => import("@/views/content/predictView.vue");
// 灾害订阅
const Alarm = () => import("@/views/content/alarmView.vue");
// 用户页面
const User = () => import("@/views/home/personalCenter.vue");
// 后台管理页面
const Manage = () => import("@c/manage/index.vue");
// 用户管理
const UserManage = () => import("@/components/manage/userManager.vue");
// 数据管理
const DataManage = () => import("@/components/manage/dataManager.vue");
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
    path: "/predict",
    name: "Predict",
    component: Predict,
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
  {
    path: "/manage",
    component: Manage,
    children: [
      {
        path: "",
        redirect: "/manage/user",
      },
      {
        path: "user",
        component: UserManage,
        meta: {
          //   permission: [UserRole.Administrator],
          permission: [UserRole.Administrator, UserRole.User, UserRole.Visitor],
        },
      },
      {
        path: "data",
        component: DataManage,
        meta: {
          //   permission: [UserRole.Administrator],
          permission: [UserRole.Administrator, UserRole.User, UserRole.Visitor],
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

export default router;
