<template>
    <div style="background:#F2F3F5 ;min-width:fit-content;">
        <div class="Background">
            <el-row :gutter="20">
                <h2 style="margin-left:40px">图谱查询</h2>
            </el-row>
            <el-row :gutter="20" style="margin-left: 20px">
                <h4 style="margin-left:40px">实体查询</h4>
                <el-col :span="8">
                    <el-input type="text" v-model="entity" placeholder="实体" @input="input_text"></el-input>
                    <div style="margin-top:20px"><b>查询实体：{{entity}}</b></div>
                    <el-row>
                        <div id="result"></div>
                    </el-row>
                </el-col>
                <el-col :span="4">
                    <el-button type="primary" value="Submit" @click="submit_entity" class="InfoButton">查询</el-button>
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="20" style="margin-left: 20px">
                <h4 style="margin-left:40px">查询结果</h4>
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <h4 style="margin-left:40px">三元组查询</h4>
            </el-row>
            <!-- <el-row :gutter="20">
                <div>
                    <iframe :src="reportUrl" frameborder="0" style="width:600px;height:700px;"></iframe>
                </div>
            </el-row> -->
        </div> 
    </div>
</template>

<script>
  export default {
    data() {
        return {
            // reportUrl: 'http://47.100.99.53:7474/browser/',
            // reportUrl: '/simple-example.html',
            // reportUrl: '/hello.html',
        }
    },
    methods:{
      preview(filename){
        // console.log(filename)
        // let a = document.createElement('a')
        // a.href = './' + filename + '.vue'
        // a.target = '_blank'
        // a.click()
        // this.$router.push({name: filename})
        // this.$router.push({name: 'fengcheng'})
      },
      input_text(){
        this.$forceUpdate();
      }
    }
  }
</script>

<style lang="scss" scoped>
    .Background{
        margin: 20px;
        background: white;
    }
    .InfoButton{
        background-color: #165DFF;
    }
    .ResetButton{
        // display: flex;
        // justify-content: center;
        color: #000000;
        background-color: #F2F3F5;
        border-color: #F2F3F5;
    }
    .card{
        margin: 10px;
        padding: 0 0 20px 20px;
        border-style: solid;
        border-width: 1px;
        border-radius: 8px;
        border-color: #C9CDD4;
    }
    .fixtext{
        margin-left: 10px;
        /* 裁剪多余的 */
        overflow : hidden;
        /* 多余的以省略号出现 */
        text-overflow: ellipsis;
        /* 将对象作为弹性伸缩盒子模型显示 */
        display: -webkit-box;
        /* 限制再一个块元素再文本显示的行数 */
        -webkit-line-clamp: 4; // 文字最多4行
        /* 设置或检索伸缩盒对象的子元素的排列方式 */
        -webkit-box-orient: vertical;
    }
    .SearchButton{
        color: #468DFF;
        background-color: #FFFFFF;
        border-width: 1px;
        float: right;
        margin-right: 20px;
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

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
  }

</style>
