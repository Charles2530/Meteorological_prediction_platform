import { createRouter, createWebHashHistory } from "vue-router";
import { UserRole } from "@/types/user";
import { useUserInfo } from "@/stores/userInfo";
import { useLoginConfig } from "@/stores/loginConfig";
import { get } from "@/api/index";
import { UserInfo } from "@/types/user";

// 速览首页
const Home = () => import("@/views/home/index.vue");
// 地图页面
const Map = () => import("@/views/home/mapView.vue");
// 天气数据
const Weather = () => import("@/views/home/weatherView.vue");
// 用户页面
const User = () => import("@/views/home/personalCenter.vue");
// 404页面
const Page404 = () => import("@/views/Page404.vue");
const routes: any = [
  {
    path: "/",
    redirect: "/home",
    children: [
      {
        path: "/home",
        name: "Home",
        component: Home,
        meta: {
          permission: [UserRole.User, UserRole.Administrator],
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
        path: "/map",
        name: "Map",
        component: Map,
        meta: {
          permission: [UserRole.Visitor, UserRole.User, UserRole.Administrator],
        },
      },
      {
        path: "/weather",
        name: "Weather",
        component: Weather,
        meta: {
          permission: [UserRole.User, UserRole.Administrator],
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
    if (to.name !== "Home") {
        const userInfo = useUserInfo();
        const themeConfig = useLoginConfig();
        get<UserInfo>("/api/get_info/").then((res) => {
            userInfo.login(res.data);
            console.log("getToken")
            if (router.currentRoute.value.meta.permission?.includes(userInfo.role)){
                themeConfig.showLoginPanel = false;
                next()
            }else {
                themeConfig.showLoginPanel = true;
            }
            });
        // console.log(permissions);
        // if (permissions.includes(userInfo.role)) {
        //     next();
        // } 
    } else {
      next();
    }
  } else {
    next({ name: "404Page" });
  }
});

export default router;
