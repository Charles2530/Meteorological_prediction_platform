// 获取assets静态资源
export const getAssetsFile = (url: string) => {
  return new URL(`../assets/icons/color-256/${url}`, import.meta.url).href;
};
