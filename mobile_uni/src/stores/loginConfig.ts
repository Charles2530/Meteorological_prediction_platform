import { defineStore } from "pinia";
import { LoginConfig } from "@/types/pinia";

export const useLoginConfig = defineStore("loginConfig", {
  state: (): LoginConfig => ({
    showLoginPanel: false,
  }),
  actions: {
    setShowLoginPanel(show: boolean) {
      console.log("showLoginPanel", show);
      this.showLoginPanel = show;
    },
  },
});
