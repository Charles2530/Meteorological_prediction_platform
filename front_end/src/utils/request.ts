import axios, { AxiosInstance } from "axios";
import { Local } from "@/utils/storage";
import pinia from "@/stores";
import { useUserInfo } from "@/stores/userInfo";
import { useLoginConfig } from "@/stores/loginConfig";

const loginConfig = useLoginConfig(pinia);
const service: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_APP_BASE_API,
  timeout: 10000,
});
const getCsrfToken = () => {
  // 返回 CSRF 令牌
  // 例如，从浏览器 Cookie 中获取
  return document.cookie.replace(
    /(?:(?:^|.*;\s*)csrf\-token\s*\=\s*([^;]*).*$)|^.*$/,
    "$1"
  );
};

service.interceptors.request.use(
  (config) => {
    config.headers["Authorization"] = `${Local.get("Bearer")?.Bearer ?? ""}`;
    const csrfToken = getCsrfToken();
    if (csrfToken) {
      config.headers["X-CSRFToken"] = csrfToken;
    }
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
      ElMessage({
        message: error.message,
        type: "error",
        duration: 3000,
      });
      loginConfig.setShowLoginPanel(true);
    } else {
      ElMessage({
        message: error.message,
        type: "error",
        duration: 3000,
      });
    }
    return Promise.reject(error);
  }
);

export default service;
