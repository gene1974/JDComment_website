<template>
    <div class="home-container">
    <!-- <div class="home-container" style="min-width:fit-content;"> -->
        <el-header>白皮书</el-header>
        <div>
          <el-row>
            <el-col :span="7" style="margin:20px">
              <el-card style="height:540px;">
                <h4 >江西丰城大米</h4>
                      <p>丰城市位于江西省中部，赣江下游，境内土壤肥沃，生长季长，日照充足，是全国重要粮食生产基地， 2021年全市粮食总产量达20.24亿斤，并建设实施高标准农田8.29万亩。</p>
                      <p>丰城大米以香、甜、软、滑的特点广为人知，丰城市致力于做大做强“丰城大米”这一区域品牌，重点发展优质大米、富硒功能大米、有机大米等优势品种，其中丰城富硒大米已经成为了独特的地理品牌标识，以天然富硒、米粒细长、晶莹剔透、口感佳等特点，成为人们天然补硒，抗氧化、增强人体免疫的食补佳品。</p>
                      <el-button type="primary" @click="preview('fengcheng')" class="Button">点击查看白皮书</el-button>
              </el-card>
            </el-col>
            <el-col :span="7" style="margin:20px">
              <el-card style="height:540px;">
                <h4 >安徽巢湖番茄</h4>
                      <p>安徽巢湖因其湿润季风气候以及良好的土壤肥力条件而盛产番茄，其中以中垾番茄最为出名。中垾番茄作为全国农产品地理标志，种植历史悠久，果肉厚，无空洞果，生食口感甜酸适口，肉质面沙，风味好，生熟食兼用，富含多种营养元素，具有健胃消食，生津止渴，润肠通便等功效。此外，番茄中所含番茄红素具有独特的抗氧化作用，对防癌抗癌，延缓衰老有良好的辅助治疗作用。</p>
                      <el-button type="primary" @click="preview('chaohu')" class="Button">点击查看白皮书</el-button>
                      <br/>
              </el-card>
            </el-col>
            <el-col :span="7" style="margin:20px">
              <el-card style="height:540px;">
                <h4 >湖北仙桃莲藕</h4>
                      <p>湖北省仙桃市地处江汉平原腹地，属亚热带季风气候区，光热资源充足，河流湖泊密布，水系发达。境内地质结构多为冲积平原，土层深厚、土壤肥沃、酸碱适中。良好的自然地理条件为仙桃莲藕的高产、稳产、优质奠定了坚实的基础。</p>
                      <p>莲藕是仙桃市四大土特名产之一，粗壮肥大，肉质松脆，纹理细腻，味道鲜美。历史上一直是进奉皇帝的上等贡品，被人们视为席中珍品。2013年，经国家工商总局商标局认定，“沔城藕”荣获中国国家地理标志证明商标。近年来，莲藕、藕带生产加工已成为仙桃市最具发展潜力的农业支柱产业之一，仙桃莲藕逐渐进入大城市的超级市场，成为人们争先购买的绿色食品。</p>
                      <el-button type="primary" @click="preview('xiantao')" class="Button">点击查看白皮书</el-button>
              </el-card>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="7" style="margin:20px">
              <el-card style="height:520px;">
                <h3>江西奉新猕猴桃</h3>
                      <p>奉新被誉为“中国猕猴桃之乡”，境内四季分明，雨量充沛，日照充足，无霜期长，种植猕猴桃历史悠久，区域特色明显，并在2015年获得了农业农村部农产品地理标志登记保护。充足的光热条件让“奉新猕猴桃”积累了更多的干物质和更丰富的营养，形成了质地细嫩、柔软多汁、风味浓郁的绝佳食用口感，深受消费者喜爱，综合年产值达9亿元。</p>
                      <el-button type="primary" @click="preview('fengxin')" class="Button">点击查看白皮书</el-button>
              </el-card>
            </el-col>
            <el-col :span="7" style="margin:20px">
              <el-card style="height:520px;">
                <h3>江西井冈山蜜柚</h3>
                      <p>“星星之火，可以燎原”。巍巍井冈，蜜柚成林。这片红色土地，绿意盎然，一派生机勃勃，井冈蜜柚，清甜飘香，无疑是其中十分亮丽的一道景色。地处典型中亚热带湿润季风区的吉安井冈山周边，雨量充沛，无霜期长，适宜绝大部分柑橘类果树的栽培。如今提起江西果业三宝，赣南脐橙和南丰蜜橘闻名天下，其实，出产于吉安井冈周边的井冈蜜柚，更是独树一帜。</p>
                      <p>井冈蜜柚味甘、酸，性寒，有健胃化食、下气消痰、轻身悦色等功用。现代医药学研究发现有降血糖、减肥、美肤美容等功效。经常食用，对高血压、糖尿病、血管硬化等疾病有辅助治疗作用，对肥胖者有健体养颜功能。</p>
                      <el-button type="primary" @click="preview('jinggangshan')" class="Button">点击查看白皮书</el-button>
              </el-card>
            </el-col>
            <el-col :span="7" style="margin:20px">
              <el-card style="height:520px;">
                <h3>江西上高大蒜</h3>
                      <p>上高县，隶属江西省宜春市，位于江西省西北部，地处赣江支流锦江中游，境内土壤肥沃，生长季长，日照充足，是全国重要粮食生产基地， 2021年全年粮食播面达67万亩，并完成2.5万亩高标准农田建设。</p>
                      <p>上高紫皮大蒜是江西省宜春市上高县特产，全国农产品地理标志。具有“蒜香浓郁，辛辣可口”的特点，紫皮大蒜是上高传统的优良地方品种，种植历史悠久，清康熙《上高县志》既有大蒜种植的记载，上高紫皮大蒜叶肉肥厚，纤维少，汁液粘滑，味香浓郁，口感爽脆，辛辣而不刺舌，是调味料食品的首选之一。</p>
                      <el-button type="primary" @click="preview('shanggao')" class="Button">点击查看白皮书</el-button>
              </el-card>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="7" style="margin:20px">
              <el-card style="height:650px;">
                <h3>江西永新橙皮</h3>
                      <p>永新陈皮也称永新橙皮，是永新的特产，是江西省永新县传统蜜饯，生产历史悠久，远近闻名。《中国土特产大全》载为“永新柚皮”，本地称“橙皮”。成品保持刚切下的橙皮片原色原形，边沿嫩绿可爱，片体色白如玉，香气清幽，质地松脆，甜美可口，嚼到绿色表皮，满口凉爽生香，别具风味，堪称茶点珍品。且含有皮苷、新橙皮糖苷、胡萝卜素、多种维生素及钙、磷、铁等成分，具有消食解酒、润肺生津、通气化痰等功效，又是调治疾病的良药。永新橙皮制作有严格的时间要求和工艺要求。一般每年农历六月摘取青皮橙子（即未成熟的袖子）进行制作，因此第三季度可以买到新鲜制作的橙皮，永新橙皮的保质期一般为一年。</p>
                      <el-button type="primary" @click="preview('yongxin')" class="Button">点击查看白皮书</el-button>
              </el-card>
            </el-col>
            <el-col :span="7" style="margin:20px">
              <el-card style="height:650px;">
                <h3>江西万年茶油</h3>
                      <p>《本草纲目拾遗》中曾记载：“豫省闽粤皆食茶油，而不知为树子油，俗呼茶油，实非茶子之油也。”茶油又名山茶油、木油，是高级木本食用植物油，被誉为“东方橄榄油”。它取自群山森林中的油茶树种子，采用传统工艺精制提炼而成。万年县地处江西省东北部、鄱阳湖东南岸，万年多岗地和丘陵，山体土质是对油茶树生长发育极为有利的酸性黄壤，森林覆盖率达到64.1%，盛产茶油。</p>
                      <p>茶油既营养丰富，又极具保健功效。其不饱和脂肪酸含量高达90%以上，富有多种维生素及微量元素，具有降血脂、降血压、降胆固醇、滋肾润肺、清於利气、清肝解毒、润肤养颜之功效，长期食用，可预防各种心脑血管疾病，调节人体内生态平衡。除食用外，万年茶油还可用作美容产品，其含有的维生素E和抗氧化成分，能防止皮肤损伤，保持皮肤光泽，同时还能去除眼角皱纹，使人永葆青春活力。</p>
                      <el-button type="primary" @click="preview('wannian')" class="Button">点击查看白皮书</el-button>
              </el-card>
            </el-col>
            <el-col :span="7" style="margin:20px">
              <el-card style="height:650px;">
                <h3>四川宜宾屏山桠橙</h3>
                      <p>屏山椪柑，是四川省宜宾市屏山县的著名特产，宜宾市的屏山县处于典型南野热带气候属性的金沙江区域，独特的地理条件、丰富的热资源，使这片区域能成为宜宾市椪柑最好的生产区域，同时也酿成了屏山椪柑的优良品质。</p>
                      <p>屏山椪柑果面橙黄、光滑、皮薄、籽少、质脆、甚甜、清香、汁多。屏山椪柑是宜宾市水果业的一面旗帜，自从上个世纪90年代开始一枝独秀，以南亚热带气候属性的金沙江河谷“自然天成”的地理优势，凸现其在宜宾区域的心智资源，这一水果枭雄不但问鼎川南，而且还进入全国市场，曾获中国第二届农业博览会铜奖，有“屏山椪柑甲天府”的美誉。</p>
                      <el-button type="primary" @click="preview('yibin')" class="Button">点击查看白皮书</el-button>
              </el-card>
            </el-col>
          </el-row>
        </div>
        
        <!-- <div>
            <h3 style="margin:20px">江西丰城大米</h3>
            <p style="margin:20px">2022年第一季度江西丰城大米电商销售白皮书</p>
            <el-row style="margin:20px;">
                <el-col :span="12" style="width:400px;">
                    <el-card>
                      <h4 >产品背景介绍</h4>
                      <p>丰城市位于江西省中部，赣江下游，境内土壤肥沃，生长季长，日照充足，是全国重要粮食生产基地， 2021年全市粮食总产量达20.24亿斤，并建设实施高标准农田8.29万亩。</p>
                      <p>丰城大米以香、甜、软、滑的特点广为人知，丰城市致力于做大做强“丰城大米”这一区域品牌，重点发展优质大米、富硒功能大米、有机大米等优势品种，其中丰城富硒大米已经成为了独特的地理品牌标识，以天然富硒、米粒细长、晶莹剔透、口感佳等特点，成为人们天然补硒，抗氧化、增强人体免疫的食补佳品。</p>
                    </el-card>
                </el-col>
                <el-col :span="8" style="margin-left: 40px">
                    <el-card>
                    <h4 style="margin-left:10px">白皮书查看</h4>
                    <el-button type="primary" @click="preview('fengcheng')" class="Button">点击预览</el-button>
                    </el-card>
                </el-col>
            </el-row>
        </div> -->
    </div>
</template>

<script>
  export default {
    methods:{
      preview(filename){
        // console.log(filename)
        // let a = document.createElement('a')
        // a.href = './' + filename + '.vue'
        // a.target = '_blank'
        // a.click()
        this.$router.push({name: filename})
        // this.$router.push({name: 'fengcheng'})
      },
      download(filename){
        console.log(filename)
        let a = document.createElement('a')
        a.href = '/whitepaper/2022年第一季度江西丰城大米电商销售白皮书.docx'
        a.download = '江西丰城大米.docx'
        a.click()
      }
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
