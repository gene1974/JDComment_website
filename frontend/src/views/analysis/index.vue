<template>
    <div style="background:#F2F3F5 ;min-width:fit-content;">
        <div class="dataAnalysisBacground">
            <el-row :gutter="20" class="dataAnalysisBacground">
                <h2 style="margin-left:40px">文本分析</h2>
            </el-row>
        </div>
        <div class="dataAnalysisBacground">
            <el-row :gutter="20">
                <el-col :span="14">
                    <h3 style="margin-left:40px">输入文本</h3>
                    <el-row style="margin:20px">
                        <el-input class="shuruwenbenkuang"
                        type="textarea"
                        :autosize="{ minRows: 10, maxRows: 30}"
                        placeholder="请输入内容"
                        style="font-size: 16px;"
                        v-model="inputText">
                        </el-input>
                        <el-button :loading="submitLoading" type="primary" @click="submitText" class="InfoButton">文本分析</el-button>
                    </el-row>
                </el-col>
                <!-- <el-col :span="9">
                    <h3 style="margin-left:40px">上传文件</h3>
                    <el-row style="margin:20px">
                        <el-upload
                        class="shangchuanwenjiankuang"
                        accept=".txt"
                        ref="upload"
                        :limit="1"
                        :on-exceed="handleFileExceed"
                        drag
                        :auto-upload="false"
                        action="http://101.6.69.215:9050/api/v1/postDataFile"
                        :on-success="uploadSuccess"
                        :on-error="uploadError"
                        :file-list="fileList"
                        >
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                        <div class="el-upload__tip" slot="tip">只能上传txt文件</div>
                        </el-upload>
                    </el-row>
                </el-col> -->
            </el-row>
        </div>
        <div class="dataAnalysisBacground" v-show="resultStatus">
            <el-row :gutter="20" style="margin:20px">
                <h3 style="margin:30px">结果展示</h3>
                <el-col :span="22" style="text-align: center;">
                    <div  max-height="450px;">
                        <el-table :header-cell-style="{textAlign: 'center', 'background-color': '#F2F3F5', color: '#000000'}" :cell-style="{textAlign: 'center', color: '#000000'}"
                            v-for="item in textRes" :data="item['comment_units']"
                            style="width: 100%" max-height="420px;">
                            <!-- <el-table-column label="编号" width="150"></el-table-column> -->
                            <el-table-column label="评价对象" prop="entity.text" width="150"></el-table-column>
                            <el-table-column label="观点表达" prop="evaluation.text" width="150"></el-table-column>
                            <el-table-column label="评价类别" prop="attribute" width="150"></el-table-column>
                            <el-table-column label="情感极性" prop="polarity" width="150"></el-table-column>
                        </el-table>
                    </div>
                </el-col>
            </el-row>
        </div>  
  </div>
</template>

