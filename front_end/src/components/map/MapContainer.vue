<template>
  <div id="mapContainer">
    <div class="input-card" style="position: relative; z-index: 100; top:30%; width: 100px;">
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
        <el-button :class="{ 'selected': buttonActive.a, 'unselected': !buttonActive.a }"  :active="buttonActive.A" @click="clicka">
          <div class="btnDiv">
            <div class="btnName">风场</div>
            <div class="btnIcon1"></div>
          </div>
        </el-button>
        <el-button :class="{ 'selected': buttonActive.b, 'unselected': !buttonActive.b }"  :active="buttonActive.A" @click="clickb">
          <div class="btnDiv">
            <div class="btnName">地震</div>
            <div class="btnIcon2"></div>
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
});

let map: {
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
remove(pl: { setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: { key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number; yoyo: boolean; repeat: number; }) => void; }): unknown; add: (arg0: any) => void; 
}=null;

let windLayer: AMapWind = null;

let wms: null = null;

let sate: null = null;

let pl: { setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: { key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number; yoyo: boolean; repeat: number; }) => void; } = null;

// let dat: {
// removeLayer(pl: { setSource: (arg0: any) => void; setStyle: (arg0: { radius: (i: any, feature: { properties: { level: string | number; }; }) => number; color: (i: any, feature: { properties: any; }) => string; borderWidth: number; blurRadius: number; unit: string; }) => void; addAnimate: (arg0: { key: string; value: number[]; duration: number; easing: string; transform: number; random: boolean; delay: number; yoyo: boolean; repeat: number; }) => void; }): unknown; addLayer: (arg0: any, arg1: string) => void; 
// } = null;

// 使用defineEmits注册一个自定义事件
const emit = defineEmits(["getValue"])
 
// 点击事件触发emit，去调用我们注册的自定义事件getValue,并传递value参数至父组件
const transValue = () => {
  emit("getValue", dis_info.districtName);
}

onMounted(() => {
  getHazardInfo();
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
      map.setLimitBounds(new AMap.Bounds([50,60],[150,0]));
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
      dis_info.district = new AMap.DistrictSearch(dis_info.opts);
      dis_info.geoCoder = new AMap.Geocoder();
      handlerMapClick();
      markPoints();
      InitEarthQuake();
    })
    .catch((e) => {
      console.log(e);
    });
}

//高亮区域
function drawBounds() {
  var step = 15;
  //行政区查询
  dis_info.district.search(
    dis_info.districtCode,
    function (_status: any, result: { districtList: { boundaries: any }[] }) {
      map.remove(dis_info.polygons); //清除上次结果
      dis_info.polygons = [];
      var bounds = result.districtList[0].boundaries;
      if (bounds) {
        var bounds2 = new Array();
        if (dis_info.districtCode != '710000' && dis_info.districtCode != '460000') {
          bounds2.push(bounds.pop());
          bounds = bounds2;
        }
        if(dis_info.districtCode == '150000') {
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
          dis_info.polygons.push(polygon);
        }
      }

      map.add(dis_info.polygons);
      map.setZoom(5);
    }
  );
}

//点击区域触发事件
function handlerMapClick() {
  map.on("click", (e: { lnglat: { lng: any; lat: any } }) => {
    // 点击坐标
    const markersPosition = [e.lnglat.lng, e.lnglat.lat];
    // console.log(markersPosition);
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
            //向父组件传省份名
            transValue();
            dis_info.districtName = dis_info.districtName + "/中国";
            drawBounds();
            map.setCenter(markersPosition, false, 300);
          } else {
            dis_info.districtName = "中国";
            //向父组件传省份名
            transValue();
            map.remove(dis_info.polygons); //清除结果
            map.setCenter([105, 36], false, 30);
            map.setZoom(4.8);
          }
        } else {
          dis_info.districtName = "中国";
          //向父组件传省份名
          transValue();
          map.remove(dis_info.polygons); //清除结果
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
    showWind();
  }
  else {
    windLayer.remove();
  }
}

function clickb() {
  buttonActive.b = !buttonActive.b;
  if (buttonActive.b) {
    loca.add(pl);
  }
  else {
    loca.remove(pl);
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
  width:100px;
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
  width: 90px;
  margin: 0.3em 0 0.3em 0.4em;
  position: relative;
}

.layerbtn2 {
  height: 35px;
  border: 1px solid #3924a7; 
  border-radius: 30px;
  background-color: rgba(45,45,45,0.2);
  display: flex;
  width: 90px;
  margin: 0.3em 0 0.3em 0.4em;
  position: relative;
}

.unselected {
  height: 35px;
  border: 1px solid #3924a7; 
  border-radius: 30px;
  background-color: rgba(45,45,45,0.1);
  display: flex;
  width: 90px;
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
  width: 90px;
  margin: 0.3em 0 0.3em 0.4em;
  position: relative;
}

.btnIcon1 {
  width: 2.4em;
  height: 2.4em;
  border-radius: 3em;
  box-shadow: 0 0 4px 0 black;
  background-image: url("../../assets/img/wind.png");
  background-size: 100% 100%;/*按比例缩放*/
  z-index: 1;
  text-align: center;
  position: absolute;
  right:0;
}

.btnIcon2 {
  width: 2.4em;
  height: 2.4em;
  border-radius: 3em;
  box-shadow: 0 0 4px 0 black;
  background-image: url("../../assets/img/earthquake.png");
  background-size: 100% 100%;/*按比例缩放*/
  z-index: 1;
  text-align: center;
  position: absolute;
  right:0;
}

.btnName {
  position: absolute;
  left: 15%;
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
