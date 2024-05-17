// 获取assets静态资源
//天气图标
export const getAssetsFileIcon = (url: string) => {
  return new URL(`../assets/icons/png/${url}`, import.meta.url).href;
};
//灾害图标
export const getAssetsFile = (url: string) => {
  return new URL(`../assets/img/${url}`, import.meta.url).href;
};
//防抖函数
export const debounce = (func: Function, wait: number) => {
  let timer: any;
  return function (this: any, ...args: any[]) {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      func.apply(this, args);
    }, wait);
  };
};
