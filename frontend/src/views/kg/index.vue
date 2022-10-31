<template>
    <div style="background:#F2F3F5 ;min-width:fit-content;">
        <div class="Background">
            <el-row :gutter="20">
                <h2 style="margin-left:40px">图谱查询</h2>
            </el-row>
            <el-row :gutter="20">
                <h4 style="margin-left:40px">实体查询</h4>
            </el-row>
            <el-row :gutter="20">
                <h4 style="margin-left:40px">三元组查询</h4>
            </el-row>
            <div>
                <iframe :src="reportUrl" frameborder="0" style="width:600px;height:700px;"></iframe>
            </div>
            <!-- <el-row :gutter="10" style="margin-left: 10px; margin-right: 10px;">
                <el-col :span="7" class="card">
                    <h4 style="margin-left: 10px">江西丰城大米</h4>
                    <p class="fixtext">丰城市位于江西省中部，赣江下游，境内土壤肥沃，生长季长，日照充足，是全国重要粮食生产基地， 2021年全市粮食总产量达20.24亿斤，并建设实施高标准农田8.29万亩。丰城大米以香、甜、软、滑的特点广为人知，丰城市致力于做大做强“丰城大米”这一区域品牌，重点发展优质大米、富硒功能大米、有机大米等优势品种，其中丰城富硒大米已经成为了独特的地理品牌标识，以天然富硒、米粒细长、晶莹剔透、口感佳等特点，成为人们天然补硒，抗氧化、增强人体免疫的食补佳品。</p>
                    <el-button type="primary" @click="preview('fengcheng')" class="SearchButton" align="right">点击查看</el-button>
                </el-col>
                <el-col :span="7"  class="card">
                    <h4 style="margin-left: 10px">安徽巢湖番茄</h4>
                    <p class="fixtext">安徽巢湖因其湿润季风气候以及良好的土壤肥力条件而盛产番茄，其中以中垾番茄最为出名。中垾番茄作为全国农产品地理标志，种植历史悠久，果肉厚，无空洞果，生食口感甜酸适口，肉质面沙，风味好，生熟食兼用，富含多种营养元素，具有健胃消食，生津止渴，润肠通便等功效。此外，番茄中所含番茄红素具有独特的抗氧化作用，对防癌抗癌，延缓衰老有良好的辅助治疗作用。</p>
                    <el-button type="primary" @click="preview('chaohu')" class="SearchButton">点击查看</el-button>
                    <br/>
                </el-col>
                <el-col :span="7" class="card">
                    <h4 style="margin-left: 10px">湖北仙桃莲藕</h4>
                    <p class="fixtext">湖北省仙桃市地处江汉平原腹地，属亚热带季风气候区，光热资源充足，河流湖泊密布，水系发达。境内地质结构多为冲积平原，土层深厚、土壤肥沃、酸碱适中。良好的自然地理条件为仙桃莲藕的高产、稳产、优质奠定了坚实的基础。莲藕是仙桃市四大土特名产之一，粗壮肥大，肉质松脆，纹理细腻，味道鲜美。历史上一直是进奉皇帝的上等贡品，被人们视为席中珍品。2013年，经国家工商总局商标局认定，“沔城藕”荣获中国国家地理标志证明商标。近年来，莲藕、藕带生产加工已成为仙桃市最具发展潜力的农业支柱产业之一，仙桃莲藕逐渐进入大城市的超级市场，成为人们争先购买的绿色食品。</p>
                    <el-button type="primary" @click="preview('xiantao')" class="SearchButton">点击查看</el-button>
                </el-col>
            </el-row> -->
        </div> 
    </div>
</template>

<script>
  export default {
    methods:{
        data() {
            return {
                reportUrl: 'http://47.100.99.53:7474/browser/',
            }
        },
      preview(filename){
        // console.log(filename)
        // let a = document.createElement('a')
        // a.href = './' + filename + '.vue'
        // a.target = '_blank'
        // a.click()
        this.$router.push({name: filename})
        // this.$router.push({name: 'fengcheng'})
      },
    },
    data() {
      return {
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

    .Background{
        margin: 20px;
        background: white;
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
