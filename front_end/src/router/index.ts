import { createRouter, createWebHashHistory } from "vue-router";
import { UserRole } from "@/types/user";
import { useUserInfo } from "@/stores/userInfo";
import { useLoginConfig } from "@/stores/loginConfig";
import { get } from "@/api/index";
import { UserInfo } from "@/types/user";
// 定义路由部分
// 网站首页
const Home = () => import("@/views/home/index.vue");
// 历史记录
const History = () => import("@/views/home/weatherDetails.vue");
// 数据分析
const Statistics = () => import("@/views/home/statisticsCenter.vue");
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
const routes: any = [
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
      permission: [UserRole.User, UserRole.Administrator],
    },
  },
  {
    path: "/statistics",
    name: "Statistics",
    component: Statistics,
    meta: {
      permission: [UserRole.User, UserRole.Administrator],
    },
  },
  {
    path: "/alarm",
    name: "Alarm",
    component: Alarm,
    meta: {
      permission: [UserRole.User, UserRole.Administrator],
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
          permission: [UserRole.Administrator],
          //   permission: [UserRole.Administrator, UserRole.User, UserRole.Visitor],
        },
      },
      {
        path: "data",
        component: DataManage,
        meta: {
          permission: [UserRole.Administrator],
          //   permission: [UserRole.Administrator, UserRole.User, UserRole.Visitor],
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
    routes.some((item: any) =>
      new RegExp("^" + item.path.split("/:")[0] + "(?:/.*)?$").test(to.path)
    )
  ) {
    // if (to.name !== "Home") {
    //   const userInfo = useUserInfo();
    //   const themeConfig = useLoginConfig();
    //   const permissions = to.meta.permission;
    //   console.log(permissions);
    //   if (permissions.includes(userInfo.role)) {
    //     next();
    //   } else {
    //     themeConfig.showLoginPanel = true;
    //   }
    // } else {
    //   next();
    // }
        const userInfo = useUserInfo();
        const themeConfig = useLoginConfig();
        get<UserInfo>("/api/get_info/").then((res) => {
            userInfo.login(res.data);
            console.log("getToken")
            });
        const permissions=to.meta.permission
        console.log(permissions);
        if (permissions.includes(userInfo.role)) {
            themeConfig.showLoginPanel = false;
            next();
        } else{
            themeConfig.showLoginPanel = true;
        }
  } else {
    next({ name: "404Page" });
  }
});

export default router;
