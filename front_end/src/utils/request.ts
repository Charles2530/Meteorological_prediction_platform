import axios, { AxiosInstance } from "axios";
import { ElNotification } from "element-plus";
import { Local } from "@/utils/storage";
import pinia from "@/stores";
import { useUserInfo } from "@/stores/userInfo";

const service: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
});

service.interceptors.request.use(
  (config) => {
    config.headers["Authorization"] = `${Local.get("Bearer")?.Bearer ?? ""}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

service.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.log(error);

    const userInfo = useUserInfo(pinia);
    // 401 请求要求用户的身份认证 清除token信息, 显示登录界面
    if (error.response.status === 401) {
      userInfo.logout();
      ElNotification({
        message: error.message,
        type: "error",
        duration: 3000,
      });
    } else {
      ElNotification({
        title: error.code,
        message: error.message,
        type: "error",
        duration: 3000,
      });
    }
    return Promise.reject(error);
  }
);

export default service;
