<template>
  <div class="annotator-container">
    
    <div style="padding: 50px 130px 30px 80px;">
      <!-- 标注数据：{{labeled_cnt}} 未标注数据：{{unlabeled_cnt}}
      <el-progress :text-inside="true" :stroke-width="24" :percentage="labelPercentage" style="padding-top: 6px;"></el-progress> -->
    </div>
    
    <el-row :gutter="25" type="flex" justify="center">
      <el-col :span="10">
        <div class="raw-text-container grid-content">
          <div class="title" v-text="'产品分类：'+ comment_variety + '\u2003\u2003\u2003\u2003\u2003' + '用户评分：' + user_star"></div>
          <div class="line" />
          <div class="raw-text" @mouseup="saveRangeList">
            {{text}}
          </div>
        </div>
      </el-col>
      <el-col :span="10">
        <div class="event-list-container grid-content">
          <div class="event-list">
            <div class="title">标注</div>
            <div class="line" />
            <table class="gridtable">
              <tr>
                <th>是否有效数据</th>
                <td colspan="3">
                    <template>
                      <el-radio-group v-model="tag.isValue">
                        <el-radio label=0>有效数据</el-radio>
                        <el-radio label=1>无效数据</el-radio>
                      </el-radio-group>
                    </template>
                  </td>
              </tr>
            </table>
            <table class="gridtable" :key="index" v-for="(value,index) in tag.valueList">
              <col style="width: 25%" />
              <col style="width: 25%" />
              <col style="width: 25%" />
              <col style="width: 25%" />

              <tr>
                <th>
                  <el-radio v-model="varFlag" @change="getRadioVal(index)" :label="'0' + index"  style="font-weight: bold; color: black">评价对象</el-radio>
                </th>
                <td>
                  <el-tag :style="elTagStyle" v-for="item in value.entity" effect="plain"  :key ="item.str">{{item.str}}</el-tag>
                </td>
                <th>位置</th>
                <td>
                  <el-tag :style="elTagStyle" v-for="item in value.entity" effect="plain"  :key ="item.str">{{item.start + '--' + item.end}}</el-tag>
                </td>
              </tr>

              <tr>
                <th>
                  <el-radio v-model="varFlag" @change="getRadioVal(index)" :label="'1' + index" style="font-weight: bold; color: black">观点表达</el-radio>
                </th>
                <td>
                  <el-tag :style="elTagStyle" v-for="item in value.evaluation" effect="plain"  :key ="item.str">{{item.str}}</el-tag>
                </td>
                <th>位置</th>
                <td>
                  <el-tag :style="elTagStyle" v-for="item in value.evaluation" effect="plain"  :key ="item.str">{{item.start + '--' + item.end}}</el-tag>
                </td>
              </tr>


              <tr>
                <th>评价方面</th>
                <td style="text-align: center;">
                  <el-dropdown trigger="click" @command="handleAttribute">
                    <span class="el-dropdown-link">
                      <div style="display: inline-block">{{attributeList[value.attribute]}}</div><i class="el-icon-arrow-down el-icon--right"></i>
                    </span>
                    <el-dropdown-menu slot="dropdown" >
                      <el-dropdown-item v-for="(item, attributeIndex) in attributeList" :key="attributeIndex" :command="attributeIndex">{{item}}</el-dropdown-item>
                    </el-dropdown-menu>
                  </el-dropdown>
                </td>

                <th>情感极性</th>
                <td style="text-align: center;">
                  <el-dropdown trigger="click" @command="handlePolarity">
                    <span class="el-dropdown-link">
                      <div style="display: inline-block">{{polarityList[value.polarity]}}</div><i class="el-icon-arrow-down el-icon--right"></i>
                    </span>
                    <el-dropdown-menu slot="dropdown" >
                      <el-dropdown-item v-for="(item, polarityIndex) in polarityList" :key="polarityIndex" :command="polarityIndex">{{item}}</el-dropdown-item>
                    </el-dropdown-menu>
                  </el-dropdown>
                </td>

              </tr>


            </table>
          </div>
        </div>
      </el-col>


      <el-col :span="2">
        <div class="annotatorBtn" style="padding-top: 120px;">
          <el-button :style="btnStyle" type="info" @click="addvalue">添加</el-button>
        </div>
        <div class="annotatorBtn" style="padding-top: 120px;">
          <el-button :style="btnStyle" type="danger" @click="clearEventAll">清空</el-button>
        </div>
        <div class="annotatorBtn" style="padding-top: 120px;">
          <el-button :style="btnStyle" type="warning" @click="decreaseEventArgument">删除</el-button>
        </div>
        <div class="annotatorBtn" style="padding-top: 180px;">
          <el-button :style="btnStyle" type="primary" @click="postEvent">提交</el-button>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
// import { eleTable, eleTableColumn } from "ele-table";
// import 'ele-table/dist/ele-table.css'; 
import {fetchNextText, postEvent, fetchEventLabeledCount,fetchHistory} from '@/api/dataAnnotation.js'

