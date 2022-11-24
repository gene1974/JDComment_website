<template>
    <div style="background:#F2F3F5 ;min-width:fit-content;">
        <div class="Background">
        <el-row :gutter="20" class="Background">
            <h2 style="margin:20px">数据展示</h2>
            <el-row class="fenquxuanzekuangRow" :gutter="20" style="margin-left:20px">
                <el-col :span="5">
                    <el-row>
                        <el-col :span="8"><div class="xuanzekuangshuoming">产品</div></el-col>
                        <el-col :span="16">
                            <el-select v-model="product" placeholder="请选择">
                                <el-option
                                v-for="item in productList" :key="item" :label="item" :value="item">
                                </el-option>
                            </el-select>
                        </el-col>
                    </el-row>
                    <!-- <el-row style="margin-top: 20px">
                        <el-col :span="8"><div class="xuanzekuangshuoming">数据数量</div></el-col>
                        <el-col :span="16">
                            <el-select v-model="pageSize" placeholder="请选择">
                                <el-option
                                v-for="item in pageSizeList" :key="item"  :label="item" :value="item">
                                </el-option>
                            </el-select>
                        </el-col>
                    </el-row> -->
                </el-col>
                <el-col :span="6">
                    <el-row>
                        <el-col :span="8"><div class="xuanzekuangshuoming">评价类别</div></el-col>
                        <el-col :span="16">
                            <el-select v-model="attribute" placeholder="请选择">
                                <el-option
                                v-for="item in attributeList" :key="item" :label="item" :value="item">
                                </el-option>
                            </el-select>
                        </el-col>
                    </el-row>
                </el-col>
                <el-col :span="6">
                    <el-row>
                        <el-col :span="8"><div class="xuanzekuangshuoming">情感极性</div></el-col>
                        <el-col :span="16">
                            <el-select v-model="polarity" placeholder="请选择">
                                <el-option
                                v-for="item in polarityList" :key="item" :label="item" :value="item">
                                </el-option>
                            </el-select>
                        </el-col>
                    </el-row>
                </el-col>
                <el-col :span="4">
                    <el-row>
                        <el-button type="primary" @click="clickQuery" class="InfoButton">查询</el-button>
                    </el-row>
                    <el-row style="margin-top: 10px">
                        <el-button type="primary" @click="clickReset" class="ResetButton">重置</el-button>
                    </el-row>
                </el-col>
            </el-row>
            <el-row :gutter="20" id="DetailComment" style="margin: 30px;margin-top: 10px;">
                <el-col :span="22" class="Background" style="text-align: center;">
                    <div class="xuanzekuangshuoming" style="font-weight:bold; margin: 20px">数据展示</div>
                    <el-table :data="database" :header-cell-style="{textAlign: 'center', color: 'black'}" :cell-style="{ textAlign: 'center', color: 'black'}" style="width: 100%; justify-content: center;">
                        <el-table-column prop="index" label="评论序号" width="100"></el-table-column>
                        <el-table-column prop="product" label="产品" width="150"></el-table-column>
                        <el-table-column prop="category" label="评价类别" width="150"></el-table-column>
                        <el-table-column prop="target" label="评价对象" width="200"></el-table-column>
                        <el-table-column prop="opinion" label="评价观点" width="200"></el-table-column>
                        <el-table-column prop="polarity" label="情感极性" width="150"></el-table-column>
                    </el-table>
                </el-col>
            </el-row>
        </el-row>
        </div>
    </div>
</template>

