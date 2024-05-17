<template>
  <div id="mapContainer">
    <div class="input-card" style="position: relative; z-index: 100; top:30%; width: 100px;">
      <!-- <input id='tipinput' type="text"> -->
      <div class="layerbtns">
        <el-button :class="{ 'selected': buttonActive.A, 'unselected': !buttonActive.A }"  :active="buttonActive.A" @click="clickA">
          <div class="btnDiv">
            <div class="btnName2">标准图层</div>
          </div>
        </el-button>
        <el-button :class="{ 'selected': buttonActive.B, 'unselected': !buttonActive.B }"  :active="buttonActive.B" @click="clickB">
          <div class="btnDiv">
            <div class="btnName2">地形图层</div>
          </div>
        </el-button>
        <el-button :class="{ 'selected': buttonActive.C, 'unselected': !buttonActive.C }"  :active="buttonActive.C" @click="clickC">
          <div class="btnDiv">
            <div class="btnName2">卫星图层</div>
          </div>
        </el-button>
      </div>
      <br/>
      <br/>
      <div class="layerbtns">
        <el-button width="600px" :class="{ 'selected': buttonActive.a, 'unselected': !buttonActive.a }"  :active="buttonActive.a" @click="clicka">
          <div class="btnDiv">
            <div class="btnName">气温</div>
            <div class="btnIcona"></div>
          </div>
        </el-button>
        <el-button :class="{ 'selected': buttonActive.b, 'unselected': !buttonActive.b }"  :active="buttonActive.b" @click="clickb">
          <div class="btnDiv">
            <div class="btnName">降水</div>
            <div class="btnIconb"></div>
          </div>
        </el-button>
        <el-button width="200px" :class="{ 'selected': buttonActive.f, 'unselected': !buttonActive.f }"  :active="buttonActive.f" @click="clickf">
          <div class="btnDiv">
            <div class="btnName">空气质量</div>
            <div class="btnIconf"></div>
          </div>
        </el-button>
        <el-button :class="{ 'selected': buttonActive.e, 'unselected': !buttonActive.e }"  :active="buttonActive.e" @click="clicke">
          <div class="btnDiv">
            <div class="btnName">灾害</div>
            <div class="btnIcone"></div>
          </div>
        </el-button>
        <el-button :class="{ 'selected': buttonActive.c, 'unselected': !buttonActive.c }"  :active="buttonActive.c" @click="clickc">
          <div class="btnDiv">
            <div class="btnName">风场</div>
            <div class="btnIcond"></div>
          </div>
        </el-button>
      </div>
    </div>
  </div>
 
</template>

<script setup lang="ts">
import { onMounted, reactive } from "vue";
import AMapLoader from "@amap/amap-jsapi-loader";
import { getAssetsFile } from '@/utils/pub-use'
import AMapWind from "amap-wind";
import { get } from "@/api/index";
import { GeoJsonOri } from "@/types/weather";

// 设置安全密钥
(window as any)._AMapSecurityConfig = {
  securityJsCode: "ff942cdc56a565fb2e5d5b5e6a3481ae",
};

//高亮区域信息
const pos_info = reactive({
  lng: 0,               //所在经度
  lat: 0,               //所在纬度
  adcode: "100000",     //所在行政区划编码
  provinceCode:"",      //所在省编码
  provinceName: "中国", //所在省名称
  cityName: "",         //所在市名称
  districtName:"",      //所在县名称
  name:"",              //拼接名称
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

//灾害标记信息
let hazardMarkData = reactive([
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

const buttonActive = reactive({
  A:false,
  B:true,
  C:false,
  a:false,
  b:false,
  c:false,
  d:false,
  e:false,
  f:false,
});

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
      target: any;
      pixel: any;
      type: any; lnglat: { lng: any; lat: any } 
    }) => void
  ) => void;
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

declare let Loca:any

let loca: {
[x: string]: any;
remove(pl: { setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: { key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number; yoyo: boolean; repeat: number; }) => void; }): unknown; add: (arg0: any) => void; 
}=null;

