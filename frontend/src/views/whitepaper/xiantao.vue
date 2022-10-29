<template>
  <el-row :gutter="20" id="background" style="background:#F2F3F5 ;min-width:fit-content; height: 720px;">
      <el-col :span="20" class="Background" style="margin-left: 40px;">
          <iframe :src="reportUrl" frameborder="0" style="width:600px;height:700px;"></iframe>
      </el-col>
  </el-row>
</template>

<script>
  export default {
    methods:{
    },
    data() {
      return {
        reportUrl: '/whitepaper/湖北仙桃莲藕2022年第一季度电商销售白皮书-张文宇.html',
      }
    }
  }
</script>

<style lang="scss" scoped>
  iframe{
    background-color: white;
    margin: auto;
    position: absolute;
    left:0;
    right:0;
  }
  .Background{
        margin: 20px;
        background: white;
    }
  .home-container {
    min-height:800px;
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
    font-size:30px;
    line-height: 60px;
  }

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
  }

  @media screen and (max-width: 992px) {
    .home-container {
      .chart-wrapper {
        padding: 8px;
      }
    }
  }
</style>
