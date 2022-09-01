<template>
    <div>
        <el-menu
        :default-active="'0'"
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b">
            <el-menu-item index="0">task0</el-menu-item>
            <el-menu-item index="1">task1</el-menu-item>
            <el-menu-item index="2">task2</el-menu-item>
            <el-menu-item index="3">task3</el-menu-item>
            <el-menu-item index="4">task4</el-menu-item>
            <el-menu-item index="5">task5</el-menu-item>
            <el-menu-item index="6">task6</el-menu-item>
            <el-menu-item index="7">task7</el-menu-item>
            <el-menu-item index="8">task8</el-menu-item>
        </el-menu>
        <el-table
            :data="tableData"
            style="width: 100%">
            <el-table-column type="expand">
            <template slot-scope="props">
                <el-form label-position="left" inline class="demo-table-expand">
                <el-form-item>
                    <el-tree :data="props.row.children"  default-expand-all @node-click="handleNodeClick"></el-tree>
                    <el-button @click="annotatorChange(props.$index)">修改标注</el-button>
                </el-form-item>
                </el-form>
            </template>
            </el-table-column>
            <el-table-column
            label="文本"
            prop="label">
            </el-table-column>
        </el-table>
        <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="pageData.currentPage+1"
            :page-sizes="[10, 20, 30, 40]"
            :page-size="pageData.pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="pageData.pageSum">
        </el-pagination>
    </div>
</template>

<style>
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

<script>
import {fetchPageHistory, fetchHistoryInfo} from '@/api/dataAnnotation.js'

  export default {
    mounted() {
        this.getDataSum()
        this.getFirstPage()
    },
    methods: {
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
        },
        handleCurrentChange(val) {
            console.log(`当前页: ${val}`);
            this.pageData.currentPage = val-1
            this.getNewPage()
        }
        },
        //   default-expand-all
        data() {
            return {
                taskNum:'0',
                isValueList:['有效数据','无效数据'],
                attributeList:['价格', '品质', '色泽', '口感', '包装', '分量', '物流', '售后', '其他'],
                polarityList:['负向', '正向', '中立'],
                rawData:null,
                tableData:[],
                pageData:{
                    pageSize:10,
                    pageSum:0,
                    currentPage:0,
                }
            }
        }
    }
</script>