export default {
  name: 'annotatorchange',
  data() {
    return {
      taskNum: '0',
      rawData: null,           //从后端获取的原始数据
      labeled_cnt: null,       //当前标注了多少数据
      unlabeled_cnt: null,     //当前没标多少数据
      labelPercentage: 0,   //标注进度
      text: '',       //需要标注的文本内容
      comment_variety:'',
      user_star:'',
      attributeList:['价格', '品质', '色泽', '口感', '包装', '分量', '物流', '售后', '其他'],
      polarityList:['负向', '正向', '中立'],
      tag: {
        isValue:'0',
        valueList:[
          {
            entity:[],
            evaluation:[],
            attribute:8,
            polarity:2,
          }
        ]
      },
      varOrder:0,
      varFlag: '',
      btnStyle: 'height:80px;margin-bottom:15px;font-size:18px',
      elTagStyle: 'font-size: 16px;',
    }
  },
  mounted() {
    this.getParams()
  },
  methods: {

    getParams(){
        this.rawData = this.$route.params.rawData
        this.taskNum = this.$route.params.taskNum
        this.text = this.rawData.comment_text
        this.comment_variety = this.rawData.comment_variety
        this.user_star = this.rawData.user_star
        this.tag = this.rawData.tag
        // console.log(this.rawData)
    },

    // 初始化 tag 这个变量，事件元素变动之后可以调用
    initData() {
      this.rawData = null,
      this.text = '',       //需要标注的文本内容
      this.comment_variety = '',
      this.user_star = '',
      this.tag = {
        isValue:'0',
        valueList:[
          {
            entity:[],
            evaluation:[],
            attribute:'8',
            polarity:'2',
          }
        ]
      }
    },

    handleSelect(key) {
      // console.log(key);
      this.taskNum = key
      this.updateText()
      this.updateCount()
    },

    handleAttribute(attributeIndex) {
      this.tag.valueList[this.varOrder].attribute = attributeIndex
    },

    handlePolarity(polarityIndex) {
      this.tag.valueList[this.varOrder].polarity = polarityIndex
    },

    // 提交标注好的事件
    postEvent() {
        //   console.log('ok')
        if (this.rawData){
          let data = {"comment_id": this.rawData['comment_id'], "comment_text": this.text, "comment_variety":this.comment_variety, 'user_star':this.user_star, "taskNum":this.taskNum, "tag": this.tag}
          postEvent(data).then(res => {
              // console.log('ok')
            this.$message({message:"成功提交", type:'success'})
            this.clearEventAll()
          }).catch(err => {
            this.$message({message: err, type:'error'})
          })
        }
        else{
          this.$message({message:"修改已提交，若想再次修改请从查看页面重新进入", type:'warning'})
        }
    },

    getRadioVal (value) {
      // console.log("ok")
      this.varOrder = value
      // console.log(this.varOrder)
    },

    //增加标注
    addvalue(){
      this.tag.valueList.push(
        {
          entity:[],
          evaluation:[],
          attribute:'8',
          polarity:'2',
        }
      )
    },

    
    // 清除事件所有变量
    clearEventAll() {
      this.varFlag = ''
      this.initData()
    },

    // 判断obj是否在arr中
    objectInArray(obj) {
      var arr = []
      
      switch (this.varFlag.charAt(0)){
        case "0":
          arr = this.tag.valueList[this.varOrder].entity
          
          break
        case "1":
          arr = this.tag.valueList[this.varOrder].evaluation
          
          break

      }
      if (arr.length!==0) {
        let flag = false
        for (let item of arr) {
          if (item['str']===obj['str'] && item['start']===obj['start'] && item['end']===obj['end']) {
            flag = true
            break;
          }
        }
        if (!flag) {
          arr.push(obj)
        }
      } else {
        arr.push(obj)
      }
    },

    // 删除列表最后一个事件元素
    decreaseEventArgument() {
      var arr = []
      
      switch (this.varFlag.charAt(0)){
        case "0":
          arr = this.tag.valueList[this.varOrder].entity
          
          break
        case "1":
          arr = this.tag.valueList[this.varOrder].evaluation
          
          break
      }
      arr.pop()
    },

    
    // 保存字符及其起始位置
    saveRangeList() {
      // 这个是测试出来的偏移量
      let offset = 1
      let selectionRange = window.getSelection().getRangeAt(0);
      let start = selectionRange.startOffset - offset;
      let end = selectionRange.endOffset - offset;  
      // console.log(start, end);
      let selectStr = window.getSelection().toString()
      // console.log(1)
      // console.log(this.varFlag)
      
      if (selectStr.length!==end-start || selectStr !== this.text.slice(start, end)){
        // console.log("start: "+start+" end: "+end+" offset: "+offset);
        // console.log("ERROR: check 'offset' in saveRangeList function");
      } else {
        // console.log('varFlag: '+this.varFlag)
        // console.log('varFlag: '+this.varFlag.charAt(0))
        // console.log(selectStr);
        // console.log(this.tag)
        if (this.varFlag!=='' && selectStr!=='') {
          let markData = {'str': selectStr, 'start': start, 'end': end}
          this.objectInArray(markData)
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.annotator-container {
  // background: #B3C0D1;
  background: rgb(240, 242, 245);
  // background: #E3EDCD;
  // padding-top: 50px;
  .grid-content {
    // border-radius: 4px;
    min-height: 625px;
    // overflow-y: scroll
  }
  .raw-text-container {
    border-style: solid;
    border-width: 1px;
    .raw-text {
      padding: 20px;
      line-height: 45px;
      font-size: 25px;
    }
    .raw-text::selection {
      color: #fff;
      background: #088;
    }
  }
  .event-list-container {
    border-style: solid;
    border-width: 1px;
    .event-list {
      // padding: 20px;
      .gridtable {
        width: 98%;
        line-height: 30px;
        border-width: 1px;
        border-collapse: collapse;
        margin: 1% 1% 1% 1%;
      }
      .gridtable th {
          border-width: 1px;
          padding: 8px;
          border-style: solid;
          // border-radius: 4px;
      }
      .gridtable td {
          border-width: 1px;
          padding: 8px;
          border-style: solid;
          // border-radius: 4px;
      }
    }
  }
  .line {
    width: 100%;
    border-bottom: solid 1px;
  }
  .title {
    line-height: 50px;
    padding-left: 10px;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
  }
  .annotatorBtn {
    height: 50px;
    width: 36px;
    padding-left: 20px;
  }
}
.el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
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
  }
</style>
