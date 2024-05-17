// 获取assets静态资源
//天气图标
export const getAssetsFileIcon = (url: string) => {
  return new URL(`../assets/icons/png/${url}`, import.meta.url).href;
};
export const getAssetsFileAQI = (url: string) => {
  return new URL(`../assets/icons/AQI/${url}`, import.meta.url).href;
};
//灾害图标
export const getAssetsFile = (url: string) => {
  return new URL(`../assets/img/${url}`, import.meta.url).href;
};
// //echarts图片大小自适应
// import * as echarts from "echarts";
// import elementResizeDetectorMaker from "element-resize-detector";
// export const drawLine = (id: any, option: any) => {
//   const erd = elementResizeDetectorMaker();
//   let myChart = echarts.getInstanceByDom(document.getElementById(id));
//   if (myChart == null) {
//     myChart = echarts.init(document.getElementById(id));
//   }
//   myChart.setOption(option);
//   setTimeout(function () {
//     erd.listenTo(document.getElementById(id), (element: any) => {
//       myChart.resize();
//     });
//   }, 200);
// };
