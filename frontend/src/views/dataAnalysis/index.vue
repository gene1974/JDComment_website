<template>
    <div style="background:#F7F8FA ;min-width:fit-content;">
        <!-- <div class="home-container"><el-header>产品数据分析</el-header></div> -->
        <!-- <div class="home-container"><h1>数据分析</h1></div> -->

       
        <!-- <div style="margin: 30px"> -->
        <el-row :gutter="30"  class="dataAnalysisBacground">
            <h1 style="margin-left:40px">数据分析</h1>
            <!-- 选取产地时间 -->
            <el-row class="fenquxuanzekuangRow" :gutter="30" style="margin-left:20px">
                <!-- 产地 -->
                <el-col :span="5">
                    <el-row>
                        <el-col :span="6"><div class="xuanzekuangshuoming">产地</div></el-col>
                        <el-col :span="18">
                            <el-select v-model="chandiValue" placeholder="请选择" @change="chandiValueChange">
                                <el-option
                                v-for="item in chandiList" :key="item" :label="item" :value="item">
                                </el-option>
                            </el-select>
                        </el-col>
                    </el-row>
                    <el-row style="margin-top: 20px">
                        <el-col :span="6"><div class="xuanzekuangshuoming">筛选</div></el-col>
                        <el-col :span="18">
                            <el-select v-model="analysisChoice" placeholder="请选择" @change="analysisChoiceChange">
                                <el-option
                                v-for="item in analysisList" :key="item"  :label="item" :value="item">
                                </el-option>
                            </el-select>
                        </el-col>
                    </el-row>
                </el-col>
                <!-- 产品 -->
                <el-col :span="5">
                    <el-row>
                        <el-col :span="6"><div class="xuanzekuangshuoming">产品</div></el-col>
                        <el-col :span="18">
                            <el-select v-model="chanpinValue" placeholder="请选择">
                                <el-option
                                v-for="item in chanpinList" :key="item" :label="item" :value="item">
                                </el-option>
                            </el-select>
                        </el-col>
                    </el-row>
                </el-col>
                <!-- 起始时间 -->
                <el-col :span="10">
                    <el-row>
                        <el-col :span="6"><div class="xuanzekuangshuoming">起始时间</div></el-col>
                        <el-col :span="8">
                            <el-date-picker
                                style="width:100%"
                                v-model="startDate"
                                type="date"
                                value-format="yyyy-MM-dd"
                                placeholder="选择日期">
                            </el-date-picker>
                        </el-col>
                        <el-col :span="2"><div class="xuanzekuangshuoming"> - </div></el-col>
                        <el-col :span="8">
                            <el-date-picker
                                style="width:100%"
                                v-model="endDate"
                                type="date"
                                value-format="yyyy-MM-dd"
                                placeholder="选择日期">
                            </el-date-picker>
                        </el-col>
                    </el-row>
                </el-col>
                <el-col :span="2">
                    <el-row>
                        <el-button :loading="getDailyInfoLoading" type="primary" @click="clickQuery" class="InfoButton">查询</el-button>
                    </el-row>
                    <el-row style="margin-top: 20px">
                        <el-button :loading="getDailyInfoLoading" type="primary" @click="clickAll" class="ResetButton">重置</el-button>
                    </el-row>
                </el-col>
            </el-row>
        </el-row>

        <!-- 获取图表按钮 -->
        <!-- <el-row :gutter="30"  class="dataAnalysisBacground" type="flex" justify="center">
            <el-col class="fenquCol" style="margin-left: 30px">
                <el-row style="margin:20px 10px;">
                    <el-col :span="4">
                        <el-button style="color:powderblue" :loading="getDailyInfoLoading" type="primary" @click="clickAll" class="DailyInfoButton">获取全部</el-button>
                    </el-col>
                    <el-col :span="4">
                        <el-button :loading="getDailyInfoLoading" type="primary" @click="clickDailyInfo" class="DailyInfoButton">获取基本走势</el-button>
                    </el-col>
                    <el-col :span="4">
                        <el-button :loading="getAnalysisInfoLoading" type="primary" @click="clickAnalysisInfo" class="DailyInfoButton">获取分析概览</el-button>
                    </el-col>
                    <el-col :span="4">
                        <el-button :loading="getAnalysisDetailLoading" type="primary" @click="clickAnalysisDetail" class="DailyInfoButton">获取分析详情</el-button>
                    </el-col>
                </el-row>
            </el-col>    
        </el-row> -->

        <!-- <div style="background: rgb(232, 221, 203)"> -->
        <!-- 产地信息，总体评价 -->
        <el-row>
            <el-col :span="8" v-show="SentimentText" style="background: rgb(255, 255, 255);margin:20px;margin-left:40px;" class="fenquCol">
                <el-card>
                    <h3 style="margin-left:20px;">产品产地信息</h3>
                    <el-table
                        :data="product_table"
                        height="200"
                        width="330"
                        stripe
                        style="width: 100%">
                        <el-table-column prop="location" label="产地" width="150"></el-table-column>
                        <el-table-column prop="product" label="产品"> </el-table-column>
                    </el-table>
                </el-card>
            </el-col>
            <el-col :span="8" v-show="SentimentText" style="background: rgb(255, 255, 255);margin:20px" class="fenquCol">
                <el-card>
                    <h3 style="margin-left:30px;">消费评价概览</h3>
                    <div id="ScoreText" style="margin: 10px; margin-left:30px; color:slategrey">等待获取评价概览</div>
                    <div id="HeatText" style="margin: 10px; margin-left:30px; color:slategrey">等待获取热度信息</div>
                    <div id="AspectText" style="margin: 10px; margin-left:30px; color:slategrey">等待获取具体评价</div>
                </el-card>
            </el-col>
        </el-row>

        <!-- 购买建议 -->
        <!-- <el-col :span="11" v-show="AnalysisInfoStatus" class="fenquCol">
            <div>
                <el-row v-show="AnalysisInfoStatus">
                    <el-col :span="12">
                        <div class="xuanzekuangshuoming" style="font-weight:bold">购买建议</div>
                        <el-card  shadow="hover" class="cardStyle">
                            <el-table
                                :header-cell-style="{textAlign: 'center'}" :cell-style="{ textAlign: 'center' }"
                                :data="purchaseAdvicesList"
                                style="width: 100%">
                                <el-table-column
                                    prop="advice"
                                    label="购买建议"
                                    width="300">
                                </el-table-column>
                            </el-table>
                        </el-card>
                    </el-col>
                    <el-col :span="12">
                        <div class="xuanzekuangshuoming" style="font-weight:bold">种植建议</div>
                        <el-card  shadow="hover" class="cardStyle">
                            <el-table
                                :header-cell-style="{textAlign: 'center'}" :cell-style="{ textAlign: 'center' }"
                                :data="plantAdvicesList"
                                style="width: 100%">
                                <el-table-column
                                    prop="advice"
                                    label="种植建议"
                                    width="300">
                                </el-table-column>
                            </el-table>
                        </el-card>
                    </el-col>
                </el-row>
            </div>
        </el-col> -->
        
        <!-- 基本走势 -->
        <el-row :gutter="30" style="margin:20px" class="dataAnalysisBacground" >
            <el-col :span="11" v-show="DailyInfoStatus" class="fenquCol">
                <el-row class="fenqubiaotiRow" style="margin:20px; margin-bottom:0px;"><el-col :span="24"><div class="fenqubiaoti">基本走势</div></el-col></el-row>
                <el-row v-show="DailyInfoStatus" style="margin-top:20px">
                    <el-col :span="11" style='margin:10px'>
                        <data-statistics-bar0 ref="bar0"/>
                    </el-col>
                    <el-col :span="11" style='margin:10px'>
                        <data-statistics-line0 ref="line0"/>
                    </el-col>
                </el-row>
                <br/>
                <el-row :gutter="30" v-show="DailyInfoStatus" class="dataAnalysisBacground" >
                    <el-col :span="18" style="background: rgb(255, 255, 255); margin-left:40px" class="fenquCol">
                        <h3 style="margin:20px">每日评分信息</h3>
                        <el-card><el-table
                            :data="comment_daily"
                            :key="component_key"
                            height="250"
                            width="450"
                            stripe
                            style="width:100%">
                            <el-table-column prop="time" label="日期" width="150"></el-table-column>
                            <el-table-column prop="number" label="评价数量" width="150"></el-table-column>
                            <el-table-column prop="score" label="评分"> </el-table-column>
                        </el-table></el-card>
                    </el-col>
                </el-row>
            </el-col>
        <!-- </el-row>  -->

        
        
        <!-- 分析概览 -->
        <!-- <el-row :gutter="30"  class="dataAnalysisBacground"> -->
            <el-col :span="11" v-show="AnalysisInfoStatus" class="fenquCol">
                <el-row class="fenqubiaotiRow" style="margin:20px; margin-bottom:0px;"><el-col :span="24"><div class="fenqubiaoti">分析概览</div></el-col></el-row>
                <el-row v-show="AnalysisInfoStatus" style="margin:20px">
                    <el-col :span="12">
                        <data-statistics-pie0 ref="pie0"/>
                    </el-col>
                    <el-col :span="12">
                        <data-statistics-pie1 ref="pie1"/>
                    </el-col>
                </el-row>
                <br/>
                <el-row :gutter="30" class="dataAnalysisBacground" >
                    <el-col :span="18" style="background: rgb(255, 255, 255); margin-left:80px" class="fenquCol">
                        <h3 style="margin:20px">分类评价信息</h3>
                        <el-card><el-table
                            :data="comment_aspect"
                            :key="component_key"
                            height="250"
                            width="450"
                            stripe
                            style="width: 100%">
                            <el-table-column prop="aspect" label="评价类别" width="150"></el-table-column>
                            <el-table-column prop="number" label="评价数量" width="150"></el-table-column>
                            <el-table-column prop="score" label="整体评价结果"> </el-table-column>
                        </el-table></el-card>
                    </el-col>
                </el-row>
            </el-col>
        </el-row>

        <!-- 分析详情 -->
        <div v-show="AnalysisDetailStatus" style="background: rgb(240, 242, 245);">
            <el-row class="fenqubiaotiRow" style="margin:20px"><el-col :span="24"><div class="fenqubiaoti">分析详情</div></el-col></el-row>
            <el-row class="fenqubiaotiRow" type="flex" justify="center">
                <el-col :span="3"><div class="xuanzekuangshuoming">产品属性</div></el-col>
                <el-col :span="14" type="flex" justify="center">
                    <el-checkbox-group v-model="varietyValue"  :max="1" @change="varietyChange">
                        <el-checkbox-button v-for="variety in varietyList" :label="variety" :key="variety">{{variety}}</el-checkbox-button>
                    </el-checkbox-group>
                    <div style="margin-top:20px; color:slategrey">（取消选择一个属性，再点击另一个属性）</div>
                </el-col>
            </el-row>
            <el-row id="DetailPie" v-show="AnalysisDetailStatus" style="margin:20px; margin-top:0px" type="flex" justify="space-around">
                <el-col :span="8" style="margin:10px;">
                    <el-card><data-statistics-pie2 ref="pie2"/></el-card>
                </el-col>
                <el-col :span="8" style="margin:10px;">
                    <el-card><data-statistics-pie3 ref="pie3"/></el-card>
                </el-col>
                <el-col :span="8" style="margin:10px;">
                    <el-card><data-statistics-pie4 ref="pie4"/></el-card>
                </el-col>
            </el-row>
            <!-- 正面负面评价 -->
            <el-row id="DetailComment" v-show="AnalysisDetailStatus" style="margin:20px;" type="flex" justify="space-around" >
                <el-col :span="8">
                    <div class="xuanzekuangshuoming" style="font-weight:bold">正面评价</div>
                    <el-card  shadow="hover" class="cardStyle"  style="width:50">
                        <el-table
                            :header-cell-style="{textAlign: 'center'}" :cell-style="{ textAlign: 'center' }"
                            :data="POSUnitList"
                            style="width: 100%">
                            <el-table-column
                                prop="target"
                                label="评价对象"
                                width="100%">
                            </el-table-column>
                            <el-table-column
                                prop="opinion"
                                label="评价观点"
                                width="100%">
                            </el-table-column>
                            <el-table-column
                                prop="times"
                                label="评价次数"
                                width="100%">
                            </el-table-column>
                        </el-table>
                    </el-card>
                </el-col>
                <el-col :span="8">
                    <div class="xuanzekuangshuoming" style="font-weight:bold">中性评价</div>
                    <el-card  shadow="hover" class="cardStyle"  style="width:50">
                        <el-table
                            :header-cell-style="{textAlign: 'center'}" :cell-style="{ textAlign: 'center' }"
                            :data="NEUUnitList"
                            style="width: 100%">
                            <el-table-column
                                prop="target"
                                label="评价对象"
                                width="100%">
                            </el-table-column>
                            <el-table-column
                                prop="opinion"
                                label="评价观点"
                                width="100%">
                            </el-table-column>
                            <el-table-column
                                prop="times"
                                label="评价次数"
                                width="100%">
                            </el-table-column>
                        </el-table>
                    </el-card>
                </el-col>
                <el-col :span="8">
                    <div class="xuanzekuangshuoming" style="font-weight:bold">负面评价</div>
                    <el-card  shadow="hover" class="cardStyle" style="width:50">
                        <el-table
                            :header-cell-style="{textAlign: 'center'}" :cell-style="{ textAlign: 'center' }"
                            :data="NEGUnitList"
                            style="width: 100%">
                            <el-table-column
                                prop="target"
                                label="评价对象"
                                width="100%">
                            </el-table-column>
                            <el-table-column
                                prop="opinion"
                                label="评价观点"
                                width="100%">
                            </el-table-column>
                            <el-table-column
                                prop="times"
                                label="评价次数"
                                width="100%">
                            </el-table-column>
                        </el-table>
                    </el-card>
                </el-col>
            </el-row>
        </div>
        
        <!-- 产品展示 -->
        <div style="margin: 30px; margin-top: 100px">
            <div style="margin: 10px; margin-left:20px; color:slategrey; text-align: center;">部分产品展示：（点击图片跳转京东链接）</div>
            <br/>
            <el-row style="margin:20px; margin-top:0px" type="flex" justify="space-around">
                <el-col :span="8"><a href="https://search.jd.com/Search?keyword=大米&enc=utf-8" target="_blank">
                    <img src="./images/大米.jpeg" width="300" height="200">
                </a></el-col>
                <el-col :span="8"><a href="https://search.jd.com/Search?keyword=茶叶&enc=utf-8" target="_blank">
                    <img src="./images/茶叶.jpeg" width="300" height="200">
                </a></el-col>
                <el-col :span="8"><a href="https://search.jd.com/Search?keyword=番茄&enc=utf-8" target="_blank">
                    <img src="./images/番茄.jpeg" width="300" height="200">
                </a></el-col>
            </el-row>
            <el-row style="margin:20px; margin-top:0px" type="flex" justify="space-around">
                <el-col :span="8"><a href="https://search.jd.com/Search?keyword=荸荠&enc=utf-8" target="_blank">
                    <img src="./images/荸荠.jpeg" width="300" height="200">
                </a></el-col>
                <el-col :span="8"><a href="https://search.jd.com/Search?keyword=油茶&enc=utf-8" target="_blank">
                    <img src="./images/油茶.jpeg" width="300" height="200">
                </a></el-col>
                <el-col :span="8"><a href="https://search.jd.com/Search?keyword=猕猴桃&enc=utf-8" target="_blank">
                    <img src="./images/猕猴桃.jpeg" width="300" height="200">
                </a></el-col>
            </el-row>
            <br/>
            <br/>
        </div>

        <!-- </div> -->
    </div>
