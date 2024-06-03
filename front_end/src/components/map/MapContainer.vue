<template>
  <div id="mapContainer">
    <div class="input-card" style="position: relative; z-index: 100; top:25%; width: 100px;">
      <div class="layerbtns">
        <el-button :class="{ 'selected': buttonActive.A, 'unselected': !buttonActive.A }" :active="buttonActive.A"
          @click="clickA">
          <div class="btnDiv">
            <div class="btnName2">标准图层</div>
          </div>
        </el-button>
        <el-button :class="{ 'selected': buttonActive.B, 'unselected': !buttonActive.B }" :active="buttonActive.B"
          @click="clickB">
          <div class="btnDiv">
            <div class="btnName2">地形图层</div>
          </div>
        </el-button>
        <el-button :class="{ 'selected': buttonActive.C, 'unselected': !buttonActive.C }" :active="buttonActive.C"
          @click="clickC">
          <div class="btnDiv">
            <div class="btnName2">卫星图层</div>
          </div>
        </el-button>
      </div>
      <br />
      <br />
      <div class="layerbtns">
        <el-button :class="{ 'selected': buttonActive.d, 'unselected': !buttonActive.d }" :active="buttonActive.d"
          @click="clickd">
          <div class="btnDiv">
            <div class="btnName">地理环境</div>
            <div class="btnIcond"></div>
          </div>
        </el-button>
        <el-button width="600px" :class="{ 'selected': buttonActive.a, 'unselected': !buttonActive.a }"
          :active="buttonActive.a" @click="clicka">
          <div class="btnDiv">
            <div class="btnName">气温</div>
            <div class="btnIcona"></div>
          </div>
        </el-button>
        <el-button :class="{ 'selected': buttonActive.b, 'unselected': !buttonActive.b }" :active="buttonActive.b"
          @click="clickb">
          <div class="btnDiv">
            <div class="btnName">降水</div>
            <div class="btnIconb"></div>
          </div>
        </el-button>
        <el-button width="200px" :class="{ 'selected': buttonActive.f, 'unselected': !buttonActive.f }"
          :active="buttonActive.f" @click="clickf">
          <div class="btnDiv">
            <div class="btnName">空气质量</div>
            <div class="btnIconf"></div>
          </div>
        </el-button>
        <el-button :class="{ 'selected': buttonActive.e, 'unselected': !buttonActive.e }" :active="buttonActive.e"
          @click="clicke">
          <div class="btnDiv">
            <div class="btnName">灾害</div>
            <div class="btnIcone"></div>
          </div>
        </el-button>
        <el-button :class="{ 'selected': buttonActive.c, 'unselected': !buttonActive.c }" :active="buttonActive.c"
          @click="clickc">
          <div class="btnDiv">
            <div class="btnName">风场</div>
            <div class="btnIconc"></div>
          </div>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive } from "vue";
import AMapLoader from "@amap/amap-jsapi-loader";
import AMapWind from "amap-wind";
import { get } from "@/api/index.ts";
import { MapGeo, Point, Hazard, ProInfo } from "@/types/weather";
import { getAssetsFileAQI } from "@/utils/pub-use";
import { Interface } from "readline";

// 设置安全密钥
(window as any)._AMapSecurityConfig = {
  securityJsCode: "ff942cdc56a565fb2e5d5b5e6a3481ae",
};

const pos_info = reactive({
  pixel: null,          //所在网格
  lng: 0,               //所在经度
  lat: 0,               //所在纬度
  adcode: "100000",     //所在行政区划编码
  provinceCode: "",      //所在省编码
  provinceName: "中国", //所在省名称
  cityName: "",         //所在市名称
  districtName: "",      //所在县名称
  name: "",              //拼接名称
  weatherInfo: <Point>{},  //格点天气数据
  geoInfo: "",             //格点所在省份地理数据
  searcher: null,
  geoCoder: null,
  polygons: <any>[],
  //行政区划查询
  opts: {
    subdistrict: 2, //获取边界不需要返回下级行政区
    extensions: "all", //返回行政区边界坐标组等具体信息
    level: "province", //查询行政级别为 区
  },
});

const buttonActive = reactive({
  A: false,
  B: true,
  C: false,
  a: false,
  b: false,
  c: false,
  d: true,
  e: false,
  f: false,
});

declare let Loca: any

