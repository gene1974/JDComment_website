<template>

  
    <div style="background: rgb(240, 242, 245);">
        <div class="home-container">
            <el-header>知识图谱展示</el-header>
        </div>
        <div style="margin: 20px;color:slategrey">本体图谱：</div>
        <div style="margin: 10px; margin-left:20px; color:slategrey">· 层次化展示农产品评价类别</div>
        <!-- <div style="margin: 10px; margin-left:20px; color:slategrey">· 分析概览：用户满意度分布、用户评价类别分布</div>
        <div style="margin: 10px; margin-left:20px; color:slategrey">· 分析详情：产品每一类属性的用户评价分析</div>    -->

        <div style="background: rgb(240, 242, 245);">
            <el-row style="margin:20px; margin-top:0px" type="flex" justify="space-around">
                <!-- 本体图谱 -->
                <el-col :span="12">
                    <kg-ontology ref="KGOntology"/>
                </el-col>
                <!-- 产品图谱 -->
                <el-col :span="12">
                    <el-row :gutter="30"  class="dataAnalysisBacground">
                        <el-col :span="6">
                            <el-row>
                                <el-col :span="6"><div class="xuanzekuangshuoming">产品</div></el-col>
                                <el-col :span="18">
                                    <el-select v-model="chanpinValue" placeholder="请选择">
                                        <el-option
                                        v-for="item in chanpinList"
                                        :key="item"
                                        :label="item"
                                        :value="item">
                                        </el-option>
                                    </el-select>
                                </el-col>
                            </el-row>
                        </el-col>
                        <el-col :span="4">
                            <el-button :loading="getProductGraph" type="primary" @click="clickProduct" class="DailyInfoButton">获取产品图谱</el-button>
                        </el-col>
                    </el-row>
                    <!-- 分析信息 -->
                    <el-row :gutter="30"  class="dataAnalysisBacground">
                        <el-card style="margin:20px;">
                            <p>本系统对于农产品2022年度的评价信息进行了整体分析。</p>
                            <p id="year_comment"></p>
                        </el-card>
                    </el-row>
                    <!-- <el-row v-show="getProductGraph"> -->
                    <el-row>
                        <kg-product ref="KgProduct"/>
                    </el-row>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
    import {getProductGraph} from '@/api/knowledgeGraph.js'
    import KgOntology from './ontology.vue'
    import KgProduct from './product.vue'
    export default {
        components: {
            KgOntology,
            KgProduct,
        },
        data() {
        return {
            chanpinValue:'大米',
            chanpinList:['大米', '番茄', '茶叶', '荸荠', '猕猴桃', '竹笋', '蜜柚', '茶油', '椪柑', '大蒜', '藕', '豆皮', '蜜茄'],
            // chanpinList:['大米', '番茄', '茶叶', '荸荠', '油茶', '猕猴桃', '竹笋', '红米', '蜜柚', '茶油', '贡米', '炒青', '椪柑', '大蒜', '白肉姜', '红心脚板薯', '藕', '酱姜', '豆皮', '橙皮', '蜜茄'],
            // chanpinList:['大米','番茄','茶叶'],
            getProductGraph:false,
        }
        },
        methods: {
            clickProduct(){
                this.getProductGraph = true
                let data = {}
                if (this.chanpinValue){
                    data['variety'] = this.chanpinValue
                    // this.$refs.KgProduct.initChart('产品图谱','', this.chanpinValue)
                    getProductGraph(data).then(res =>{
                        this.getAnalysisDetailLoading = false
                        this.$message({message:"获取成功", type:'success'})
                        this.ProductRes = res
                        console.log(this.ProductRes)
                        document.getElementById('year_comment').innerText = res['comment_data']
                        this.$refs.KgProduct.initChart(this.chanpinValue, '', res['graph_data'])
                        // this.$refs.KgProduct.initChart('产品图谱','', res['data']['graph_data'])
                    })
                    }
                else{
                    this.$message.warning('请选择产品');
                }
                this.getProductGraph = false
            },
        }
    }