<script>
import {fetchPageHistory, fetchHistoryInfo, fetchPageHistoryFiltered} from '@/api/dataAnnotation.js'

  export default {
    data(){
        return{
            product: '大米',
            productList:['大米', '玉米', '花生', '番茄', '茶叶', '荸荠', '猕猴桃', '竹笋', '蜜柚', '茶油', '椪柑', '大蒜', '藕', '豆皮', '蜜茄'],
            attribute: '品质',
            attributeList:['价格', '品质', '色泽', '口感', '包装', '分量', '物流', '售后', '其他'],
            taskNum:'0',
            taskList: ['0', '1', '2', '3'],
            polarity: '全部',
            polarityList:['负向', '正向', '中立'],
            database: [],
            isValueList:['有效数据','无效数据'],
            rawData:null,
            tableData:[],
            pageData:{
                pageSize:20,
                pageSum:0,
                currentPage:0,
            },
            pageSize: 20,
            pageSizeList: [10, 20, 30, 40, 50]
        }
    },
    mounted() {
        // this.getDataSum()
        // this.getFirstPage()
    },
    methods: {
        clickReset(){
            this.database = []
            this.product = '大米'
            this.taskNum = '0'
            this.polarity = '全部'
        },
        clickQuery(){
            let data = {
                "product": this.product,
                "category": this.attribute,
                "polarity": this.polarity,
            }
            fetchPageHistoryFiltered(data).then(res => {
                console.log(res)
                this.database = res
            }).catch(err => {
                console.log(err);
                this.$message({message:"获取当前页标注数据失败", type:'error'})
            })
        },
        getDataSum(){
            let data = {"taskNum":this.taskNum}
            fetchHistoryInfo(data).then( res => {
                this.pageData.pageSum = res
            }).catch(err => {
                console.log(err);
                this.$message({message:"获取后端标注数据总数失败", type:'error'})
            });
        },
        handleSelect(key) {
            // console.log(key);
            this.taskNum = key
            // this.updateText()
            // this.updateCount()
            this.getDataSum()
            this.getNewPage()
        },
        getFirstPage(){
            let data = {"page": 0, "pageSize": 10, "taskNum":this.taskNum}
            // this.clickQuery()
            fetchPageHistory(data).then( res => {
                this.rawData = res
                // console.log(this.rawData)
                for(var i=0;i<this.rawData.length;i++){
                    this.tableData.push({})
                    this.tableData[i]['label'] = this.rawData[i]['comment_text']
                    this.tableData[i]['children'] = [{}]
                    this.tableData[i]['children'][0]['label'] = '产品分类：' + this.rawData[i]['comment_variety'] + '用户评分：' + this.rawData[i]['user_star']
                    this.tableData[i]['children'][0]['children'] = []
                    this.tableData[i]['children'][0]['children'].push({})
                    this.tableData[i]['children'][0]['children'][0]['label'] = '是否有效数据：' + this.isValueList[this.rawData[i]['tag']['isValue']]
                    if (parseInt(this.rawData[i]['tag']['isValue'])){
                        continue
                    }
                    this.tableData[i]['children'][0]['children'][0]['children'] = []
                    for(var j=0;j<this.rawData[i]['tag']['valueList'].length;j++){
                        // console.log('ok')
                        this.tableData[i]['children'][0]['children'][0]['children'].push({})
                        this.tableData[i]['children'][0]['children'][0]['children'][j]['label'] = '评价对象：'
                        if(this.rawData[i]['tag']['valueList'][j]['entity'].length){
                            for(var k=0; k<this.rawData[i]['tag']['valueList'][j]['entity'].length; k++){
                                this.tableData[i]['children'][0]['children'][0]['children'][j]['label'] += '    ' + this.rawData[i]['tag']['valueList'][j]['entity'][k]['str'] + '\u2003\u2003\u2003\u2003\u2003位置：' + this.rawData[i]['tag']['valueList'][j]['entity'][k]['start'] + '-' + this.rawData[i]['tag']['valueList'][j]['entity'][k]['end']
                            }
                        }
                        this.tableData[i]['children'][0]['children'][0]['children'][j]['children'] = []
                        this.tableData[i]['children'][0]['children'][0]['children'][j]['children'].push({})
                        this.tableData[i]['children'][0]['children'][0]['children'][j]['children'][0]['label'] = '观点表达：'
                        if(this.rawData[i]['tag']['valueList'][j]['evaluation'].length){
                            for(var k=0; k<this.rawData[i]['tag']['valueList'][j]['evaluation'].length; k++){
                                this.tableData[i]['children'][0]['children'][0]['children'][j]['children'][0]['label'] += '    ' + this.rawData[i]['tag']['valueList'][j]['evaluation'][k]['str'] + '\u2003\u2003\u2003\u2003\u2003位置：' + this.rawData[i]['tag']['valueList'][j]['evaluation'][k]['start'] + '-' + this.rawData[i]['tag']['valueList'][j]['evaluation'][k]['end']
                            }
                        }
                        this.tableData[i]['children'][0]['children'][0]['children'][j]['children'][0]['children'] = []
                        this.tableData[i]['children'][0]['children'][0]['children'][j]['children'][0]['children'].push({})
                        this.tableData[i]['children'][0]['children'][0]['children'][j]['children'][0]['children'][0]['label'] = '评价方面：' + this.attributeList[this.rawData[i]['tag']['valueList'][j]['attribute']] + '  ' + '情感极性：' + this.polarityList[this.rawData[i]['tag']['valueList'][j]['polarity']]
                    }
                }
                // console.log(this.tableData)
            }).catch(err => {
                console.log(err);
                this.$message({message:"获取当前页标注数据失败", type:'error'})
            })
        },
        getNewPage(){
            let data = {"page": this.pageData.currentPage, "pageSize": this.pageData.pageSize, "taskNum":this.taskNum}
            fetchPageHistory(data).then( res => {
                this.rawData = res
                console.log(this.rawData)
                this.tableData = []
                for(var i=0;i<this.rawData.length;i++){
                    this.tableData.push({})
                    this.tableData[i]['label'] = this.rawData[i]['comment_text']
                    this.tableData[i]['children'] = [{}]
                    this.tableData[i]['children'][0]['label'] = '产品分类：' + this.rawData[i]['comment_variety'] + '用户评分：' + this.rawData[i]['user_star']
                    this.tableData[i]['children'][0]['children'] = []
                    this.tableData[i]['children'][0]['children'].push({})
                    this.tableData[i]['children'][0]['children'][0]['label'] = '是否有效数据：' + this.isValueList[this.rawData[i]['tag']['isValue']]
                    if (parseInt(this.rawData[i]['tag']['isValue'])){
                        continue
                    }
                    this.tableData[i]['children'][0]['children'][0]['children'] = []
                    for(var j=0;j<this.rawData[i]['tag']['valueList'].length;j++){
                        // console.log('ok')
                        this.tableData[i]['children'][0]['children'][0]['children'].push({})
                        this.tableData[i]['children'][0]['children'][0]['children'][j]['label'] = '评价对象：'
                        if(this.rawData[i]['tag']['valueList'][j]['entity'].length){
                            for(var k=0; k<this.rawData[i]['tag']['valueList'][j]['entity'].length; k++){
                                this.tableData[i]['children'][0]['children'][0]['children'][j]['label'] += '    ' + this.rawData[i]['tag']['valueList'][j]['entity'][k]['str'] + '\u2003\u2003\u2003\u2003\u2003位置：' + this.rawData[i]['tag']['valueList'][j]['entity'][k]['start'] + '-' + this.rawData[i]['tag']['valueList'][j]['entity'][k]['end']
                            }
                        }
                        this.tableData[i]['children'][0]['children'][0]['children'][j]['children'] = []
                        this.tableData[i]['children'][0]['children'][0]['children'][j]['children'].push({})
                        this.tableData[i]['children'][0]['children'][0]['children'][j]['children'][0]['label'] = '观点表达：'
                        if(this.rawData[i]['tag']['valueList'][j]['evaluation'].length){
                            for(var k=0; k<this.rawData[i]['tag']['valueList'][j]['evaluation'].length; k++){
                                this.tableData[i]['children'][0]['children'][0]['children'][j]['children'][0]['label'] += '    ' + this.rawData[i]['tag']['valueList'][j]['evaluation'][k]['str'] + '\u2003\u2003\u2003\u2003\u2003位置：' + this.rawData[i]['tag']['valueList'][j]['evaluation'][k]['start'] + '-' + this.rawData[i]['tag']['valueList'][j]['evaluation'][k]['end']
                            }
                        }
                        this.tableData[i]['children'][0]['children'][0]['children'][j]['children'][0]['children'] = []
                        this.tableData[i]['children'][0]['children'][0]['children'][j]['children'][0]['children'].push({})
                        this.tableData[i]['children'][0]['children'][0]['children'][j]['children'][0]['children'][0]['label'] = '评价方面：' + this.attributeList[this.rawData[i]['tag']['valueList'][j]['attribute']] + '  ' + '情感极性：' + this.polarityList[this.rawData[i]['tag']['valueList'][j]['polarity']]
                    }
                }
                // console.log(this.tableData)
            }).catch(err => {
                console.log(err);
                this.$message({message:"获取当前页标注数据失败", type:'error'})
            })
        },
        annotatorChange(index){
            // console.log(index)
            this.$router.push({name:'annotatorChange', params:{rawData:this.rawData[index], taskNum:this.taskNum}})
        },
        handleNodeClick(data) {
        console.log(data);
      },
        handleSizeChange(val) {
            console.log(`每页 ${val} 条`);
            this.pageData.pageSize = val
            this.getNewPage()
            this.clickQuery()
        },
        handleCurrentChange(val) {
            console.log(`当前页: ${val}`);
            this.pageData.currentPage = val-1
            this.getNewPage()
            this.clickQuery()
        }
        },
    }
</script>


<style lang="scss">
    .Background{
        margin: 20px;
        background: white;
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
    .el-table-column{
        color:#000000;
    }
    .demo-table-expand {
        font-size: 0;
    }
    .demo-table-expand label {
        width: 90px;
        color: #99a9bf;
    }
    .demo-table-expand .el-form-item {
        margin-left: 5%;
        margin-right: 0;
        margin-bottom: 0;
        width: 50%;
    }
</style>