let map: {
  clearMap(): unknown;
  setCenter(markersPosition: any[], arg1: boolean, arg2: number): unknown;
  setFitView(polygons: any, arg1: boolean): unknown;
  setLimitBounds(bounds: any): unknown;
  getCenter: any;
  addControl: (arg0: any) => void;
  add: (arg0: any) => void;
  remove: (arg0: any) => void;
  on: (
    arg0: string,
    arg1: (e: {
      data: any;
      target: any;
      pixel: any;
      type: any; lnglat: { lng: any; lat: any }
    }) => void
  ) => void;
  setZoom: (arg0: number) => void;
} | null = null;

let AAMap: {
  Pixel: any;
  DistrictLayer: any;
  Polyline: any;
  Icon: any;
  Size: any;
  InfoWindow: any;
  LngLat: any;
  Marker: any;
} = null;

let loca: {
  [x: string]: any; remove(pl: { setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: { key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number; yoyo: boolean; repeat: number; }) => void; }): unknown; add: (arg0: any) => void;
} = null;

let heatmapTem: {
  remove(): unknown; setLoca(loca: { remove(pl: { setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: { key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number; yoyo: boolean; repeat: number; }) => void; }): unknown; add: (arg0: any) => void; }): unknown; destroy(): unknown; setSource: any; addAnimate: any; queryFeature?: any; setStyle?: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void;
} = null;

let heatmapWater: {
  remove(): unknown; setLoca(loca: { remove(pl: { setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: { key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number; yoyo: boolean; repeat: number; }) => void; }): unknown; add: (arg0: any) => void; }): unknown; destroy(): unknown; setSource: any; addAnimate: any; queryFeature?: any; setStyle?: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void;
} = null;

let windLayer: AMapWind = null;

let scatter: {
  getLabelsLayer(): unknown;
  getData(): unknown;
  getScatterLayer(): unknown;
  on(arg0: string, arg1: (event: any) => void): unknown;
  setLoca: (arg0: {
    [x: string]: any; remove(pl: {
      setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: {
        key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number // 设置安全密钥
        ; yoyo: boolean; repeat: number;
      }) => void;
    }): unknown; add: (arg0: any) => void;
  }) => void; remove: () => void; setSource: (arg0: null, arg1: { unit: string; size: number[]; texture: string; borderWidth: number; }) => void; queryFeature: (arg0: any) => any;
} = null;

let breath: { setLoca: (arg0: { [x: string]: any; remove(pl: { setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: { key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number; yoyo: boolean; repeat: number; }) => void; }): unknown; add: (arg0: any) => void; }) => void; remove: () => void; setSource: (arg0: any) => void; setStyle: (arg0: { unit: string; size: number[]; texture: string; animate: boolean; duration: number; }) => void; } = null;

let wms: null = null;

let sate: null = null;

let aqiLayer: {
  [x: string]: any;
  getScatterLayer(): unknown;
  on(arg0: string, arg1: () => void): unknown;
  setLoca: (arg0: {
    [x: string]: any; remove(pl: {
      setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: {
        key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number // 设置安全密钥
        ; yoyo: boolean; repeat: number;
      }) => void;
    }): unknown; add: (arg0: any) => void;
  }) => void; remove: () => void; setSource: (arg0: null, arg1: {
    icon: {
      type: string; image: (_index: any, feature: { properties: { aqi: any; mom: string | any[]; }; }) => string; size: number[]; anchor: string;
    }; extData: (_index: any, feat: { properties: any; }) => any;
  }) => void;
} = null;

let infoWindow: {
  getIsOpen(): any;
  setContent: (arg0: string) => void; open: (arg0: {
    clearMap: () => unknown; setCenter: (markersPosition: any[], arg1: boolean, arg2: number) => unknown; setFitView: (polygons: any, arg1: boolean) => unknown; setLimitBounds: (bounds: any) => unknown; getCenter: any; addControl: (arg0: any) => void; add: (arg0: any) => void; remove: (arg0: any) => void; on: (arg0: string, arg1: (e: {
      target: any; pixel: any; type: any; lnglat: {
        lng: any // 设置安全密钥
        ; lat: any;
      };
    }) => void) => void; setZoom: (arg0: number) => void;
  }, arg1: any) => void; getIsopen: () => any; close: () => void;
} = null;

var geo: null = null;
var aqiGeo: null = null;

var hazardGeo: null = null;
var hazardTopGeo: null = null;

// let windData: { data: any[]; }[]=null;

var disProvince: { destroy: () => void; setMap: (arg0: { clearMap(): unknown; setCenter(markersPosition: any[], arg1: boolean, arg2: number): unknown; setFitView(polygons: any, arg1: boolean): unknown; setLimitBounds(bounds: any): unknown; getCenter: any; addControl: (arg0: any) => void; add: (arg0: any) => void; remove: (arg0: any) => void; on: (arg0: string, arg1: (e: { data: any; target: any; pixel: any; type: any; lnglat: { lng: any; lat: any; }; }) => void) => void; setZoom: (arg0: number) => void; }) => void; } = null;