</template>

<script>
    import {getDailyInfo} from '@/api/dataAnalysis.js'
    import {getAnalysisInfo} from '@/api/dataAnalysis.js'
    import {getAnalysisDetail} from '@/api/dataAnalysis.js'
    import {getSentimentAnalysis} from '@/api/dataAnalysis.js'
    import DataStatisticsBar0 from './bar0.vue'
    import DataStatisticsLine0 from './line0.vue'
    import DataStatisticsPie0 from './pie0.vue'
    import DataStatisticsPie1 from './pie1.vue'
    import DataStatisticsPie2 from './pie2.vue'
    import DataStatisticsPie3 from './pie3.vue'
    import DataStatisticsPie4 from './pie4.vue'
//   import { saveAs } from 'file-saver'
  
    export default {
        components: {
            DataStatisticsBar0,
            DataStatisticsLine0,
            DataStatisticsPie0,
            DataStatisticsPie1,
            DataStatisticsPie2,
            DataStatisticsPie3,
            DataStatisticsPie4,
        },
        data() {
        return {
            analysisChoice:'基本走势',
            analysisList:['全部信息', '基本走势', '分析概览', '分析详情'],
            chandiValue:'安徽省巢湖市',
            chandiList:['安徽省巢湖市','江西省丰城市','江西省奉新县','江西省井冈山市','江西上饶市万年县','四川省宜宾市屏山县','江西省宜春市上高县','湖北省仙桃市','江西省永新县',],
            chandichanpinDict:{
                '安徽省巢湖市':['大米','番茄','茶叶'],
                '江西省丰城市':['油茶','大米','荸荠'],
                '江西省奉新县':['猕猴桃','大米','茶叶'],
                '江西省井冈山市':['竹笋','红米','蜜柚'],
                '江西上饶市万年县':['贡米','茶油','竹笋'],
                '四川省宜宾市屏山县':['炒青','椪柑','竹笋'],
                '江西省宜春市上高县':['大蒜','白肉姜','红心脚板薯'],
                '湖北省仙桃市':['香米','藕','豆皮'],
                '江西省永新县':['酱姜','橙皮','蜜茄'],
            },
            chanpinValue:'大米',
            chanpinList:['大米','番茄','茶叶'],
            startDate:'2022-03-01',
            endDate:'2022-03-31',
            SentimentText: false,
            getDailyInfoLoading:false,
            DailyInfoRes: null,
            DailyInfoStatus: false,
            getAnalysisInfoLoading:false,
            AnalysisInfoRes: null,
            AnalysisInfoStatus: false,
            purchaseAdvicesList:[{'advice': '暂无'}],
            plantAdvicesList:[{'advice': '暂无'}],
            varietyValue:['价格'],
            varietyList:['价格','品质','色泽','口感','包装','分量','物流','售后'],
            getAnalysisDetailLoading:false,
            AnalysisDetailRes: null,
            AnalysisDetailStatus: false,
            POSUnitList:[{}],
            NEUUnitList:[{}],
            NEGUnitList:[{}],
            comment_daily: [{}],
            comment_aspect: [{}],
            component_key: 0,
        }
        },
        created(){
            this.product_table = []
            for (var i in this.chandiList){
                this.product_table[i] = {
                    'location': this.chandiList[i],
                    'product': ('、'.concat(this.chandichanpinDict[this.chandiList[i]])).substring(1),
                }
            }
        },
        mounted() {
        // this.$refs.chart1.initChart('123')
        },
        methods: {
            clickQuery(){
                if(this.analysisChoice == '全部信息'){
                    this.clickAll()
                }
                else if(this.analysisChoice == '基本走势'){
                    this.clickDailyInfo()
                }
                else if(this.analysisChoice == '分析概览'){
                    this.clickAnalysisInfo()
                }
                else if(this.analysisChoice == '分析详情'){
                    this.clickAnalysisDetail()
                }
            },
            chandiValueChange(chandiValue){
                this.chanpinList = this.chandichanpinDict[chandiValue]
            },
            varietyChange(varietyValue){
                console.log(varietyValue)
                // 选中一个类别
                if (varietyValue.length > 0){
                    for(var index in this.AnalysisDetailRes['data']['aspect_details']){
                        if (this.AnalysisDetailRes['data']['aspect_details'][index]['aspect'] == this.varietyValue[0]){
                            console.log(this.AnalysisDetailRes['data']['aspect_details'][index]['aspect'])
                            console.log(this.AnalysisDetailRes['data']['aspect_details'].length)
                            document.getElementById("DetailComment").style.visibility = 'visible'
                            document.getElementById("DetailPie").style.visibility = 'visible'
                            this.$refs.pie2.initChart('情感分布','', this.AnalysisDetailRes['data']['aspect_details'][index]['sentiment_distribution'])
                            this.$refs.pie3.initChart('评价对象','', this.AnalysisDetailRes['data']['aspect_details'][index]['target_distribution'])
                            this.$refs.pie4.initChart('评价观点','', this.AnalysisDetailRes['data']['aspect_details'][index]['opinion_distribution'])
                            this.POSUnitList = this.AnalysisDetailRes['data']['aspect_details'][index]['positive_units']
                            this.NEUUnitList = this.AnalysisDetailRes['data']['aspect_details'][index]['neutral_units']
                            this.NEGUnitList = this.AnalysisDetailRes['data']['aspect_details'][index]['negative_units']
                            return
                        }
                    }
                    document.getElementById("DetailComment").style.visibility = 'hidden'
                    document.getElementById("DetailPie").style.visibility = 'hidden'
                    this.SentimentText = false
                    this.DailyInfoStatus = false
                    this.AnalysisInfotatus = false
                    this.AnalysisDetailStatus = false
                }
                else{
                    document.getElementById("DetailComment").style.visibility = 'hidden'
                    document.getElementById("DetailPie").style.visibility = 'hidden'
                }
            },
            clickAll(){
                this.getDailyInfoLoading = true
                this.getAnalysisInfoLoading = true
                this.getAnalysisDetailLoading = true
                let data = {}
                data['location'] = this.chandiValue
                data['variety'] = this.chanpinValue
                data['start_date'] = this.startDate
                data['end_date'] = this.endDate
                getSentimentAnalysis(data).then(res =>{
                    this.SentimentText = true
                    this.DailyInfoStatus = true
                    this.AnalysisInfoStatus = true
                    this.AnalysisDetailStatus = true
                    this.$message({message:"获取成功", type:'success'})
                    this.SentimentRes = res
                    this.AnalysisDetailRes = res
                    console.log(this.SentimentRes)
                    this.$refs.bar0.initChart('消费热度','', this.SentimentRes['data']['daily_info'])
                    this.$refs.line0.initChart('消费评价','', this.SentimentRes['data']['daily_info'])
                    this.$refs.pie0.initChart('评分分布','', this.SentimentRes['data']['score_distribution'])
                    this.$refs.pie1.initChart('属性分布','', this.SentimentRes['data']['aspect_distribution'])
                    this.purchaseAdvicesList = this.SentimentRes['data']['purchase_advices']
                    this.plantAdvicesList = this.SentimentRes['data']['plant_advices']
                    document.getElementById("ScoreText").innerHTML = this.SentimentRes['data']['score_text']
                    document.getElementById("HeatText").innerHTML = this.SentimentRes['data']['heat_text']
                    document.getElementById("AspectText").innerHTML = this.SentimentRes['data']['aspect_text']
                    this.getDailyInfoLoading = false
                    this.getAnalysisInfoLoading = false
                    this.getAnalysisDetailLoading = false
                    this.SentimentText = true
                    if (res['data']['daily_info'] === undefined){
                        this.$message.warning('时间段内没有产品评价！');
                        return
                    }
                    // 表格
                    for (var i = 0; i < this.SentimentRes['data']['daily_info'].length; i++){
                        this.comment_daily[i] = {
                            'time': this.SentimentRes['data']['daily_info'][i]['date'],
                            'number': this.SentimentRes['data']['daily_info'][i]['comment_number'],
                            'score': this.SentimentRes['data']['daily_info'][i]['average_score'],
                        }
                    }
                    console.log(this.comment_daily)
                    for (var i = 0; i < this.SentimentRes['data']['aspect_distribution'].length; i++){
                        this.comment_aspect[i] = {
                            'aspect': this.SentimentRes['data']['aspect_distribution'][i]['aspect'],
                            'number': this.SentimentRes['data']['aspect_distribution'][i]['number'],
                            'score': this.SentimentRes['data']['aspect_comments'][this.SentimentRes['data']['aspect_distribution'][i]['aspect']],
                        }
                    }
                    console.log(this.comment_aspect)
                    this.component_key += 1
                    // 只显示产品有的属性
                    this.varietyList = []
                    for(var index in this.SentimentRes['data']['aspect_details']){
                        this.varietyList[index] = this.SentimentRes['data']['aspect_details'][index]['aspect']
                    }
                    this.varietyValue = [this.varietyList[0]]
                    if (this.varietyValue.length > 0){
                        for(var index in this.SentimentRes['data']['aspect_details']){
                            if (this.SentimentRes['data']['aspect_details'][index]['aspect'] == this.varietyValue[0]){
                                this.$refs.pie2.initChart('情感分布','', this.SentimentRes['data']['aspect_details'][index]['sentiment_distribution'])
                                this.$refs.pie3.initChart('评价对象','', this.SentimentRes['data']['aspect_details'][index]['target_distribution'])
                                this.$refs.pie4.initChart('评价观点','', this.SentimentRes['data']['aspect_details'][index]['opinion_distribution'])
                                this.POSUnitList = this.SentimentRes['data']['aspect_details'][index]['positive_units']
                                this.NEUUnitList = this.SentimentRes['data']['aspect_details'][index]['neutral_units']
                                this.NEGUnitList = this.SentimentRes['data']['aspect_details'][index]['negative_units']
                                break
                            }
                        }
                    }
                })
            },
            clickDailyInfo(){
                this.getDailyInfoLoading = true
                let data = {}
                if (this.chandiValue){
                    if (this.chanpinValue){
                        if(this.startDate){
                            if(this.endDate){
                                data['location'] = this.chandiValue
                                data['variety'] = this.chanpinValue
                                data['start_date'] = this.startDate
                                data['end_date'] = this.endDate
                                getDailyInfo(data).then(res =>{
                                    this.getAnalysisDetailLoading = false
                                    this.$message({message:"获取成功", type:'success'})
                                    this.DailyInfoRes = res
                                    console.log(this.DailyInfoRes)
                                    this.$refs.bar0.initChart('消费热度','', this.DailyInfoRes['data'])
                                    this.$refs.line0.initChart('消费评价','', this.DailyInfoRes['data'])
                                    this.DailyInfoStatus = true
                                    if (res['data'] === undefined){
                                        this.$message.warning('时间段内没有产品评价！');
                                        return
                                    }
                                    // 表格
                                    for (var i = 0; i < res['data'].length; i++){
                                        this.comment_daily[i] = {
                                            'time': res['data'][i]['date'],
                                            'number': res['data'][i]['comment_number'],
                                            'score': res['data'][i]['average_score'],
                                        }
                                    }
                                    console.log(this.comment_daily)
                                    this.component_key += 1

                                    this.AnalysisInfoStatus = false
                                    this.AnalysisDetailStatus = false
                                    this.SentimentText = false
                                })
                            }
                            else{
                                this.$message.warning('请选择截止时间');
                            }
                        }
                        else{
                            this.$message.warning('请选择起始时间');
                        }
                    }
                    else{
                        this.$message.warning('请选择产品');
                    }
                }
                else{
                    this.$message.warning('请选择产地');
                }
                this.getDailyInfoLoading = false
            },
            clickAnalysisInfo(){
                this.getAnalysisInfoLoading = true
                let data = {}
                if (this.chandiValue){
                    if (this.chanpinValue){
                        if(this.startDate){
                            if(this.endDate){
                                data['location'] = this.chandiValue
                                data['variety'] = this.chanpinValue
                                data['start_date'] = this.startDate
                                data['end_date'] = this.endDate
                                getAnalysisInfo(data).then(res =>{
                                    this.getAnalysisDetailLoading = false
                                    this.$message({message:"获取成功", type:'success'})
                                    this.AnalysisInfoRes = res
                                    console.log(this.AnalysisInfoRes)
                                    this.$refs.pie0.initChart('评分分布','', this.AnalysisInfoRes['data']['score_distribution'])
                                    this.$refs.pie1.initChart('属性分布','', this.AnalysisInfoRes['data']['aspect_distribution'])
                                    this.purchaseAdvicesList = this.AnalysisInfoRes['data']['purchase_advices']
                                    this.plantAdvicesList = this.AnalysisInfoRes['data']['plant_advices']
                                    document.getElementById("ScoreText").innerHTML = this.AnalysisInfoRes['data']['score_text']
                                    document.getElementById("HeatText").innerHTML = this.AnalysisInfoRes['data']['heat_text']
                                    this.AnalysisInfoStatus = true
                                    if (res['data']['score_distribution'] === undefined){
                                        this.$message.warning('时间段内没有产品评价！');
                                        return
                                    }
                                    // 表格
                                    for (var i = 0; i < res['data']['score_distribution'].length; i++){
                                        this.comment_aspect[i] = {
                                            'aspect': res['data']['aspect_distribution'][i]['aspect'],
                                            'number': res['data']['aspect_distribution'][i]['number'],
                                        }
                                    }
                                    console.log(this.comment_aspect)
                                    this.component_key += 1

                                    this.DailyInfoStatus = false
                                    this.AnalysisDetailStatus = false
                                    this.SentimentText = false
                                })
                            }
                            else{
                                this.$message.warning('请选择截止时间');
                            }
                        }
                        else{
                            this.$message.warning('请选择起始时间');
                        }
                    }
                    else{
                        this.$message.warning('请选择产品');
                    }
                }
                else{
                    this.$message.warning('请选择产地');
                }
                this.getAnalysisInfoLoading = false
            },
            clickAnalysisDetail(){
                this.getAnalysisDetailLoading = true
                let data = {}
                if (this.chandiValue){
                    if (this.chanpinValue){
                        if(this.startDate){
                            if(this.endDate){
                                data['location'] = this.chandiValue
                                data['variety'] = this.chanpinValue
                                // console.log(typeof(this.startDate))
                                // console.log(this.startDate)
                                data['start_date'] = this.startDate
                                data['end_date'] = this.endDate
                                // console.log(data)
                                getAnalysisDetail(data).then(res =>{
                                    this.getAnalysisDetailLoading = false
                                    this.$message({message:"获取成功", type:'success'})
                                    this.AnalysisDetailRes = res
                                    console.log(this.AnalysisDetailRes)
                                    if (res['data']['aspect_details'] === undefined){
                                        this.$message.warning('时间段内没有产品评价！');
                                        return
                                    }
                                    // 只显示产品有的属性
                                    this.varietyList = []
                                    for(var index in this.AnalysisDetailRes['data']['aspect_details']){
                                        this.varietyList[index] = this.AnalysisDetailRes['data']['aspect_details'][index]['aspect']
                                    }
                                    this.varietyValue = [this.varietyList[0]]
                                    if (this.varietyValue.length > 0){
                                        for(var index in this.AnalysisDetailRes['data']['aspect_details']){
                                            if (this.AnalysisDetailRes['data']['aspect_details'][index]['aspect'] == this.varietyValue[0]){
                                                this.$refs.pie2.initChart('情感分布','', this.AnalysisDetailRes['data']['aspect_details'][index]['sentiment_distribution'])
                                                this.$refs.pie3.initChart('评价对象','', this.AnalysisDetailRes['data']['aspect_details'][index]['target_distribution'])
                                                this.$refs.pie4.initChart('评价观点','', this.AnalysisDetailRes['data']['aspect_details'][index]['opinion_distribution'])
                                                this.POSUnitList = this.AnalysisDetailRes['data']['aspect_details'][index]['positive_units']
                                                this.NEUUnitList = this.AnalysisDetailRes['data']['aspect_details'][index]['neutral_units']
                                                this.NEGUnitList = this.AnalysisDetailRes['data']['aspect_details'][index]['negative_units']
                                                break
                                            }
                                        }
                                    }
                                    this.AnalysisDetailStatus = true
                                    this.DailyInfoStatus = false
                                    this.AnalysisInfoStatus = false
                                    this.SentimentText = false
                                })
                            }
                            else{
                                this.$message.warning('请选择截止时间');
                            }
                        }
                        else{
                            this.$message.warning('请选择起始时间');
                        }
                    }
                    else{
                        this.$message.warning('请选择产品');
                    }
                }
                else{
                    this.$message.warning('请选择产地');
                }
                this.getAnalysisDetailLoading = false
            },
        }
    }