</script>

<!-- <script>
    import {getDailyInfo} from '@/api/dataAnalysis.js'
    import {getAnalysisInfo} from '@/api/dataAnalysis.js'
    import {getAnalysisDetail} from '@/api/dataAnalysis.js'
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
            startDate:'2021-07-01',
            endDate:'2021-07-30',
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
        }
        },
        mounted() {
        // this.$refs.chart1.initChart('123')
        },
        methods: {
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
                            document.getElementById("DetailNone").style.visibility = 'hidden'
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
                    document.getElementById("DetailNone").style.visibility = 'visible'
                }
                else{
                    document.getElementById("DetailComment").style.visibility = 'hidden'
                    document.getElementById("DetailPie").style.visibility = 'hidden'
                    document.getElementById("DetailNone").style.visibility = 'hidden'
                }
            },
            clickAll(){
                this.clickDailyInfo(),
                this.clickAnalysisInfo(),
                this.clickAnalysisDetail()
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
                                // console.log(typeof(this.startDate))
                                // console.log(this.startDate)
                                data['start_date'] = this.startDate
                                data['end_date'] = this.endDate
                                // console.log(data)
                                getDailyInfo(data).then(res =>{
                                    this.getAnalysisDetailLoading = false
                                    this.$message({message:"获取成功", type:'success'})
                                    this.DailyInfoRes = res
                                    console.log(this.DailyInfoRes)
                                    this.$refs.bar0.initChart('消费热度','', this.DailyInfoRes['data'])
                                    this.$refs.line0.initChart('消费评价','', this.DailyInfoRes['data'])
                                    this.DailyInfoStatus = true
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
                                // console.log(typeof(this.startDate))
                                // console.log(this.startDate)
                                data['start_date'] = this.startDate
                                data['end_date'] = this.endDate
                                // console.log(data)
                                getAnalysisInfo(data).then(res =>{
                                    this.getAnalysisDetailLoading = false
                                    this.$message({message:"获取成功", type:'success'})
                                    this.AnalysisInfoRes = res
                                    console.log(this.AnalysisInfoRes)
                                    this.$refs.pie0.initChart('评分分布','', this.AnalysisInfoRes['data']['score_distribution'])
                                    this.$refs.pie1.initChart('属性分布','', this.AnalysisInfoRes['data']['aspect_distribution'])
                                    // this.purchaseAdvicesList = this.AnalysisInfoRes['data']['purchase_advices']
                                    // this.plantAdvicesList = this.AnalysisInfoRes['data']['plant_advices']
                                    // this.plantAdvicesList = Object(['暂无'])
                                    this.AnalysisInfoStatus = true
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
                                    // this.purchaseAdvicesList = this.AnalysisDetailRes['data']['purchase_advices']
                                    // this.plantAdvicesList = this.AnalysisDetailRes['data']['plant_advices']
                                    // // console.log(this.purchaseAdvicesList)
                                    // this.$refs.pie0.initChart('评分分布','', this.AnalysisInfoRes['data']['score_distribution'])
                                    // this.$refs.pie1.initChart('属性分布','', this.AnalysisInfoRes['data']['aspect_distribution'])
                                    // this.AnalysisInfoStatus = true
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
</script> -->

<style lang="scss" scoped>
    .home-container {
        padding: 32px;
        background-color: rgb(240, 242, 245);
        position: relative;

        .chart-wrapper {
        background: #fff;
        padding: 16px 16px 0;
        margin-bottom: 32px;
        }
    }
    .el-header, .el-footer {
        background-color: #B3C0D1;
        color: #333;
        text-align: center;
        // font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
        font-size:30px;
        // font-wight:700;
        line-height: 60px;
    }
    .dataAnalysisBacground{
        /* margin-top: 20px; */
        /* margin-bottom: 20px; */
        margin: 0px 50px;
        /* background: white; */
        /* background: rgb(240, 242, 245); */
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
        margin-top: 30px;
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
    .DailyInfoButton{
        display: flex;
        justify-content: center;
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
</style>