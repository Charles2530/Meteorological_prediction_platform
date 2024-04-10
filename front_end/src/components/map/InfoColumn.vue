<template>
    <div style="max-height: 650px; overflow: auto">
        <el-card style="width: 90%; background-color:white;margin: auto;margin-top: 2%;">
            <el-row :gutter="20">
                <el-col :span="10">
                    <div class="grid-content">
                        <span style="font-size: smaller;">{{time}}</span>
                    </div>
                </el-col>
                <el-col :offset="7" :span="7">
                    <div class="grid-content">
                        <el-button><span>{{weather.air}}</span></el-button>
                    </div>
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :offset="6" :span="6">
                    <div class="grid-content">
                        <img :src="getAssetsFile( weather.picPath +'.png')" width="100%" height="100%"/>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content">
                        <span style="font-size: larger;">{{weather.tem}}  </span>
                        <span style="font-size: larger;">{{weather.condition}}</span>
                    </div>
                </el-col>
            </el-row> 
            <el-row :gutter="20">
                <el-col :offset="1" :span="22">
                    <div class="grid-content">
                        <span>{{weather.infos}}</span>
                    </div>
                </el-col>
            </el-row>   
            <el-row :gutter="20">
                <el-col :offset="1" :span="7">
                    <div class="grid-content">
                        <span>{{weather.wind}}</span>
                        <br/>
                        <span>{{weather.windDir}}</span>
                    </div>
                </el-col>
                <el-col :offset="1" :span="7">
                    <div class="grid-content">
                        <span>{{weather.hum}}</span>
                        <br/>
                        <span>"相对湿度"</span>
                    </div>
                </el-col>
                <el-col :offset="1" :span="7">
                    <div class="grid-content">
                        <span>{{weather.ray}}</span>
                        <br/>
                        <span>"紫外线"</span>
                    </div>
                </el-col>
            </el-row>  
        </el-card>

        <el-card style="width: 90%; background-color:white;margin: auto;margin-top: 2%;">
            <el-row :gutter="10">
                <el-col :offset="9" :span="6">
                    <div class="grid-content">
                        <span>地形概况</span>
                    </div>
                </el-col>
            </el-row> 
            <el-row :gutter="10">
                <el-col :offset="1" :span="22">
                    <div class="grid-content">
                        <span>河南省位于位于中国中东部、华北平原南部的黄河中下游地区。东连山东、安徽，西邻陕西，北与河北、山西相接，南临湖北；全省总面积16.7万平方千米，居全国各省区市第17位，占全国总面积的1.73%。</span>
                    </div>
                </el-col>
            </el-row>   

        </el-card>

        <el-card style="width: 90%; background-color:white;margin: auto;margin-top: 2%;">
            <el-table :data="tableData" size:mini style="font-size: 10px" :row-style="{height:'50px'}">
                <el-table-column prop="date" label="Date" width="180" />
                <el-table-column prop="name" label="Name" width="180" />
                <el-table-column prop="address" label="Address" />
            </el-table> 

        </el-card>
    </div>
  </template>

<script setup lang="ts">
import { getAssetsFile } from '@/utils/pub-use'

let time = "2024-04-10 17:33"
let weather = reactive({
    picPath: "cloud",
    tem: "11℃",
    condition: "阴",
    infos: "今晚多云。明天晴，比今天热很多，空气一般。",
    wind: "2级",
    windDir: "西南风",
    hum: "70%",
    ray: "中等",
    air: "AQI良"
})


const tableData = [
  {
    date: '2016-05-03',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
]

</script>

<style scoped>

.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

</style>
  