</script>

<style lang="scss">
table {
  border-collapse: collapse;
  width: 100%;
}
    .home-container {
        padding: 32px;
        background-color: #F7F8FA;
        // background-color: #F2F3F5;
        position: relative;

        .chart-wrapper {
        background: #fff;
        padding: 16px 16px 0;
        margin-bottom: 32px;
        }
    }
    .el-header, .el-footer {
        background-color: #FFFFFF;
        text-align: center;
        // font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
        font-size:30px;
        // font-wight:700;
        line-height: 60px;
    }
    // 情感分析内容
    .dataAnalysisBacground{
        padding: 20px;
        // margin: 0px 50px;
        // margin: 50px;
        background: white;
        // background: rgb(240, 242, 245);
    }
    .fenquCol{
        border-radius: 4px;
        background: rgb(240, 242, 245);
    }
    .fenqubiaoti{
        font-family: 'Inter';
        font-style: normal;
        font-weight: 400;
        font-size: 24px;
        line-height: 29px;
        display: flex;
        justify-content: center;
        /* align-items: center; */
        /* text-align: center;  */
        /* margin:auto; */
    }
    .fenqubiaotiRow{
        margin-top: 30px;
        margin-bottom: 20px;
    }
    .fenquxuanzekuangRow{
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .xuanzekuangshuoming{
        font-family: 'Inter';
        font-style: normal;
        font-weight: 400;
        font-size: 18px;
        line-height: 22px;
        display: flex;
        justify-content: center;
        padding-top: 8px;
    }
    .InfoButton{
        // display: flex;
        // justify-content: center;
        background-color: #165DFF;
    }
    .ResetButton{
        // display: flex;
        // justify-content: center;
        color: #000000;
        background-color: #F2F3F5;
        border-color: #F2F3F5;
    }
    .cardStyle{
        width: 80%;
        background: #F9F9F9;
        border: 1px solid #C4C4C4;
        box-sizing: border-box;
        border-radius: 10px;display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-left: 10%;
        margin-right: 10%;
    }
    /* .el-row {
        margin-bottom: 20px;
    }
    .el-col {
        border-radius: 4px;
    }
    .bg-purple-dark {
        background: #99a9bf;
    }
    .bg-purple {
        background: #d3dce6;
    }
    .bg-purple-light {
        background: #e5e9f2;
    }
    .grid-content {
        border-radius: 4px;
        min-height: 36px;
    }
    .row-bg {
        padding: 10px 0;
        background-color: #f9fafc;
    } */
</style>