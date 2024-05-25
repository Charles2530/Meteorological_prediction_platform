/// <reference types="vite/client" />
//使typescript 识别 .vue 文件
declare module "*.vue" {
  import { ComponentOptions } from "vue";
  const componentOptions: ComponentOptions;
  export default componentOptions;
}
