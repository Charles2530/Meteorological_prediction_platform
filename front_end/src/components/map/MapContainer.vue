<template>
  <div id="container"></div>
</template>

<script setup lang="ts">
import { onMounted, reactive } from "vue";
import AMapLoader from "@amap/amap-jsapi-loader";
import { getAssetsFile } from '@/utils/pub-use'

// 设置安全密钥
(window as any)._AMapSecurityConfig = {
  securityJsCode: "ff942cdc56a565fb2e5d5b5e6a3481ae",
};

//高亮区域信息
const dis_info = reactive({
  districtCode: "100000",
  districtName: "中国",
  district: null,
  geoCoder: null,
  polygons: <any>[],
  //行政区划查询
  opts: {
    subdistrict: 2, //获取边界不需要返回下级行政区
    extensions: "all", //返回行政区边界坐标组等具体信息
    level: "province", //查询行政级别为 区
  },
});

//灾害标记信息
const hazardMarkData = reactive([
  {
    place: '甘肃省 兰州市',
    longitude: 114.344706,
    latitude: 38.051262,
    type: "地震",
    time:'4月23日5:00',
    level:'蓝',
  },
  {
    place: '甘肃省 兰州市',
    longitude: 103.343524,
    latitude: 37.049604,
    type: "大风",
    time:'4月24日晚',
    level:'红',
  },
  {
    place: '甘肃省 兰州市',
    longitude: 93.343524,
    latitude: 33.049604,
    type: "大风",
    time:'4月24日晚',
    level:'蓝',
  },
  {
    place: '甘肃省 兰州市',
    longitude: 110.343524,
    latitude: 29.049604,
    type: "大风",
    time:'4月24日晚',
    level:'红',
  },
  {
    place: '甘肃省 兰州市',
    longitude: 87.343524,
    latitude: 35.049604,
    type: "大风",
    time:'4月24日晚',
    level:'红',
  }
]);

let map: {
  getCenter: any;
  addControl: (arg0: any) => void;
  add: (arg0: any) => void;
  remove: (arg0: any) => void;
  setFitView: (arg0: any) => void;
  on: (
    arg0: string,
    arg1: (e: {
      target: any;
      pixel: any;
      type: any; lnglat: { lng: any; lat: any } 
    }) => void
  ) => void;
  setCenter: (arg0: number[]) => void;
  setZoom: (arg0: number) => void;
} | null = null;

let AAMap: {
  Icon: any;
  Size: any;
  InfoWindow: any;
  LngLat: any;
  Marker: any;
  Polygon: new (arg0: {
    strokeWeight: number;
    path: any;
    fillOpacity: number;
    fillColor: string;
    strokeColor: string;
  }) => any;
} = null;

export interface API {
  dis_info: { districtName: String };
}

defineExpose({
  dis_info,
});

onMounted(() => {
  initMap();
});

function initMap() {
  AMapLoader.load({
    key: "671116f417c14e708dd09edf8d4ab63a",
    version: "2.0",
    plugins: [
      "AMap.Scale",
      "AMap.ToolBar",
      "AMap.DistrictSearch",
      "AMap.Geocoder",
    ],
  })
    .then((AMap) => {
      // 初始化地图
      AAMap = AMap;
      map = new AMap.Map("container", {
        viewMode: "2D", // 是否为3D地图模式
        // zoom: 4.8, // 初始化地图级别
        // center: [105,36], // 初始化地图中心点位置
        zoom: 4.8, // 初始化地图级别
        center: [103, 36], // 初始化地图中心点位置
      });
      // 天地图图层
      const wms = new AMap.TileLayer.WMTS({
        url: "http://t0.tianditu.gov.cn/ter_w/wmts",
        blend: false,
        opcaity: 1,
        zIndex: 1,
        tileSize: 256,
        params: {
          Layer: "ter",
          Version: "1.0.0",
          Format: "tiles",
          TileMatrixSet: "w",
          STYLE: "default",
          tk: "ef15c00f78f64844dcab11c1c94198e4",
        },
      });
      // 行政区图层 https://lbs.amap.com/api/javascript-api/guide/layers/districtlayer
      var disCountry = new AMap.DistrictLayer.Country({
        SOC: "CHN",
        depth: 2,
        styles: {
          // "nation-stroke": "grey",
          "nation-stroke": "red",
          "coastline-stroke": [0.8, 0.63, 0.94, 1],
          "province-stroke": "#a5a5a5",
          "city-stroke": "rgba(255,255,255,0.5)", //中国特有字段
          fill: "",
        },
      });
      map.addControl(new AMap.Scale({position: 'LB'}));
      map.addControl(new AMap.ToolBar({ liteStyle: true, position: 'LT'}));
      map.add(wms);
      map.add(disCountry);
      dis_info.district = new AMap.DistrictSearch(dis_info.opts);
      dis_info.geoCoder = new AMap.Geocoder();
      handlerMapClick();
      markPoints();
    })
    .catch((e) => {
      console.log(e);
    });
}