let heatmapTem: {
remove(): unknown;
setLoca(loca: { remove(pl: { setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: { key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number; yoyo: boolean; repeat: number; }) => void; }): unknown; add: (arg0: any) => void; }): unknown;
destroy(): unknown; setSource: any; addAnimate: any; queryFeature?: any; setStyle?: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; 
} = null;

let heatmapWater: {
remove(): unknown;
setLoca(loca: { remove(pl: { setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: { key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number; yoyo: boolean; repeat: number; }) => void; }): unknown; add: (arg0: any) => void; }): unknown;
destroy(): unknown; setSource: any; addAnimate: any; queryFeature?: any; setStyle?: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; 
} = null;

let windLayer: AMapWind = null;

let scatter: { setLoca: (arg0: { [x: string]: any; remove(pl: { setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: { key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number; yoyo: boolean; repeat: number; }) => void; }): unknown; add: (arg0: any) => void; }) => void; remove: () => void; setSource: (arg0: any, arg1: { unit: string; size: number[]; texture: string; borderWidth: number; }) => void; } = null;

let breath: { setLoca: (arg0: { [x: string]: any; remove(pl: { setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: { key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number; yoyo: boolean; repeat: number; }) => void; }): unknown; add: (arg0: any) => void; }) => void; remove: () => void; setSource: (arg0: any) => void; setStyle: (arg0: { unit: string; size: number[]; texture: string; animate: boolean; duration: number; }) => void; } = null;

let wms: null = null;

let sate: null = null;

let layer: {
remove(): unknown;
queryFeature(arg0: any): unknown;
show(): unknown;
addAnimate(arg0: { key: string; value: number[]; easing: string; transform: number; random: boolean; delay: number; }): unknown;
setStyle(arg0: { unit: string; icon: (index: any, feature: any) => any; iconSize: number[]; offset: number[]; rotation: number; }): unknown;
setSource(geo: any): unknown; setLoca: (arg0: { [x: string]: any; remove(pl: { setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: { key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number; yoyo: boolean; repeat: number; }) => void; }): unknown; add: (arg0: any) => void; }) => void; 
}=null;

let pl: { setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: { key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number; yoyo: boolean; repeat: number; }) => void; } = null;

// let dat: {
// removeLayer(pl: { setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: { key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number; yoyo: boolean; repeat: number; }) => void; }): unknown; addLayer: (arg0: any, arg1: string) => void; 
// } = null;

// 使用defineEmits注册一个自定义事件
const emit = defineEmits(["getValue"])
 
// 点击事件触发emit，去调用我们注册的自定义事件getValue,并传递value参数至父组件
const transValue = () => {
  emit("getValue", pos_info.provinceName);
}

onMounted(() => {
  // getHazardInfo();
  initMap();
});

const getHazardInfo = async () => {
  get<Array<any>>("/api/getHazard/").then((res) => {
    hazardMarkData = res.data;
    // HazardInfo = res.data;
    // console.log("222", hazardMarkData);
  });
}