var draw_adcode = "100000";

var ranks = ["error", "优", "良好", "轻度污染", "中度污染", "重度污染"]
// var colors=["#000000","#84c77e","#c0dd83","#f8ed84","#f3956e","#e65d5b"]
onMounted(() => {
  initMap();
});

function object2Geojson(data: Array<MapGeo>) {
  var features = new Array();
  var featureCollection = { "type": "FeatureCollection", "features": features };

  for (let i = 0; i < data.length; i++) {
    var feature = { "type": "Feature", "properties": {}, "geometry": {}, };
    var geometry = { "type": "Point", "coordinates": new Array() };
    geometry.coordinates = [data[i].LON, data[i].LAT];
    feature.properties = data[i];
    feature.geometry = geometry;
    features.push(feature);
  }
  featureCollection.features = features;
  return featureCollection;
}

function object2Geojson2(data: Array<Hazard>) {
  var features = new Array();
  var featureCollection = { "type": "FeatureCollection", "features": features };

  for (let i = 0; i < data.length; i++) {
    var feature = { "type": "Feature", "properties": {}, "geometry": {}, };
    var geometry = { "type": "Point", "coordinates": new Array() };
    geometry.coordinates = [data[i].longitude, data[i].latitude];
    feature.properties = data[i];
    feature.geometry = geometry;
    features.push(feature);
  }
  featureCollection.features = features;
  return featureCollection;
}

function object2Geojson3(data: Array<MapGeo>) {
  var features = new Array();
  var featureCollection = { "type": "FeatureCollection", "features": features };

  for (let i = 0; i < data.length; i+=17) {
    var feature = { "type": "Feature", "properties": {}, "geometry": {}, };
    var geometry = { "type": "Point", "coordinates": new Array() };
    geometry.coordinates = [data[i].LON, data[i].LAT];
    feature.properties = data[i];
    feature.geometry = geometry;
    features.push(feature);
  }
  featureCollection.features = features;
  return featureCollection;
}

interface MapGeoRes{
  data: Array<MapGeo>;
}

async function getMapGeo() {
  await get<MapGeoRes>("/api/vis/getVisData/").then((res) => {
    
    geo = new Loca.GeoJSONSource({
      data: object2Geojson(res.data.data),
    });
    aqiGeo = new Loca.GeoJSONSource({
      data: object2Geojson3(<Array<MapGeo>>res.data.data),
    });
    InitHeatMapTem();
    InitHeatMapWater();
    InitAqi();
  });
}

async function getPointInfo() {
  await get<Point>("/api/vis/getPointInfo/", { LON: pos_info.lng, LAT: pos_info.lat }).then((res) => {
    pos_info.weatherInfo = res.data;
  });
}

async function getProInfo() {
  await get<ProInfo>("/api/getProInfo/", { proName: pos_info.provinceName }).then((res) => {
    pos_info.geoInfo = res.data.geography;
  });
};

function getHazardGeo() {
  get("/api/getHazard/").then((res) => {
    hazardGeo = new Loca.GeoJSONSource({
      data: object2Geojson2(<Array<Hazard>>res.data.data),
    });
    get("/api/getHazardTop/").then((res) => {
      hazardTopGeo = new Loca.GeoJSONSource({
        data: object2Geojson2(<Array<Hazard>>res.data.data),
      });
      InitHazard();
    });
  });
};