//高亮区域
function drawBounds() {
  //行政区查询
  dis_info.district.search(
    dis_info.districtCode,
    function (_status: any, result: { districtList: { boundaries: any }[] }) {
      map.remove(dis_info.polygons); //清除上次结果
      dis_info.polygons = [];
      var bounds = result.districtList[0].boundaries;
      if (bounds) {
        for (var i = 0, l = bounds.length; i < l; i++) {
          //生成行政区划polygon
          const polygon = new AAMap.Polygon({
            strokeWeight: 1,
            path: bounds[i],
            fillOpacity: 0.4,
            fillColor: "#80d8ff",
            strokeColor: "#0091ea",
          });
          map.add(polygon);
          dis_info.polygons.push(polygon);
        }
      }

      map.add(dis_info.polygons);
      map.setFitView(dis_info.polygons); //视口自适应
      map.setZoom(5.4);
    }
  );
}

//点击区域触发事件
function handlerMapClick() {
  map.on("click", (e: { lnglat: { lng: any; lat: any } }) => {
    // 点击坐标
    const markersPosition = [e.lnglat.lng, e.lnglat.lat];

    // eslint-disable-next-line no-undef
    // 根据坐标获取位置信息
    dis_info.geoCoder.getAddress(
      markersPosition,
      (status: string, result: { regeocode: { addressComponent: any } }) => {
        if (status === "complete" && result.regeocode) {
          // this.address = result.regeocode.formattedAddress
          // console.log('点击位置信息：', result.regeocode)
          // // id
          let addressComponent = result.regeocode.addressComponent;
          //   let reg = /.+?(省|市|自治区|自治州|县|区)/g
          dis_info.districtName = addressComponent.province;
          dis_info.districtCode = addressComponent.adcode.substr(0, 2) + "0000";
          // let cityId = parseInt(adcode.substr(0, 4) + '00')
          // let areaId = adcode
          if (dis_info.districtCode != "100000") {
            dis_info.districtName = dis_info.districtName + "/中国";
            drawBounds();
          } else {
            dis_info.districtName = "中国";
            map.remove(dis_info.polygons); //清除结果
            map.setCenter([105, 36]);
            map.setZoom(4.8);
          }
        } else {
          dis_info.districtName = "中国";
          map.remove(dis_info.polygons); //清除结果
          map.setCenter([105, 36]);
          map.setZoom(4.8);
        }
      }
    );
  });
}

//显示所有灾害标记
function markPoints() {
  hazardMarkData.forEach(item => {
    // 创建一个Marker实例：
    const marker = new AAMap.Marker({
      position: new AAMap.LngLat(item.longitude, item.latitude),   // 经纬度对象，也可以是经纬度构成的一维数组[lng, lat]
      // icon: getAssetsFile( 'pin_' + item.color +'.png'), // 添加 Icon 图标 URL
      icon: new AAMap.Icon({
        size: new AAMap.Size(23, 32),    // 图标尺寸
        image: getAssetsFile( 'pin_' + item.level +'.png'),
        imageSize: new AAMap.Size(23, 32)   // 根据所设置的大小拉伸或压缩图片
      }),
      title: '北京',
    });
    // 将创建的点标记添加到已有的地图实例：
    map.add(marker);
    //给标记点添加事件
    marker.on('click', (e: any) => setMarkWindows(e, item))
  });
}

//显示标记弹出框组件
function setMarkWindows(_e: any, item: { place: string; longitude: number; latitude: number; type: string; time: string; level: string; }) {
  let content = [
    `<div style='\'padding:0px' 0px = '' 4px; \'=''><b>${item.place}</b>`,
    `灾害类型 ：${item.type}`,
    `时间 ：${item.time}`,
    `等级 ：${item.level}`,
    // `<img src=${item.img} alt="" style="width: 100px;height: 100px">`
  ];
  // 创建 infoWindow 实例	
  let infoWindow = new AAMap.InfoWindow({
    content: content.join("<br>")  //传入 dom 对象，或者 html 字符串
  });
  // 打开信息窗体
  let dd = map.getCenter()
  // dd.pos = [e.pos[0], e.pos[1]]
  dd.lat = item.latitude
  dd.lng = item.longitude
  infoWindow.open(map, dd);
}
  
</script>

<style scoped>
#container {
  width: 100%;
  height: 100%;
  
}
</style>
