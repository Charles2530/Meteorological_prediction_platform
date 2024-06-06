import { defineStore } from "pinia";
import { UserRole, UserInfo } from "@/types/user.ts";
import { Local } from "@/utils/storage";
import router from "@/router/index";

export const useUserInfo = defineStore("userInfo", {
  state: (): UserInfo => {
    return {
      username: "",
      avatar: "http://dummyimage.com/100x100/FF0000/000000&text=Visitor",
      email: "",
      role: UserRole.Visitor,
    };
  },
  actions: {
    login(info: UserInfo, token?: string) {
      console.log("login success", info, token);
      this.$patch(info);
      if (token) Local.set("Bearer", { Bearer: `Bearer ${token}` });
    },
    logout() {
      this.$patch({
        username: "",
        avatar: "http://dummyimage.com/100x100/FF0000/000000&text=Visitor",
        email: "",
        role: UserRole.Visitor,
      });
      console.log("logout success", Local.get("Bearer"));
      Local.remove("Bearer");
      router.push({ name: "Home" });
    },
    setAvatar(avatar: string) {
      this.avatar = avatar;
    },
  },
});