function initMap() {
  AMapLoader.load({
    key: "671116f417c14e708dd09edf8d4ab63a",
    version: "2.0",
    Loca: {                // 是否加载 Loca， 缺省不加载
      version: "2.0.0",  // Loca 版本，缺省 1.3.2
    },
    plugins: [
      "AMap.Scale",
      "AMap.ToolBar",
      "AMap.MapType",
      "AMap.DistrictSearch",
      "AMap.Geocoder",
      'AMap.PlaceSearch',
      'AMap.Autocomplete',
    ],
  })
    .then((AMap) => {
      // 初始化地图
      AAMap = AMap;
      map = new AMap.Map("mapContainer", {
        viewMode: "2D", // 是否为3D地图模式
        // zoom: 4.8, // 初始化地图级别
        // center: [105,36], // 初始化地图中心点位置
        zoom: 4.8, // 初始化地图级别
        center: [103, 36], // 初始化地图中心点位置
        // mapStyle: 'amap://styles/dark',
        // showLabel: true,
        // features: ['bg', 'road', 'building', 'point'],
        // layers: [new AMap.TileLayer(), new AMap.TileLayer.Satellite()],
      });
      // map.setLimitBounds(new AMap.Bounds([50,60],[150,0]));
      loca = new Loca.Container({
        map: map
      });
      //卫星图层
      sate = new AMap.TileLayer.Satellite({ zIndex: 1 });
      // 天地图图层
      wms = new AMap.TileLayer.WMTS({
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

      // geo = new Loca.GeoJSONSource({
      //   url: 'https://a.amap.com/Loca/static/loca-v2/demos/mock_data/traffic.json',
      // });


      map.addControl(new AMap.Scale({ position: 'LB' }));
      map.addControl(new AMap.ToolBar({ liteStyle: true, position: 'LT' }));
      map.add(wms);
      // map.add(sate);
      map.add(disCountry);
      pos_info.searcher = new AMap.DistrictSearch(pos_info.opts);
      pos_info.geoCoder = new AMap.Geocoder();
      infoWindow = new AAMap.InfoWindow({
        content: "",  //传入 dom 对象，或者 html 字符串
      });
      handlerMapClick();
      getMapGeo();
      getHazardGeo();
      // markPoints();
      // InitEarthQuake();
      // InitHeatMapTem();
      // InitHeatMapWater();
      // InitAqi();
      // InitHazard();
    })
    .catch((e) => {
      console.log(e);
    });
}

function drawBounds() {
  if (pos_info.provinceCode != draw_adcode) {
    draw_adcode = pos_info.provinceCode;
    disProvince && disProvince.setMap(null);
    disProvince = new AAMap.DistrictLayer.Province({
      zIndex: 100,
      adcode: [pos_info.provinceCode],
      depth: 0,
      styles: {
        // 'fill': 'linear-gradient(to right top, rgba(26, 79, 158, 1),rgb(243, 179, 179, 1))',
        'fill': '',
        'province-stroke': 'purple',
        'city-stroke': 'white', // 中国地级市边界
        'county-stroke': 'rgba(255,255,255,0.5)' // 中国区县边界
      }
    });
    disProvince.setMap(map);
  }
}

//点击区域触发事件
async function handlerMapClick() {
  map.on("click", (e: { pixel: any; lnglat: { lng: any; lat: any } }) => {
    // 点击坐标
    const markersPosition = [e.lnglat.lng, e.lnglat.lat];
    pos_info.pixel = e.pixel.toArray();
    pos_info.lng = markersPosition[0].toFixed(2);
    pos_info.lat = markersPosition[1].toFixed(2);
    // 根据坐标获取位置信息
    pos_info.geoCoder.getAddress(
      markersPosition,
      async (status: string, result: { regeocode: { addressComponent: any } }) => {
        if (status === "complete" && result.regeocode) { //判断是否为中国境内
          let addressComponent = result.regeocode.addressComponent;
          pos_info.adcode = addressComponent.adcode;
          pos_info.provinceName = addressComponent.province;
          pos_info.cityName = addressComponent.city;
          pos_info.districtName = addressComponent.district;
          pos_info.provinceCode = addressComponent.adcode.substr(0, 2) + "0000";
          if (pos_info.cityName != "") {
            if (pos_info.districtName != "") {
              pos_info.name = '当前位置：' + pos_info.provinceName + "/" + pos_info.cityName + "/" + pos_info.districtName;
            } else {
              pos_info.name = '当前位置：' + pos_info.provinceCode + "/" + pos_info.cityName;
            }
          } else {
            pos_info.name = '当前位置：' + pos_info.provinceName;
          }
          // let cityId = parseInt(adcode.substr(0, 4) + '00')
          // let areaId = adcode
          if (pos_info.provinceCode != "100000") {  //国内各省，高亮区域并跟随中心
            await showInfoWindow();
          } else {                                  //刚刚好是中国，取消高亮并重设中心
            pos_info.provinceName = "中国";
            map.remove(pos_info.polygons); //清除结果
            map.setCenter([105, 36], false, 30);
            map.setZoom(4.8);
          }
        } else {  //非中国境内，设为中国
          pos_info.adcode = "100000";
          pos_info.provinceName = "中国";
          pos_info.cityName = "";
          pos_info.districtName = "";
          pos_info.provinceCode = "100000";
          map.remove(pos_info.polygons); //清除结果
          map.setCenter([105, 36], false, 30);
          map.setZoom(4.8);
        }
      }
    );
  });
}

async function showInfoWindow() {
  let content = [
    `<div><span style="font-size: 13px;">${pos_info.lat}°N ${pos_info.lng}°E</span>`,
  ];

  if (buttonActive.d) {  //地形图层
    drawBounds();
    await getProInfo();
    content.push(
      `<span style="font-size: 18px;"><b>${pos_info.name}</b></span>`,
      `<span style="font-size: 14px;">${pos_info.provinceName}地理概况：${pos_info.geoInfo}</span>`,
    );
    content.push("</div>");
    infoWindow.setContent(content.join('<br>'));
    // 打开信息窗体
    let dd = map.getCenter()
    dd.lat = pos_info.lat
    dd.lng = pos_info.lng
    infoWindow.open(map, dd);
  }
  else if (buttonActive.e) {
    var feat = scatter.queryFeature(pos_info.pixel);
    if (feat) {
      content.push(
        `<span style="font-size: 24px;"><b>${feat.properties.type} ${feat.properties.level}</b></span>`,
        `<span style="font-size: 13px;">${feat.properties.place}</span>`,
      );
      content.push("</div>");
      infoWindow.setContent(content.join('<br>'));
      // 打开信息窗体
      let dd = map.getCenter()
      dd.lat = pos_info.lat
      dd.lng = pos_info.lng
      infoWindow.open(map, dd);
    }
    else {
      if (infoWindow.getIsOpen()) infoWindow.close();
    }
  }
  else if (buttonActive.a || buttonActive.b || buttonActive.f) {
    await getPointInfo();
    if (buttonActive.a) {
      content.push(
        `<span style="font-size: 24px;"><b>${pos_info.weatherInfo.temp}℃</b></span>`,
        `<span style="font-size: 13px;">气温</span>`,
      );
    }
    else if (buttonActive.b) {
      content.push(
        `<span style="font-size: 24px;"><b>${pos_info.weatherInfo.precip}mm</b></span>`,
        `<span style="font-size: 13px;">降水量</span>`,
      );
    }
    else if (buttonActive.f) {
      var type = Math.floor(pos_info.weatherInfo.aqi / 50) + 1;
      if (type > 5) type = 5;
      content.push(
        `<span style="font-size: 24px;"><b>${pos_info.weatherInfo.aqi}</b></span>`,
        `<span style="font-size: 13px;">AQI  空气质量：${ranks[type]}</span>`,
      );
    }
    // else if(buttonActive.c) {
    // const wind = getWind(pos_info.lng, pos_info.lat);
    // content.push(`风场：u${wind.u},v${wind.v},speed${wind.speed}，angle${wind.angle}，direction${wind.direction}`);
    // }
    content.push("</div>");
    infoWindow.setContent(content.join('<br>'));
    // 打开信息窗体
    let dd = map.getCenter()
    dd.lat = pos_info.lat
    dd.lng = pos_info.lng
    infoWindow.open(map, dd);
  }
}


function clickA() {
  // if(infoWindow.getIsOpen()) showInfoWindow();
  // if(buttonActive.B) {
  //   disProvince && disProvince.setMap(null);
  //   draw_adcode = "100000";
  // }
  // buttonActive.A = true;
  // buttonActive.B = false;
  // buttonActive.C = false;
  // map.remove(wms);
  // map.remove(sate);
  buttonActive.A = true;
  buttonActive.B = false;
  buttonActive.C = false;
  map.remove(wms);
  map.remove(sate);
}

function clickB() {
  buttonActive.A = false;
  buttonActive.B = true;
  buttonActive.C = false;
  map.remove(sate);
  map.add(wms);
}

function clickC() {
  buttonActive.A = false;
  buttonActive.B = false;
  buttonActive.C = true;
  map.remove(wms);
  map.add(sate);
}

function clicka() {
  buttonActive.a = !buttonActive.a;
  if (buttonActive.a) {
    if (buttonActive.b) clickb();
    else if (buttonActive.c) clickc();
    else if (buttonActive.d) clickd();
    else if (buttonActive.e) clicke();
    else if (buttonActive.f) clickf();
    if (infoWindow.getIsOpen()) showInfoWindow();
    heatmapTem.setLoca(loca);
  }
  else {
    heatmapTem.remove();
  }
}

function clickb() {
  buttonActive.b = !buttonActive.b;
  if (buttonActive.b) {
    if (buttonActive.a) clicka();
    else if (buttonActive.c) clickc();
    else if (buttonActive.d) clickd();
    else if (buttonActive.e) clicke();
    else if (buttonActive.f) clickf();
    if (infoWindow.getIsOpen()) showInfoWindow();
    heatmapWater.setLoca(loca);
  }
  else {
    heatmapWater.remove();
  }
}

function clickc() {
  buttonActive.c = !buttonActive.c;
  if (buttonActive.c) {
    if (buttonActive.b) clickb();
    else if (buttonActive.a) clicka();
    else if (buttonActive.d) clickd();
    else if (buttonActive.e) clicke();
    else if (buttonActive.f) clickf();
    if (infoWindow.getIsOpen()) infoWindow.close();
    showWind();
  }
  else {
    windLayer.remove();
  }
}

function clickd() {
  buttonActive.d = !buttonActive.d;
  if (buttonActive.d) {
    if (buttonActive.b) clickb();
    else if (buttonActive.c) clickc();
    else if (buttonActive.a) clicka();
    else if (buttonActive.e) clicke();
    else if (buttonActive.f) clickf();
    if (infoWindow.getIsOpen()) showInfoWindow();
  }
  else {
    disProvince && disProvince.setMap(null);
    draw_adcode = "100000";
  }
}

function clicke() {
  buttonActive.e = !buttonActive.e;
  if (buttonActive.e) {
    if (buttonActive.b) clickb();
    else if (buttonActive.c) clickc();
    else if (buttonActive.d) clickd();
    else if (buttonActive.a) clicka();
    else if (buttonActive.f) clickf();
    scatter.setLoca(loca);
    breath.setLoca(loca);
    if (infoWindow.getIsOpen()) showInfoWindow();
    // loca.animate.start();
  }
  else {
    scatter.remove();
    breath.remove();
  }
}

function clickf() {
  buttonActive.f = !buttonActive.f;
  if (buttonActive.f) {
    if (buttonActive.b) clickb();
    else if (buttonActive.c) clickc();
    else if (buttonActive.d) clickd();
    else if (buttonActive.e) clicke();
    else if (buttonActive.a) clicka();
    aqiLayer.setLoca(loca);
    if (infoWindow.getIsOpen()) showInfoWindow();
  }
  else {
    aqiLayer.remove();
    // loca.remove(aqiLayer);
  }
}

//显示风场图层
function showWind() {
  import('amap-wind').then(({ WindLayer }) => {
    fetch('https://sakitam.oss-cn-beijing.aliyuncs.com/codepen/wind-layer/json/wind.json')
      .then(res => res.json())
      .then(res => {
        // windData = res;
        windLayer = new WindLayer(res, {
          windOptions: {
            // colorScale: scale,
            velocityScale: 1 / 50,
            paths: 1000,
            // eslint-disable-next-line no-unused-vars
            maxAge: 10,
            frameRate: 2,
            colorScale: [
              "rgb(36,104, 180)",
              "rgb(60,157, 194)",
              "rgb(128,205,193 )",
              "rgb(151,218,168 )",
              "rgb(198,231,181)",
              "rgb(238,247,217)",
              "rgb(255,238,159)",
              "rgb(252,217,125)",
              "rgb(255,182,100)",
              "rgb(252,150,75)",
              "rgb(250,112,52)",
              "rgb(245,64,32)",
              "rgb(237,45,28)",
              "rgb(220,24,32)",
              "rgb(180,0,35)"
            ],
            lineWidth: 5,
          },
          zIndex: 20,
        });

        windLayer.appendTo(map);
      });
  });
}

// function getWind(longitude: number, latitude: number) {
//   // const jIndex = Math.floor(90.5 - latitude);
//   // // const jIndex = Math.floor(latitude + 90.5);
//   // // const iIndex = Math.floor(180.5 - longitude);
//   // const iIndex = Math.floor(longitude + 180.5);
//   // const index = jIndex * 360 + iIndex;
//   const ii = Math.floor(longitude + 180.5); // calculate longitude index in wrapped range [0, 360)
//       // const j = Math.floor(90.5 - latitude); // calculate latitude index in direction +90 to -90
//       const j = Math.floor(90.5 + latitude); // calculate latitude index in direction +90 to -90
//     const index = j * 360 + ii;
//   const uSpeed = windData[0].data[index];
//   const vSpeed = windData[1].data[index];
//   const speed = Math.sqrt(uSpeed ** 2 + vSpeed ** 2);
//   var angle = Math.atan2(uSpeed, vSpeed) * (180 / Math.PI);
//   // 转换为正角度
//   angle = angle >= 0 ? angle : 360 + angle;
//   // const directions = ['北', '东北', '东', '东南', '南', '西南', '西', '西北'];
//   const directions = ['东','东北', '北' ,'西北','西', '西南', '南', '东南'];
//   const i = (Math.round((angle % 360) / 45))%8;
//   const direction = directions[i];
//   return {u:uSpeed, v:vSpeed, speed:speed, angle: angle, direction: direction};
// }

//初始化气温热力图层
function InitHeatMapTem() {
  // var heatmapTemData = new Loca.GeoJSONSource({
  //       url: 'https://a.amap.com/Loca/static/loca-v2/demos/mock_data/traffic.json',
  //   });
  heatmapTem = new Loca.HeatMapLayer({
    // loca,
    zIndex: 10,
    opacity: 1,
    visible: true,
    zooms: [2, 22],
  });

  heatmapTem.setSource(geo, {
    // radius: 200000,
    radius: 80000,
    unit: 'meter',
    gradient: {
      0.1: '#2A85B8',
      0.2: '#16B0A9',
      0.3: '#29CF6F',
      0.4: '#5CE182',
      0.5: '#7DF675',
      0.6: '#FFF100',
      0.7: '#FAA53F',
      1: '#D04343',
    },
    value: function (_index: any, feature: { properties: { temp: any; mom: string | any[]; }; }) {
      return feature.properties.temp;
    },
  });
}

//初始化降水热力图层
function InitHeatMapWater() {
  // var heatmapWaterData = new Loca.GeoJSONSource({
  //       url: 'https://a.amap.com/Loca/static/loca-v2/demos/mock_data/traffic.json',
  //   });
  heatmapWater = new Loca.HeatMapLayer({
    // loca,
    zIndex: 10,
    opacity: 1,
    visible: true,
    zooms: [2, 22],
  });

  heatmapWater.setSource(geo, {
    radius: 70000,
    unit: 'meter',
    height: 500000,

    gradient: {
      0.1: '#EAF3F7',
      0.2: '#98D5EE',
      0.3: '#59C7F6',
      0.4: '#60B1F4',
      0.5: '#4E92CE',
      0.6: '#3185CF',
      0.7: '#0A69BC',
      1: '#083D99',
    },
    value: function (_index: any, feature: { properties: { precip: any; mom: string | any[]; }; }) {
      return feature.properties.precip;
    },
    heightBezier: [0, .53, .37, .98],
  });

  //   loca.add(heatmapWater);

}

//初始化灾害图层
function InitHazard() {
  scatter = new Loca.ScatterLayer({
    // loca,
    zIndex: 15,
    opacity: 1,
    visible: true,
    zooms: [2, 22],
  });

  scatter.setSource(hazardGeo, {
    unit: 'px',
    size: [20, 20],
    texture: 'https://a.amap.com/Loca/static/loca-v2/demos/images/blue.png',
    borderWidth: 0,
  });

  breath = new Loca.ScatterLayer({
    zIndex: 15,
  });
  breath.setSource(hazardTopGeo);
  breath.setStyle({
    unit: 'px',
    size: [50, 50],
    texture: 'https://a.amap.com/Loca/static/loca-v2/demos/images/breath_red.png',
    animate: true,
    duration: 1000,
  });
  loca.animate.start();
}

//初始化空气质量图层
function InitAqi() {
  aqiLayer = new Loca.LabelsLayer({
    zindex: 100,
    fitView: true,
    eventSupport: false,  // 图层事件支持，LabelsLayer 默认开启
    collision: false  // 是否开启文字自动避让
  });
  aqiLayer.setSource(aqiGeo, {
    icon: {
      type: 'image',
      image: function (_index: any, feature: { properties: { aqi: any; mom: string | any[]; }; }) {
        var type: number = Math.floor(feature.properties.aqi / 50) + 1;
        if (type > 5) type = 5;
        return getAssetsFileAQI(type + ".png");
      },
      size: [30, 30],
      anchor: 'center',
    },
    // text: {
    //     // 每项配置都可使用回调函数来动态配置
    //     content: function (_index: any, feature: { properties: { aqi: any; mom: string | any[]; }; }) {
    //         return "AQI:" + feature.properties.aqi.toString();
    //         },
    //     style: {
    //         fontSize: 14,
    //         fontWeight: 'normal',
    //         fillColor: function (_index: any, feature: { properties: { aqi: any; mom: string | any[]; }; }) {
    //           var type:number = Math.floor(feature.properties.aqi / 50) + 1;
    //           if(type>5) type=5;
    //           return colors[type];
    //         },
    //         strokeColor: '#000',
    //         strokeWidth: 1,
    //     },
    //     direction: 'bottom',
    // },
    extData: function (_index: any, feature: { properties: { adcode: any; aqi: any; mom: string | any[]; }; }) {
      var type: number = Math.floor(feature.properties.aqi / 50) + 1;
      if (type > 5) type = 5;
      return { type: type, adcode: feature.properties.adcode };
    },

  });

}
</script>

<style scoped>
#mapContainer {
  width: 100%;
  height: 100%;

}

.layerbtns[data-iconsize="0"] {
  margin-right: 11px;
  display: grid;
  justify-items: end;
  align-items: start;
  font-size: 6px;
}

.btnDiv {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin: 0.3em 0 0.3em 0.4em;
}

.layerbtn {
  height: 40px;
  border: 1px solid #3924a7;
  border-radius: 30px;
  background-color: rgba(45, 45, 45, 0.2);
  display: flex;
  margin: 0.3em 0 0.3em 0.4em;
  position: relative;
}

.layerbtn2 {
  height: 35px;
  border: 1px solid #3924a7;
  border-radius: 30px;
  background-color: rgba(45, 45, 45, 0.2);
  display: flex;
  margin: 0.3em 0 0.3em 0.4em;
  position: relative;
}

.unselected {
  height: 35px;
  border: 1px solid #3924a7;
  border-radius: 30px;
  background-color: rgba(45, 45, 45, 0.1);
  display: flex;
  width: 105px;
  margin: 0.3em 0 0.3em 0.4em;
  position: relative;
}

.selected {
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  height: 35px;
  border: 1px solid #3924a7;
  border-radius: 30px;
  /* background-color: rgba(8, 122, 0, 0.5); */
  background: linear-gradient(to right top, rgba(26, 79, 158, 0.5), rgb(243, 179, 179, 0.5));
  display: flex;
  width: 105px;
  margin: 0.3em 0 0.3em 0.4em;
  position: relative;
}

.btnIcona {
  width: 2.4em;
  height: 2.4em;
  border-radius: 3em;
  box-shadow: 0 0 4px 0 black;
  background-image: url("../../assets/img/tem.png");
  background-size: 100% 100%;
  /*按比例缩放*/
  position: absolute;
  right: 0;
}

.btnIconb {
  width: 2.4em;
  height: 2.4em;
  border-radius: 3em;
  box-shadow: 0 0 4px 0 black;
  background-image: url("../../assets/img/water.png");
  background-size: 100% 100%;
  /*按比例缩放*/
  position: absolute;
  right: 0;
}

.btnIcond {
  width: 2.4em;
  height: 2.4em;
  border-radius: 3em;
  box-shadow: 0 0 4px 0 black;
  background-image: url("../../assets/img/geo.png");
  background-size: 100% 100%;
  /*按比例缩放*/
  position: absolute;
  right: 0;
}

.btnIconf {
  width: 2.4em;
  height: 2.4em;
  border-radius: 3em;
  box-shadow: 0 0 4px 0 black;
  background-image: url("../../assets/img/AQI.png");
  background-size: 100% 100%;
  /*按比例缩放*/
  position: absolute;
  right: 0;
}

.btnIcone {
  width: 2.4em;
  height: 2.4em;
  border-radius: 3em;
  box-shadow: 0 0 4px 0 black;
  background-image: url("../../assets/img/earthquake.png");
  background-size: 100% 100%;
  /*按比例缩放*/
  position: absolute;
  right: 0;
}

.btnIconc {
  width: 2.4em;
  height: 2.4em;
  border-radius: 3em;
  box-shadow: 0 0 4px 0 black;
  background-image: url("../../assets/img/wind.png");
  background-size: 100% 100%;
  /*按比例缩放*/
  position: absolute;
  right: 0;
}

.btnName {
  position: absolute;
  left: 10%;
  color: black;
  font-weight: 600;
}

.btnName2 {
  position: absolute;
  left: 20%;
  color: black;
  font-weight: 600;
}


:deep(.amap-info-outer) {
  /* background:linear-gradient(to right top, rgba(26, 79, 158, 0.9),rgb(243, 179, 179, 0.9));
    border: 1px solid #b9b9b9; */
  border-radius: 10px;
  /* box-shadow: 0 3px 14px rgba(0,0,0,0.4); */
  padding: 8px;
  padding-left: 15px;
  padding-right: 15px;
  min-width: 180px;
}

/* :deep(.amap-info-sharp) {
    border: 1px solid rgb(243, 179, 179, 0.6);
}
:deep(.amap-info-close) {
  color: rgb(61, 61, 61);
} */
</style>