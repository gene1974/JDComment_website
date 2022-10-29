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
        reportUrl: '/whitepaper/安徽巢湖番茄2022年第一季度电商销售白皮书-田诗扬.html',
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
</style>
