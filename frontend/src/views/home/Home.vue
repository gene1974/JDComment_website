<template>
  <div class="home-container" style="min-width:fit-content;">
    <el-container>
      <el-header>农产品情感分析系统</el-header>
      <el-main style="height:700px">
        <el-row :gutter="20">
            <el-col>
              <el-image
              @click="jumpToWhite"
              style="width: 200px; height: 200px; margin-bottom:-50px;"
              :src="url4"></el-image>
              <div class="gongnengmingcheng">白皮书</div>
              <div class="gongnengshuoming" style="margin-top:10px">农产品情感分析白皮书</div>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="8">
              <el-image
              @click="jumpToShuju"
              style="width: 200px; height: 200px; margin-top:10%; margin-bottom:-50px;"
              :src="url1"></el-image>
              <div class="gongnengmingcheng">数据库</div>
              <div class="gongnengshuoming" style="margin-top:10px">导入数据的查看、标注、修改等</div>
            </el-col>
            <el-col :span="8">
              <el-image
              @click="jumpToFenxi"
              style="width: 200px; height: 200px; margin-top:10%; margin-bottom:-50px;"
              :src="url2"></el-image>
              <div class="gongnengmingcheng">数据分析</div>
              <div class="gongnengshuoming" style="margin-top:10px">现有数据的统计分析结果及相应建议</div>
            </el-col>
            <el-col :span="8">
              <el-image
              @click="jumpToTupu"
              style="width: 200px; height: 200px; margin-top:10%; margin-bottom:-50px;"
              :src="url3"></el-image>
              <div class="gongnengmingcheng">图谱查看</div>
              <div class="gongnengshuoming" style="margin-top:10px">评价情感知识可视化图谱</div>
            </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<!-- school -->
<!-- <template>
  <div class="home-container" style="min-width:fit-content;">
    <el-container>
      <el-header>面向智慧城市的网络民调知识图谱及其应用</el-header>
      <el-main style="height:700px">
        <el-row :gutter="20">
            <el-col>
              <el-image
              @click="jumpToWhite"
              style="width: 200px; height: 200px; margin-bottom:-50px;"
              :src="url4"></el-image>
              <div class="gongnengmingcheng">民意理解报告</div>
              <div class="gongnengshuoming" style="margin-top:10px">评论民意情感分析结果</div>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="8">
              <el-image
              @click="jumpToShuju"
              style="width: 200px; height: 200px; margin-top:10%; margin-bottom:-50px;"
              :src="url1"></el-image>
              <div class="gongnengmingcheng">情感知识数据库</div>
              <div class="gongnengshuoming" style="margin-top:10px">情感知识数据库</div>
            </el-col>
            <el-col :span="8">
              <el-image
              @click="jumpToFenxi"
              style="width: 200px; height: 200px; margin-top:10%; margin-bottom:-50px;"
              :src="url2"></el-image>
              <div class="gongnengmingcheng">知识引导民意挖掘</div>
              <div class="gongnengshuoming" style="margin-top:10px">基于情感知识的民意挖掘统计分析</div>
            </el-col>
            <el-col :span="8">
              <el-image
              @click="jumpToTupu"
              style="width: 200px; height: 200px; margin-top:10%; margin-bottom:-50px;"
              :src="url3"></el-image>
              <div class="gongnengmingcheng">图谱可视化查询</div>
              <div class="gongnengshuoming" style="margin-top:10px">情感知识图谱可视化及查询可视化</div>
            </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template> -->

<script>
  export default {
    methods:{
      jumpToWhite(){
        this.$router.push({name:'whitepaper'})
      },
      jumpToShuju(){
        this.$router.push({name:'shujuku'})
      },
      jumpToFenxi(){
        this.$router.push({name:'dataAnalysis'})
      },
      jumpToTupu(){
        this.$router.push({name:'xiaofeigraph'})
      },
    },
    data() {
      return {
        url1: require('./image/Group1.png'),
        url2: require('./image/Group2.png'),
        url3: require('./image/Group3.png'),
        url4: require('./image/Group.jpg'),
      }
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

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
  }
  .gongnengmingcheng{
    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 24px;
    line-height: 29px;
    display: flex;
    justify-content: center;
  }
  .gongnengshuoming{
    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 18px;
    line-height: 22px;
    display: flex;
    justify-content: center;

    color: #ABABAB;
  }

  @media screen and (max-width: 992px) {
    .home-container {
      .chart-wrapper {
        padding: 8px;
      }
    }
  }
</style>
