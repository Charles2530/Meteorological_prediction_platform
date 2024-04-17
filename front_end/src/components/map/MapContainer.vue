<template>
  <div id="container"></div>
</template>

<script setup lang="ts">
import { onMounted, reactive } from "vue";
import AMapLoader from "@amap/amap-jsapi-loader";

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

let map: {
  addControl: (arg0: any) => void;
  add: (arg0: any) => void;
  remove: (arg0: any) => void;
  setFitView: (arg0: any) => void;
  on: (
    arg0: string,
    arg1: (e: { lnglat: { lng: any; lat: any } }) => void
  ) => void;
  setCenter: (arg0: number[]) => void;
  setZoom: (arg0: number) => void;
} | null = null;
let AAMap: {
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
        center: [105, 36], // 初始化地图中心点位置
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
          "nation-stroke": "grey",
          "coastline-stroke": [0.8, 0.63, 0.94, 1],
          "province-stroke": "#a5a5a5",
          "city-stroke": "rgba(255,255,255,0.5)", //中国特有字段
          fill: "",
        },
      });
      map.addControl(new AMap.Scale());
      map.addControl(new AMap.ToolBar({ liteStyle: true }));
      map.add(wms);
      map.add(disCountry);
      dis_info.district = new AMap.DistrictSearch(dis_info.opts);
      dis_info.geoCoder = new AMap.Geocoder();
      handlerMapClick();
    })
    .catch((e) => {
      console.log(e);
    });
}

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
    }
  );
}

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
</script>

<style scoped>
#container {
  width: 100%;
  height: 100%;
  border: 1px solid red;
}
</style>
