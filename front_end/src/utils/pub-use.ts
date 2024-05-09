// 获取assets静态资源
//天气图标
export const getAssetsFileIcon = (url: string) => {
  return new URL(`../assets/icons/color-256/${url}`, import.meta.url).href;
};
//灾害图标
export const getAssetsFileHazard = (url: string) => {
  return new URL(`../assets/img/${url}`, import.meta.url).href;
};