function initMap() {
  AMapLoader.load({
    key: "671116f417c14e708dd09edf8d4ab63a",
    version: "2.0",
    Loca:{                // 是否加载 Loca， 缺省不加载
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
      sate = new AMap.TileLayer.Satellite({zIndex:1});
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
     
      
      map.addControl(new AMap.Scale({position: 'LB'}));
      map.addControl(new AMap.ToolBar({ liteStyle: true, position: 'LT'}));
      map.add(wms);
      // map.add(sate);
      map.add(disCountry);
      pos_info.searcher = new AMap.DistrictSearch(pos_info.opts);
      pos_info.geoCoder = new AMap.Geocoder();
      InitAqi();
      handlerMapClick();
      // markPoints();
      InitEarthQuake();
      InitHeatMapTem();
      InitHeatMapWater();
      InitHazard();
    })
    .catch((e) => {
      console.log(e);
    });
}

//高亮区域
function drawBounds() {
  var step = 15;
  //行政区查询
  pos_info.searcher.search(
    pos_info.provinceCode,
    function (_status: any, result: { districtList: { boundaries: any }[] }) {
      map.remove(pos_info.polygons); //清除上次结果
      pos_info.polygons = [];
      var bounds = result.districtList[0].boundaries;
      if (bounds) {
        var bounds2 = new Array();
        if (pos_info.provinceCode != '710000' && pos_info.provinceCode != '460000') {
          bounds2.push(bounds.pop());
          bounds = bounds2;
        }
        if(pos_info.provinceCode == '150000') {
          step=3;
        }
        else {
          step=10;
        }
        for (var i = 0, l = bounds.length; i < l; i++) {
          var bound = bounds[i];
          var bound2 = new Array();
          for (var j = 0, m = bound.length; j < m; j=j+step) {
            bound2.push(bound[j]);
          }
          const polygon = new AAMap.Polygon({
            strokeWeight: 1,
            path: bound2,
            fillOpacity: 0.4,
            fillColor: "#80d8ff",
            strokeColor: "#0091ea",
          });
          map.add(polygon);
          pos_info.polygons.push(polygon);
        }
      }

      map.add(pos_info.polygons);
      map.setZoom(5);
    }
  );
}

//点击区域触发事件
function handlerMapClick() {
  map.on("click", (e: { lnglat: { lng: any; lat: any } }) => {
    // 点击坐标
    const markersPosition = [e.lnglat.lng, e.lnglat.lat];
    pos_info.lng = markersPosition[0];
    pos_info.lat = markersPosition[1];
    // 根据坐标获取位置信息
    pos_info.geoCoder.getAddress(
      markersPosition,
      (status: string, result: { regeocode: { addressComponent: any } }) => {
        if (status === "complete" && result.regeocode) { //判断是否为中国境内
          let addressComponent = result.regeocode.addressComponent;
          //   let reg = /.+?(省|市|自治区|自治州|县|区)/g
          pos_info.adcode = addressComponent.adcode;
          pos_info.provinceName = addressComponent.province;
          pos_info.cityName = addressComponent.city;
          pos_info.districtName = addressComponent.district;
          pos_info.provinceCode = addressComponent.adcode.substr(0, 2) + "0000";
          if(pos_info.cityName != "") {
            if(pos_info.districtName != "") {
              pos_info.name = '当前位置：' + pos_info.districtName + "/" + pos_info.cityName + "/" + pos_info.provinceName;
            } else {
              pos_info.name = '当前位置：' + pos_info.cityName + "/" + pos_info.provinceName;
            }
          } else {
            pos_info.name = '当前位置：'+ pos_info.provinceName;
          }
          // console.log(pos_info.name);
          // console.log('经度：', pos_info.lng, ',经度：', pos_info.lat)
          // let cityId = parseInt(adcode.substr(0, 4) + '00')
          // let areaId = adcode
          if (pos_info.provinceCode != "100000") {  //国内各省，高亮区域并跟随中心
            //向父组件传省份名
            transValue();
            // pos_info.provinceName = pos_info.provinceName + "/中国";
            // drawBounds();
            // map.setCenter(markersPosition, false, 300);
            //显示标记弹出框
            let content = [
              `<div style='\'padding:0px' 0px = '' 4px; \'=''><b>${pos_info.name}</b>`,
              `经度：${pos_info.lng}`,
              `纬度：${pos_info.lat}`
              // `<img src=${item.img} alt="" style="width: 100px;height: 100px">`
            ];
            // 创建 infoWindow 实例	
            let infoWindow = new AAMap.InfoWindow({
              content: content.join("<br>")  //传入 dom 对象，或者 html 字符串
            });
            // 打开信息窗体
            let dd = map.getCenter()
            // dd.pos = [e.pos[0], e.pos[1]]
            dd.lat = pos_info.lat
            dd.lng = pos_info.lng
            infoWindow.open(map, dd);
          } else {                                  //刚刚好是中国，取消高亮并重设中心
            pos_info.provinceName = "中国";
            //向父组件传省份名
            transValue();
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
          //向父组件传省份名
          transValue();
          map.remove(pos_info.polygons); //清除结果
          map.setCenter([105, 36], false, 30);
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

function clickA() {
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
    if(buttonActive.b) clickb();
    else if(buttonActive.e) clicke();
    else if(buttonActive.f) clickf();
    clickB();
    heatmapTem.setLoca(loca);
  }
  else {
    heatmapTem.remove();
  }
}

function clickb() {
  buttonActive.b = !buttonActive.b;
  if (buttonActive.b) {
    if(buttonActive.a) clicka();
    else if(buttonActive.e) clicke();
    else if(buttonActive.f) clickf();
    clickB();
    heatmapWater.setLoca(loca);
  }
  else {
    heatmapWater.remove();
  }
}

function clickc() {
  buttonActive.c = !buttonActive.c;
  if (buttonActive.c) {
    showWind();
  }
  else {
    windLayer.remove();
  }
}

function clickd() {
  buttonActive.d = !buttonActive.d;
  if (buttonActive.d) {
    loca.add(pl);
  }
  else {
    loca.remove(pl);
  }
}

function clicke() {
  buttonActive.e = !buttonActive.e;
  if (buttonActive.e) {
    if(buttonActive.a) clicka();
    else if(buttonActive.b) clickb();
    else if(buttonActive.f) clickf();
    clickC();
    scatter.setLoca(loca);
    breath.setLoca(loca);
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
    if(buttonActive.a) clicka();
    else if(buttonActive.b) clickb();
    else if(buttonActive.e) clicke();
    clickB();
    layer.setLoca(loca);
  }
  else {
    layer.remove();
  }
}



//显示风场图层
function showWind() {
 import('amap-wind').then(({ WindLayer }) => {
  fetch('https://sakitam.oss-cn-beijing.aliyuncs.com/codepen/wind-layer/json/wind.json')
    .then(res => res.json())
    .then(res => {
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
          // colorScale: scale,
        },
        zIndex: 20,
      });

      windLayer.appendTo(map);
    });
  });
}

//初始化地震图层
function InitEarthQuake() {
  var geo = new Loca.GeoJSONSource({
    url: 'https://a.amap.com/Loca/static/loca-v2/demos/mock_data/earthquake.json',
  });

  // dat = new Loca.Dat();

  pl = new Loca.PointLayer({
      zIndex: 10,
      blend: 'lighter' //lighter normal
  });

  var colors = [
      '#F86615',
      '#F86615',
      '#F86615',
      '#F86615',
      '#D60352',
  ];

  pl.setSource(geo);
  pl.setStyle({
      radius: function(_i: any, feature: { properties: { level: string | number; }; }) {
          let level = +feature.properties.level;
          if (level < 7) {
              return level / 2;
          }
          return 8;
      },
      color: function(_i: any, feature: { properties: any; }) {
          let data = feature.properties;
          let ci = ~~(data.depth / 120 * colors.length) % colors.length;
          return colors[ci];
      },
      borderWidth: 0,
      blurRadius: -1,
      unit: 'px',
  });
  // loca.add(pl);

  pl.addAnimate({
    key: 'radius',
    value: [0, 1],
    duration: 500,
    easing: 'Linear',
    transform: 2000,
    random: true,
    delay: 8000,
    yoyo:true,
    repeat: 100000
  });
  // dat.addLayer(pl, '点图层');
}

// const getGeo = async () => {
//   get<any>("/api/getHazard/").then((res) => {
//     geo = res.data;
//     // geo = res.data;
//     // console.log("222", hazardMarkData);
//   });
// }

function object2Geojson(data:Array<GeoJsonOri>) {
    var features = new Array();
    var featureCollection = { "type": "FeatureCollection" ,"features": features};
 
	for (let i = 0; i < data.length; i++) {
        var feature = { "type": "Feature" ,"properties": {}, "geometry": {},};
        var geometry = { "type": "Point","coordinates":new Array()};
        geometry.coordinates = [data[i].LON, data[i].LAT];
        feature.properties = data[i];
        feature.geometry = geometry;
        features.push(feature);
	}
			
	featureCollection.features = features;
	return featureCollection;
}


//初始化气温热力图层
function InitHeatMapTem() {
    var heatmapTemData = new Loca.GeoJSONSource({
          url: 'https://a.amap.com/Loca/static/loca-v2/demos/mock_data/traffic.json',
      });

    // get("/api/vis/getTem2").then((res) => {
    //   var heatmapTemData = new Loca.GeoJSONSource({
    //     data:object2Geojson(<Array<GeoJsonOri>>res.data),
    //   });

      heatmapTem = new Loca.HeatMapLayer({
          // loca,
          zIndex: 10,
          opacity: 1,
          visible: true,
          zooms: [2, 22],
      });

      heatmapTem.setSource(heatmapTemData, {
          radius: 200000,
          unit: 'meter',
          //difference: true,
          //height: 500000,
          //radius: 35,
          //unit: 'px',
          //height: 100,
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
          value: function (_index: any, feature: { properties: { avg: any; mom: string | any[]; }; }) {
              return feature.properties.avg;
            //   var value = feature.properties.mom.slice(0, -1);
            //   return value + 10 * Math.random();
          },
          // min: -100,
          // max: 100,
        //   heightBezier: [0, .53, .37, .98],
      });

    //   loca.add(heatmapTem);
    // heatmapTem.setLoca(loca);
    
    //   map.on('complete', function () {
    //       heatmapTem.addAnimate({
    //           key: 'radius',
    //           value: [0, 1],
    //           //   duration: 2000,
    //           duration: 0,
    //           easing: 'BackOut',
    //           // 开启随机动画
    //           //   transform: 1000,
    //           transform: 0,
    //           random: true,
    //           //   delay: 1000,
    //           delay: 0,
    //       });
    //   });
	//   map.on('click', function (e) {
    //       var feat = heatmapTem.queryFeature(e.pixel.toArray());
    //       if(feat){
    //         map.clearMap();
    //         map.add(AAMap.Marker({
	// 		  position:feat.lnglat,
    //           anchor: 'bottom-center',
    //           content: '<div style="margin-bottom: 15px; border:1px solid #fff; border-radius: 4px;color: #fff; width: 150px; text-align: center;">热力值: '+ feat.value.toFixed(2) +'</div>'
    //         }));
    //       }
    //   });
    //   var timerId = setTimeout(() => {
    //     loca.add(heatmapTem);
    //     clearTimeout(timerId); // 取消定时执行
    //    }, 1000); // 延迟2秒后修改message
    // });
      
}

//初始化降水热力图层
function InitHeatMapWater() {
    var heatmapWaterData = new Loca.GeoJSONSource({
          url: 'https://a.amap.com/Loca/static/loca-v2/demos/mock_data/traffic.json',
      });

    // get("/api/vis/getVisData").then((res) => {
    //   var heatmapTemData = new Loca.GeoJSONSource({
    //     data:object2Geojson(<Array<GeoJsonOri>>res.data),
    //   });

    heatmapWater = new Loca.HeatMapLayer({
          // loca,
          zIndex: 10,
          opacity: 1,
          visible: true,
          zooms: [2, 22],
      });

      heatmapWater.setSource(heatmapWaterData, {
          radius: 200000,
          unit: 'meter',
          height: 500000,
          //radius: 35,
          //unit: 'px',
          //height: 100,
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
          value: function (_index: any, feature: { properties: { avg: any; mom: string | any[]; }; }) {
              return feature.properties.avg;
            //   var value = feature.properties.mom.slice(0, -1);
            //   return value + 10 * Math.random();
          },
          // min: -100,
          // max: 100,
          heightBezier: [0, .53, .37, .98],
      });

    //   loca.add(heatmapWater);
    
      map.on('complete', function () {
        heatmapWater.addAnimate({
              key: 'radius',
              value: [0, 1],
              //   duration: 2000,
              duration: 0,
              easing: 'BackOut',
              // 开启随机动画
              //   transform: 1000,
              transform: 0,
              random: true,
              //   delay: 1000,
              delay: 0,
          });
      });
	//   map.on('click', function (e) {
    //       var feat = heatmapWater.queryFeature(e.pixel.toArray());
    //       if(feat){
    //         map.clearMap();
    //         map.add(AAMap.Marker({
	// 		  position:feat.lnglat,
    //           anchor: 'bottom-center',
    //           content: '<div style="margin-bottom: 15px; border:1px solid #fff; border-radius: 4px;color: #fff; width: 150px; text-align: center;">热力值: '+ feat.value.toFixed(2) +'</div>'
    //         }));
    //       }
    //   });
    //   var timerId = setTimeout(() => {
    //     loca.add(heatmapTem);
    //     clearTimeout(timerId); // 取消定时执行
    //    }, 1000); // 延迟2秒后修改message
    // });
      
}

//初始化灾害图层
function InitHazard() {
  var geo = new Loca.GeoJSONSource({
          // data: [],
          url: 'https://a.amap.com/Loca/static/loca-v2/demos/mock_data/china_traffic_event.json',
      });
      scatter = new Loca.ScatterLayer({
          // loca,
          zIndex: 10,
          opacity: 1,
          visible: true,
          zooms: [2, 22],
      });

      scatter.setSource(geo, {
          unit: 'px',
          size: [20, 20],
          texture: 'https://a.amap.com/Loca/static/loca-v2/demos/images/blue.png',
          borderWidth: 0,
      });
      
      // 呼吸
      var top10 = {
          type: 'FeatureCollection',
          features: [
              {
                  "type": "Feature",
                  "properties": {
                      "cityName": "韶关市",
                      "ratio": 0,
                      "rank": 96
                  },
                  "geometry": {
                      "type": "Point",
                      "coordinates": [
                          113.58052,
                          24.760098
                      ]
                  }
              },
              {
                  "type": "Feature",
                  "properties": {
                      "cityName": "乐山市",
                      "ratio": 0,
                      "rank": 97
                  },
                  "geometry": {
                      "type": "Point",
                      "coordinates": [
                          103.75082,
                          29.58099
                      ]
                  }
              },
              {
                  "type": "Feature",
                  "properties": {
                      "cityName": "阜阳市",
                      "ratio": 0,
                      "rank": 98
                  },
                  "geometry": {
                      "type": "Point",
                      "coordinates": [
                          115.82654,
                          32.889915
                      ]
                  }
              },
              {
                  "type": "Feature",
                  "properties": {
                      "cityName": "荆门市",
                      "ratio": 0,
                      "rank": 99
                  },
                  "geometry": {
                      "type": "Point",
                      "coordinates": [
                          112.209816,
                          30.997377
                      ]
                  }
              },
              {
                  "type": "Feature",
                  "properties": {
                      "cityName": "哈尔滨市",
                      "ratio": 0,
                      "rank": 100
                  },
                  "geometry": {
                      "type": "Point",
                      "coordinates": [
                          126.61314,
                          45.746685
                      ]
                  }
              },
              {
                  "type": "Feature",
                  "properties": {
                      "cityName": "达州市",
                      "ratio": 0,
                      "rank": 101
                  },
                  "geometry": {
                      "type": "Point",
                      "coordinates": [
                          107.493,
                          31.205515
                      ]
                  }
              },
              {
                  "type": "Feature",
                  "properties": {
                      "cityName": "自贡市",
                      "ratio": 0,
                      "rank": 102
                  },
                  "geometry": {
                      "type": "Point",
                      "coordinates": [
                          104.777824,
                          29.34555
                      ]
                  }
              },
              {
                  "type": "Feature",
                  "properties": {
                      "cityName": "陇南市",
                      "ratio": 0,
                      "rank": 103
                  },
                  "geometry": {
                      "type": "Point",
                      "coordinates": [
                          104.93356,
                          33.388184
                      ]
                  }
              },
              {
                  "type": "Feature",
                  "properties": {
                      "cityName": "南充市",
                      "ratio": 0,
                      "rank": 104
                  },
                  "geometry": {
                      "type": "Point",
                      "coordinates": [
                          106.1188,
                          30.800997
                      ]
                  }
              },
              {
                  "type": "Feature",
                  "properties": {
                      "cityName": "恩施土家族苗族自治州",
                      "ratio": 0,
                      "rank": 105
                  },
                  "geometry": {
                      "type": "Point",
                      "coordinates": [
                          109.48512,
                          30.298103
                      ]
                  }
              }
          ]
      };
      breath = new Loca.ScatterLayer({
          zIndex: 121,
      });
      breath.setSource(new Loca.GeoJSONSource({
          data: top10,
      }));
      breath.setStyle({
          unit: 'px',
          size: [50, 50],
          texture: 'https://a.amap.com/Loca/static/loca-v2/demos/images/breath_red.png',
          animate: true,
          duration: 1000,
      });
      loca.animate.start();
      
}

function getEventsCollection() {
  var events = [{
    "code": 110000,
    "name": "北京市",
    "events": [{
            "lngLat": "68.731153,17.010458",
            "id": 1868459870,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "70.506534,23.562138",
            "id": 455154464,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "72,35.843587",
            "id": 1818586214,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "74,30.690492",
            "id": 2080537607,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "76,19.625207",
            "id": 1467766644,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "78,28.761410",
            "id": 1641308637,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "80,40.112516",
            "id": 494542195,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "82,12.875484",
            "id": 912864867,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "84,43.669228",
            "id": 1140868111,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "86,49.137176",
            "id": 711469688,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "88,16.182146",
            "id": 2146205695,
            "pic": false,
            "source": 0,
            "type": 2
        },
        {
            "lngLat": "90,28.383838",
            "id": 397940652,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "92,30.238499",
            "id": 1608933362,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "94,22.746641",
            "id": 1838050710,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "96,24.031905",
            "id": 877409366,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "98,26.077546",
            "id": 706554368,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "100,28.153173",
            "id": 937506753,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "116.295653,30.234626",
            "id": 1339641849,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "116.321472,20.407838",
            "id": 858338057,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "116.628102,18.619864",
            "id": 360256859,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "116.662064,16.215760",
            "id": 1872457656,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "116.089321,14.588933",
            "id": 1721525944,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "116.064639,12.929627",
            "id": 1116947127,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "116.542658,32.759983",
            "id": 1999402762,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "117.207314,34.204017",
            "id": 521609022,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "116.741243,36.214172",
            "id": 389420828,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "116.128031,38.820252",
            "id": 1181173322,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "116.506077,39.963128",
            "id": 476650577,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "116.558300,23.974173",
            "id": 768552438,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "116.548344,39.693684",
            "id": 720972485,
            "pic": false,
            "source": 0,
            "type": 3
        },
        {
            "lngLat": "117.114306,40.148748",
            "id": 1944744609,
            "pic": false,
            "source": 0,
            "type": 3
        },
        ]}];
    let _events = events[0].events;
    var list = _events.map((e: { lngLat: string; }) => {
        let ll = e.lngLat.split(',');
        let arr = [parseFloat(ll[0]), parseFloat(ll[1])]
        return {
            "type": "Feature",
            "properties": {
                rawData: e
            },
            "geometry": {
                "type": "Point",
                "coordinates": arr
            }
        }
    })

    var data = {
        "type": "FeatureCollection",
        "features": list,
    };
    return data;
}

function InitAqi() {
  var data = getEventsCollection();
  var geo = new Loca.GeoJSONSource({
      data: data,
  });

  layer = new Loca.IconLayer({
      zIndex: 15,
      opacity: 1,
  });

  var trafficIcons = {
      1: 'https://a.amap.com/Loca/static/loca-v2/demos/images/traffic-control.png',
      2: 'https://a.amap.com/Loca/static/loca-v2/demos/images/jam.png',
      3: 'https://a.amap.com/Loca/static/loca-v2/demos/images/construction.png',
      4: 'https://a.amap.com/Loca/static/loca-v2/demos/images/close.png',
      5: 'https://a.amap.com/Loca/static/loca-v2/demos/images/fog.png',
      0: 'https://a.amap.com/Loca/static/loca-v2/demos/images/accident.png',
  };
  layer.setSource(geo);
  layer.setStyle({
      unit: 'px',
      icon: (_index, feature) => {
          let data = feature.properties.rawData;
          let url = trafficIcons[data.type % Object.keys(trafficIcons).length];
          return url;
      },
      iconSize: [40,40],
      offset: [0, -40],
      rotation: 0,
  })
                

  // 拾取测试
  map.on('click', (e) => {
      const feat = layer.queryFeature(e.pixel.toArray());
      // console.log('feat', feat);
      if (feat) {
          layer.setStyle({
              unit: 'px',
              icon: (_index, feature) => {
                  let data = feature.properties.rawData;
                  let url = trafficIcons[data.type % Object.keys(trafficIcons).length];
                  return url;
              },
              iconSize: (_i, feature) => {
                  if (feature === feat) {
                      return [60, 60];
                  }
                  return [40, 40];
              },
          });
      }
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
  background-color: rgba(45,45,45,0.2);
  display: flex;
  margin: 0.3em 0 0.3em 0.4em;
  position: relative;
}

.layerbtn2 {
  height: 35px;
  border: 1px solid #3924a7; 
  border-radius: 30px;
  background-color: rgba(45,45,45,0.2);
  display: flex;
  margin: 0.3em 0 0.3em 0.4em;
  position: relative;
}

.unselected {
  height: 35px;
  border: 1px solid #3924a7; 
  border-radius: 30px;
  background-color: rgba(45,45,45,0.1);
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
  background:linear-gradient(to right top, rgba(26, 79, 158, 0.5),rgb(243, 179, 179, 0.5));
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
  background-size: 100% 100%;/*按比例缩放*/
  position: absolute;
  right:0;
}

.btnIconb {
  width: 2.4em;
  height: 2.4em;
  border-radius: 3em;
  box-shadow: 0 0 4px 0 black;
  background-image: url("../../assets/img/water.png");
  background-size: 100% 100%;/*按比例缩放*/
  position: absolute;
  right:0;
}

.btnIconf {
  width: 2.4em;
  height: 2.4em;
  border-radius: 3em;
  box-shadow: 0 0 4px 0 black;
  background-image: url("../../assets/img/AQI.png");
  background-size: 100% 100%;/*按比例缩放*/
  position: absolute;
  right:0;
}

.btnIcone {
  width: 2.4em;
  height: 2.4em;
  border-radius: 3em;
  box-shadow: 0 0 4px 0 black;
  background-image: url("../../assets/img/earthquake.png");
  background-size: 100% 100%;/*按比例缩放*/
  position: absolute;
  right:0;
}

.btnIcond {
  width: 2.4em;
  height: 2.4em;
  border-radius: 3em;
  box-shadow: 0 0 4px 0 black;
  background-image: url("../../assets/img/wind.png");
  background-size: 100% 100%;/*按比例缩放*/
  position: absolute;
  right:0;
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
</style>