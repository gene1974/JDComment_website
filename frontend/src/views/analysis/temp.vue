<template>
  <div class="event-extraction">
    <el-row :gutter="30">
      <el-col :xs="12" :sm="12" :md="12" :lg="10" :xl="10">
        <el-tabs v-model="activeSubmitName" @tab-click="handleActiveSubmit">
          <el-tab-pane label="输入文本" name="text" style="font-size: 20px">
            <el-input
              type="textarea"
              :autosize="{ minRows: 10, maxRows: 30}"
              placeholder="请输入内容"
              style="font-size: 16px;"
              v-model="inputText">
            </el-input>
            
            <div style="padding-top: 10px;text-align:center">
              <el-button :loading="submitLoading" type="primary" @click="submitText">提交文本</el-button>
            </div>
          </el-tab-pane>
          
          
          <el-tab-pane label="上传文件" name="file">
            <el-upload
              class="upload"
              accept=".txt"
              ref="upload"
              :limit="1"
              :on-exceed="handleFileExceed"
              drag
              :auto-upload="false"
              action="http://101.6.69.238:5000/api/v1/postDataFile"
              :on-success="uploadSuccess"
              :on-error="uploadError"
              :file-list="fileList"
              >
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
              <div class="el-upload__tip" slot="tip">只能上传txt文件</div>
            </el-upload>
            
            <div style="padding-top: 10px;text-align:center">
              <el-button :loading="uploadLoading" type="primary" @click="submitUpload">上传文件</el-button>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-col>
      
      <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12">
        <el-row>
          <el-col :span="12">
            <div class="grid-content">
              事件抽取结果
            </div>
          </el-col>
          <!-- <el-col :span="12">
            <div class="grid-content download-result">
              <el-button style="float: right; padding: 3px 0" type="text" icon="el-icon-download"
              @click="handleDownload">
                导出结果
              </el-button>
            </div>
          </el-col> -->
        </el-row>
        
        <el-divider></el-divider>
        
        <div class="card-list" v-show="resultStatus === 1">
          
          <el-card  shadow="hover" class="box-card" v-for="item in textRes">
            <div slot="header" class="clearfix">
                <div>
                    <i class="el-icon-document" style="padding-right: 15px;"></i><span>{{item['comment_text']}}</span>
                </div>
                
            </div>
            <el-table
                :data="item['comment_units']"
                style="width: 100%">
                <el-table-column
                    prop="entity"
                    label="评价对象"
                    width="100">
                </el-table-column>
                <el-table-column
                    prop="evaluation"
                    label="观点表达"
                    width="100">
                </el-table-column>
                <el-table-column
                    prop="attribute"
                    label="评价方面"
                    width="100">
                </el-table-column>
                <el-table-column
                    prop="polarity"
                    label="情感极性">
                </el-table-column>
            </el-table>
          </el-card>
        </div>

        <data-statistics-pie ref="chart1"  v-show="resultStatus === 2"/>

      </el-col>
    </el-row>
  </div>
</template>

<script>
  import {getTextAnalysis} from '@/api/dataAnalysis.js'
  // import echarts from 'echarts'
  import DataStatisticsPie from './pie.vue'
  import { saveAs } from 'file-saver'
  
  export default {
    components: {
      DataStatisticsPie
    },
    data() {
      return {
        chart:null,
        inputText: '',
        fileList: [],
        submitLoading: false,
        uploadLoading: false,
        downloadLoading: false,
        textRes: [],
        fileRes: [],
        statistics_result:{},
        resultStatus: 0,
        activeSubmitName: 'text',
        tableData: [],
      }
    },
    mounted() {
      // this.$refs.chart1.initChart('123')
    },
    methods: {
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
        console.log(this.fileRes['statistics_result'])
        this.statistics_result = this.fileRes['statistics_result']
        let varietyData1 = []
        for (var key in this.statistics_result['variety']){
          varietyData1.push({'value':this.statistics_result['variety'][key]['count'], 'name':key})
        }
        this.$refs.chart1.initChart('类型分析结果', varietyData1)
        // this.$refs.chart1.setOption()
        this.resultStatus = 2
        // console.log(this.$refs)
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

<style scoped>
  .event-extraction {
    padding: 30px;
    padding-top: 50px;
  }
  .grid-content {
    /* background-color: red; */
    padding-top: 10px;
    border-radius: 4px;
    min-height: 36px;
    font-size: 20px;
    /* font-weight: bold; */
  }
  .download-result {
    float:right;
    padding-right: 20px;
  }
  .box-card {
    margin-bottom: 30px;
  }
  .card-list {
    height: 660px;
    overflow:auto;
  }
  /deep/ .el-tabs__item {
    font-size: 20px;
  }
  /deep/ .el-divider--horizontal {
    margin: 3px 0 15px 0;
    height: 2px;
    background-color: #E4E7ED;
  }
  /deep/ .el-card__body {
    padding: 5px 20px;
  }
</style>