<script>
  import {getTextAnalysis} from '@/api/dataAnalysis.js'
  import DataStatisticsPie0 from './pie0.vue'
  import DataStatisticsPie1 from './pie1.vue'
  import DataStatisticsBar0 from './bar0.vue'
  import { saveAs } from 'file-saver'
  
  export default {
    components: {
      DataStatisticsPie0,
      DataStatisticsPie1,
      DataStatisticsBar0,
    },
    data() {
      return {
        chart:null,
        inputText: '',
        fileList: [],
        submitLoading: false,
        uploadLoading: false,
        downloadLoading: false,
        resultStatus: 0,
        
        textRes: [],
        // wenjianResultStatus: 0,
        activeSubmitName: 'text',
        wenbenneirongkeshihua: [],
        zhengxiangqinggankeshihua: [],
        zhongxingqinggankeshihua: [],
        fuxiangqinggankeshihua: [],

        fileRes: [],
        statistics_result:{},
        siyuanzu_result: [],
        tableData_all: [],
        tableData: [],
        wenjiansiyuanzu_pageSize: 8,
        wenjiansiyuanzu_currentPage: 0,
        currentRow: null,
        wenjianneirongkeshihua_list: [],
        wenjianneirongkeshihua_index: 0,
        wenjianneirongkeshihua_pageSize: 1,
        wenjianneirongkeshihua_text: [],
        wenjianzhengxiangqinggankeshihua: [],
        wenjianzhongxingqinggankeshihua: [],
        wenjianfuxiangqinggankeshihua: [],
        wenjian_variety: null,
        wenjian_aspect: null,
        wenjian_polarity: null,
        wenjian_target: null,
        wenjiankeshihuaStatus: 0,
        
      }
    },
    mounted() {
      // this.$refs.chart1.initChart('123')
    },
    methods: {
      handleWenjiankeshihuaCurrentChange(val){
        this.wenjianneirongkeshihua_index = val - 1
        this.wenjianneirongkeshihua_text = []
        this.wenjianzhengxiangqinggankeshihua = []
        this.wenjianzhongxingqinggankeshihua = []
        this.wenjianfuxiangqinggankeshihua = []
        let temp_list = []
        for (var unit in this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units']){
          let temp_unit = {}
          // console.log(unit)
          if(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['entity']['tail']){
            temp_list.push([parseInt(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['entity']['head']),parseInt(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['entity']['tail']),'ENTITY'])
            temp_unit['entity'] =[parseInt(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['entity']['head']),parseInt(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['entity']['tail']),'ENTITY']
          }
          else{
            temp_unit['entity'] =[0,0,'ENTITY']
          }
          if(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['evaluation']['tail']){
            temp_list.push([parseInt(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['evaluation']['head']),parseInt(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['evaluation']['tail']),this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['polarity']])
            temp_unit['evaluation'] = [parseInt(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['evaluation']['head']),parseInt(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['evaluation']['tail']),this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['polarity']]
          }
          else{
            temp_unit['evaluation'] =[0,0,'ENTITY']
          }
          if (this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['polarity'] == 'POS'){
            this.wenjianzhengxiangqinggankeshihua.push(temp_unit)
          }
          else{
            if (this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['polarity'] == 'NEU'){
              this.wenjianzhongxingqinggankeshihua.push(temp_unit)
            }
            else{
              this.wenjianfuxiangqinggankeshihua.push(temp_unit)
            }
          }
        }
        // console.log(this.wenjianzhengxiangqinggankeshihua)
        // console.log(this.wenjianzhongxingqinggankeshihua)
        // console.log(this.wenjianfuxiangqinggankeshihua)
        temp_list.sort(function(a,b){
          if (a[0] > b[0]) return 1 
          else if (a[0] < b[0]) return -1 
          else return 0})
        // console.log(temp_list)
        let temp_index = 0
        for (var i in temp_list){
          if (temp_list[i][0] > temp_index){
            this.wenjianneirongkeshihua_text.push([temp_index,temp_list[i][0],'NORMAL'])
            temp_index = temp_list[i][0]
          }
          if (temp_index < temp_list[i][1]){
            this.wenjianneirongkeshihua_text.push([temp_index,temp_list[i][1],temp_list[i][2]])
            temp_index = temp_list[i][1]
          }
        }
        this.wenjianneirongkeshihua_text.push([temp_index,this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_text'].length,'NORMAL'])
      
      },
      tableRowClassName({row, rowIndex}) {
          row.row_index = rowIndex;
      },
      onRowClick (row, event, column) {
          this.currentRow = row.row_index;
          // console.log(this.currentRow)
      },
      handleCurrentChange(val) {
        // console.log(`当前页: ${val}`);
        this.wenjiansiyuanzu_currentPage = val - 1
        if (val*this.wenjiansiyuanzu_pageSize > this.tableData_all.length){
          this.tableData = this.tableData_all.slice(this.wenjiansiyuanzu_currentPage*this.wenjiansiyuanzu_pageSize,this.tableData_all.length)
        }
        else{
          this.tableData = this.tableData_all.slice(this.wenjiansiyuanzu_currentPage*this.wenjiansiyuanzu_pageSize,val*this.wenjiansiyuanzu_pageSize)
        }
      },
      addClass(item){return item[2]},
      handleActiveSubmit(tab, event) {
        // console.log(tab, event);
      },
      uploadError() {
        this.$message({message:"文件上传发生错误", type:'error'})
        this.uploadLoading = false
        this.$refs.upload.clearFiles();
      },
      uploadSuccess(response, file, fileList) {
        this.$message({message:"抽取成功", type:'success'})
        console.log(response)
        this.fileRes = response
        this.uploadLoading = false
        this.$refs.upload.clearFiles();
        // console.log(this.fileRes['statistics_result'])
        this.statistics_result = this.fileRes['statistics_result']
        this.siyuanzu_result = this.fileRes['siyuanzu_result']
        // console.log(this.tableData_all)
        this.tableData_all = this.siyuanzu_result
        this.tableData = this.tableData_all.slice(0,8)
        this.wenjianneirongkeshihua_list = new Array(this.fileRes['comment_result'].length).fill(1).map((v, i) => i)
        // console.log(this.wenjianneirongkeshihua_list)
        this.wenjianneirongkeshihua_text = []
        this.wenjianzhengxiangqinggankeshihua = []
        this.wenjianzhongxingqinggankeshihua = []
        this.wenjianfuxiangqinggankeshihua = []
        let temp_list = []
        for (var unit in this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units']){
          let temp_unit = {}
          // console.log(unit)
          if(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['entity']['tail']){
            temp_list.push([parseInt(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['entity']['head']),parseInt(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['entity']['tail']),'ENTITY'])
            temp_unit['entity'] =[parseInt(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['entity']['head']),parseInt(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['entity']['tail']),'ENTITY']
          }
          else{
            temp_unit['entity'] =[0,0,'ENTITY']
          }
          if(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['evaluation']['tail']){
            temp_list.push([parseInt(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['evaluation']['head']),parseInt(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['evaluation']['tail']),this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['polarity']])
            temp_unit['evaluation'] = [parseInt(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['evaluation']['head']),parseInt(this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['evaluation']['tail']),this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['polarity']]
          }
          else{
            temp_unit['evaluation'] =[0,0,'ENTITY']
          }
          if (this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['polarity'] == 'POS'){
            this.wenjianzhengxiangqinggankeshihua.push(temp_unit)
          }
          else{
            if (this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_units'][unit]['polarity'] == 'NEU'){
              this.wenjianzhongxingqinggankeshihua.push(temp_unit)
            }
            else{
              this.wenjianfuxiangqinggankeshihua.push(temp_unit)
            }
          }
        }
        // console.log(this.wenjianzhengxiangqinggankeshihua)
        // console.log(this.wenjianzhongxingqinggankeshihua)
        // console.log(this.wenjianfuxiangqinggankeshihua)
        temp_list.sort(function(a,b){
          if (a[0] > b[0]) return 1 
          else if (a[0] < b[0]) return -1 
          else return 0})
        // console.log(temp_list)
        let temp_index = 0
        for (var i in temp_list){
          if (temp_list[i][0] > temp_index){
            this.wenjianneirongkeshihua_text.push([temp_index,temp_list[i][0],'NORMAL'])
            temp_index = temp_list[i][0]
          }
          if (temp_index < temp_list[i][1]){
            this.wenjianneirongkeshihua_text.push([temp_index,temp_list[i][1],temp_list[i][2]])
            temp_index = temp_list[i][1]
          }
        }
        this.wenjianneirongkeshihua_text.push([temp_index,this.fileRes['comment_result'][this.wenjianneirongkeshihua_list[this.wenjianneirongkeshihua_index]]['comment_text'].length,'NORMAL'])
        // let pieData0 = []
        // for (var key in this.statistics_result['variety']){
        //   pieData0.push({'value':this.statistics_result['variety'][key]['count'], 'name':key, 'user_stars':(this.statistics_result['variety'][key]['user_stars']/this.statistics_result['variety'][key]['count']).toFixed(2)})
        // }
        // this.$refs.pie0.initChart('产品种类及其平均评分','（含无效评论数据）', pieData0)
        let pieData1 = []
        for (var key in this.statistics_result['variety']['花生']['polarity']){
          pieData1.push({'value':this.statistics_result['variety']['花生']['polarity'][key], 'name':key})
        }
        this.$refs.pie1.initChart('三元组情感极性分布','', pieData1)
        let barData0 = {}
        for (var key in this.statistics_result['variety']['花生']['aspect']){
          barData0[key] = {'POS':0,'NEU':0,'NEG':0}
          for (var pol in this.statistics_result['variety']['花生']['aspect'][key]['polarity']){
            barData0[key][pol] = this.statistics_result['variety']['花生']['aspect'][key]['polarity'][pol]
          }
          // pieData1.push({'value':this.statistics_result['variety']['花生']['aspect'][key], 'name':key})
        }
        this.$refs.bar0.initChart('评价方面情感极性分布','', barData0)
      
        
        // let varietyData1 = []
        // for (var key in this.statistics_result['variety']){
        //   varietyData1.push({'value':this.statistics_result['variety'][key]['count'], 'name':key})
        // }
        // this.$refs.chart1.initChart('类型分析结果', varietyData1)
        this.resultStatus = 2
      },
      submitUpload() {
        if(this.$refs.upload.uploadFiles.length <= 0){
            this.$message.error("请选择文件");
        }
        else{
            this.uploadLoading = true
            this.$refs.upload.submit()
        }
      },
      handleFileExceed(files, fileList) {
        this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
      },
    //   handleDownload () {
    //     let data = JSON.stringify(this.fileRes, null, 2);
    //     let blob = new Blob([data], {type: "text/plain;charset=utf-8"});
    //     saveAs(blob, "事件抽取结果.json");
    //   },
      submitText() {
        this.submitLoading = true
        let data = {'data_list': []}
        data['data_list'].push({'comment_text': this.inputText })
        getTextAnalysis(data).then(res => {
          this.$message({message:"抽取成功", type:'success'})
          this.textRes = res
          console.log(this.textRes)
          // console.log(this.textRes[0])
          this.wenbenneirongkeshihua = []
          this.zhengxiangqinggankeshihua = []
          this.zhongxingqinggankeshihua = []
          this.fuxiangqinggankeshihua = []
          let temp_list = []
          for (var unit in this.textRes[0]['comment_units']){
            let temp_unit = {}
            // console.log(unit)
            if(this.textRes[0]['comment_units'][unit]['entity']['tail']){
              temp_list.push([parseInt(this.textRes[0]['comment_units'][unit]['entity']['head']),parseInt(this.textRes[0]['comment_units'][unit]['entity']['tail']),'ENTITY'])
              temp_unit['entity'] =[parseInt(this.textRes[0]['comment_units'][unit]['entity']['head']),parseInt(this.textRes[0]['comment_units'][unit]['entity']['tail']),'ENTITY']
            }
            else{
              temp_unit['entity'] =[0,0,'ENTITY']
            }
            if(this.textRes[0]['comment_units'][unit]['evaluation']['tail']){
              temp_list.push([parseInt(this.textRes[0]['comment_units'][unit]['evaluation']['head']),parseInt(this.textRes[0]['comment_units'][unit]['evaluation']['tail']),this.textRes[0]['comment_units'][unit]['polarity']])
              temp_unit['evaluation'] = [parseInt(this.textRes[0]['comment_units'][unit]['evaluation']['head']),parseInt(this.textRes[0]['comment_units'][unit]['evaluation']['tail']),this.textRes[0]['comment_units'][unit]['polarity']]
            }
            else{
              temp_unit['evaluation'] =[0,0,'ENTITY']
            }
            if (this.textRes[0]['comment_units'][unit]['polarity'] == 'POS'){
              this.zhengxiangqinggankeshihua.push(temp_unit)
            }
            else{
              if (this.textRes[0]['comment_units'][unit]['polarity'] == 'NEU'){
                this.zhongxingqinggankeshihua.push(temp_unit)
              }
              else{
                this.fuxiangqinggankeshihua.push(temp_unit)
              }
            }
          }
          // console.log(this.zhengxiangqinggankeshihua)
          // console.log(this.zhongxingqinggankeshihua)
          // console.log(this.fuxiangqinggankeshihua)
          temp_list.sort(function(a,b){
            if (a[0] > b[0]) return 1 
            else if (a[0] < b[0]) return -1 
            else return 0})
          // console.log(temp_list)
          let temp_index = 0
          for (var i in temp_list){
            if (temp_list[i][0] > temp_index){
              this.wenbenneirongkeshihua.push([temp_index,temp_list[i][0],'NORMAL'])
              temp_index = temp_list[i][0]
            }
            if (temp_index < temp_list[i][1]){
              this.wenbenneirongkeshihua.push([temp_index,temp_list[i][1],temp_list[i][2]])
              temp_index = temp_list[i][1]
            }
            // this.wenbenneirongkeshihua.push([temp_index,temp_list[i][1],temp_list[i][2]])
            // temp_index = temp_list[i][1]
          }
          this.wenbenneirongkeshihua.push([temp_index,this.textRes[0]['comment_text'].length,'NORMAL'])
          // console.log(this.wenbenneirongkeshihua)
          this.submitLoading = false
          this.resultStatus = 1
        }).catch(err => {
          this.$message({message: err, type:'error'})
          this.submitLoading = false
        })
      },
    }
  }
</script>

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
        margin: 20px;
        background: white;
    }
    .InfoButton{
        // display: flex;
        // justify-content: center;
        background-color: #165DFF;
    }
.sentiment-analysis {
  background: rgb(240, 242, 245);
  // padding: 32px;
  height: 995px;
  width: 2220px;

  .shuruwenben {
    position: absolute;
    width: 185px;
    height: 35px;
    left: 78px;
    top: 173px;

    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 24px;
    line-height: 29px;
    display: flex;
    align-items: center;
  }
  .shuruwenbenshuoming {
    position: absolute;
    width: 240px;
    height: 35px;
    left: 213px;
    top: 173px;

    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 18px;
    line-height: 22px;
    display: flex;
    align-items: center;

    color: #ABABAB;
  }
  .shuruwenbenkuang {
    position: absolute;
    width: 360px;
    height: 294px;
    left: 70px;
    top: 229px;

    background: rgb(240, 242, 245);
  }
  .dantiaofenxibutton{
    position: absolute;
    width: 113px;
    height: 45px;
    left: 300px;
    top: 490px;

    background: #175BD1;
    border-radius: 6px;
  }
  .shangchuanwenjian{
    position: absolute;
    width: 185px;
    height: 35px;
    left: 78px;
    top: 573px;

    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 24px;
    line-height: 29px;
    display: flex;
    align-items: center;
  }
  .shangchuanwenjianshuoming{
    position: absolute;
    width: 240px;
    height: 35px;
    left: 213px;
    top: 573px;

    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 18px;
    line-height: 22px;
    display: flex;
    align-items: center;

    color: #ABABAB;
  }
  .shangchuanwenjiankuang{
    position: absolute;
    width: 190px;
    height: 190px;
    left: 70px;
    top: 629px;

    background: rgb(240, 242, 245);
  }
  .piliangfenxibutton{
    position: absolute;
    width: 113px;
    height: 45px;
    left: 300px;
    top: 820px;

    background: #175BD1;
    border-radius: 6px;
  }
  .jieguozhanshi{
    position: absolute;
    width: 185px;
    height: 35px;
    left: 479px;
    top: 173px;

    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 24px;
    line-height: 29px;
    display: flex;
    align-items: center;
  }
  .jieguozhanshikuang{
    position: absolute;
    width: 1308px;
    height: 651px;
    left: 460px;
    top: 230px;

    background: #FFFFFF;
  }
  .siyuanzuline{
    position: absolute;
    width: 2px;
    height: 29px;
    left: 512px;
    top: 265px;

    background:#000000
  }
  .siyuanzu{
    position: absolute;
    width: 185px;
    height: 35px;
    left: 523px;
    top: 262px;

    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 20px;
    line-height: 24px;
    display: flex;
    align-items: center;
  }
  .chanpin{
    position: absolute;
    width: 95px;
    height: 35px;
    left: 524px;
    top: 326px;

    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 18px;
    line-height: 22px;
    display: flex;
    align-items: center;

  }
  .siyuanzucard{
    position: absolute;
    width: 494px;
    // height: 323px;
    left: 523px;
    top: 365px;

    background: #F9F9F9;
    border: 1px solid #C4C4C4;
    box-sizing: border-box;
    border-radius: 10px;
  }
  .siyuanzuicon{
    padding-right: 5px;
  }
  .keshihuajieguoline{
    position: absolute;
    width: 3px;
    height: 29px;
    left: 1063px;
    top: 265px;

    background:#000000
  }
  .keshihuajieguo{
    position: absolute;
    width: 185px;
    height: 35px;
    left: 1074px;
    top: 262px;

    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 20px;
    line-height: 24px;
    display: flex;
    align-items: center;
  }
  .wenbenneirong{
    position: absolute;
    width: 95px;
    height: 35px;
    left: 1074px;
    top: 320px;

    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 18px;
    line-height: 22px;
    display: flex;
    align-items: center;
  }
  .wenbenneirongcard{
    position: absolute;
    width: 641px;
    // height: 323px;
    left: 1074px;
    top: 363px;

    background: #F9F9F9;
    border: 1px solid #C4C4C4;
    box-sizing: border-box;
    border-radius: 10px;
  }
  .wenbenneirongcontent{
    // width: 601px;
    // height: 57px;

    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 18px;
    line-height: 30px;
    /* or 167% */


    color: #595959;

  }
  .NORMAL{
    background-color: #F9F9F9;
  }
  .ENTITY{
    padding:0 7px;
    border-radius: 15px;
    background-color: #D3D3D3;
  }
  .POS{
    padding:0 7px;
    border-radius: 15px;
    background-color: #D0EDE0;
  }
  .NEU{
    padding:0 7px;
    border-radius: 15px;
    background-color: #EDEDD0;
  }
  .NEG{
    padding:0 7px;
    border-radius: 15px;
    background-color: #EDD7D0;
  }
  .qingganjixingfenbu{
    position: absolute;
    width: 118px;
    height: 35px;
    left: 1074px;
    top: 492px;

    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 18px;
    line-height: 22px;
    display: flex;
    align-items: center;
  }
  .qingganjixingfenbucard{
    position: absolute;
    width: 641px;
    // height: 253px;
    left: 1074px;
    top: 532px;

    background: #F9F9F9;
    border: 1px solid #C4C4C4;
    box-sizing: border-box;
    border-radius: 10px;
  }
  .qingganjixing{
    // width: 95px;
    // height: 35px;
    // left: 1318px;
    // top: 721px;
    font-weight:bold;
    padding: 30px 50px;
    

    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 18px;
    line-height: 22px;
    display: flex;
    align-items: center;
    text-align: center;
  }

  .zhengxiangbackground{
    position: absolute;
    width: 60px;
    height: 50px;
    left: 57px;
    top: 36px;
  }
  .zhongxingbackground{
    position: absolute;
    width: 60px;
    height: 50px;
    left: 57px;
    top: 117px;
  }
  .fuxiangbackground{
    position: absolute;
    width: 60px;
    height: 50px;
    left: 57px;
    top: 200px;
  }
  .wenjianfenxikeshihuashuoming{
    position: absolute;
    width: 485px;
    height: 35px;
    left: 600px;
    top: 173px;

    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 18px;
    line-height: 22px;
    display: flex;
    align-items: center;

    color: #ABABAB;
  }
  .wenjiansiyuanzucard{
    position: absolute;
    width: 658px;
    // height: 457px;
    left: 490px;
    top: 336px;

    background: #F9F9F9;
    border: 1px solid #C4C4C4;
    box-sizing: border-box;
    border-radius: 10px;
  }
  .wenjiankeshihuajieguoline{
    position: absolute;
    width: 3px;
    height: 29px;
    left: 1181px;
    top: 265px;

    background:#000000
  }
  .wenjiankeshihuajieguo{
    position: absolute;
    width: 185px;
    height: 35px;
    left: 1192px;
    top: 262px;

    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 20px;
    line-height: 24px;
    display: flex;
    align-items: center;
  }
  .wenjianwenbenneirongcard{
    position: absolute;
    width: 550px;
    // height: 323px;
    left: 1192px;
    top: 336px;

    background: #F9F9F9;
    border: 1px solid #C4C4C4;
    box-sizing: border-box;
    border-radius: 10px;
  }
  .tubiaobiaoti{
    position: absolute;
    width: 217px;
    height: 71px;
    left: 1192px;
    top: 486px;

    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 18px;
    line-height: 22px;
    display: flex;
    align-items: center;

    color: #000000;
  }
  .tubiaobiaotibuchong{
    position: absolute;
    width: 217px;
    height: 71px;
    left: 1192px;
    top: 506px;

    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 22px;
    display: flex;
    align-items: center;

    color: #ABABAB;
  }
  .wenjianPie0{
    position: absolute;
    // width: 217px;
    height: 381px;
    left: 1192px;
    top: 486px;
  }
  .wenjianPie1{
    position: absolute;
    // width: 217px;
    height: 381px;
    left: 1152px;
    top: 486px;
  }
  .wenjianBar0{
    position: absolute;
    // width: 217px;
    height: 381px;
    left: 1450px;
    top: 486px;
  }
}
</style>
