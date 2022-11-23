<template>
    <div style="background:#F2F3F5 ;min-width:fit-content;">
        <el-row :gutter="20" class="Background">
            <h2 style="margin:20px;margin-left: 40px;">知识图谱展示</h2>
        </el-row>
        <el-row :gutter="20" class="Background">
            <!-- 本体图谱 -->
            <el-col :span="11">
                <div style="margin: 20px;color:slategrey">本体图谱：</div>
                <div style="margin: 10px; margin-left:20px; color:slategrey">· 层次化展示农产品评价类别</div>
            
                <el-row style="margin-left:20px">
                    <kg-ontology ref="KGOntology"/>
                </el-row>
            </el-col>
            <!-- 产品图谱 -->
            <el-col :span="11">
                <!-- 产品选择 -->
                <el-row :gutter="30" style="margin-top:30px">
                    <el-col :span="4"><div class="xuanzekuangshuoming">产品</div></el-col>
                    <el-col :span="6">
                        <el-select v-model="chanpinValue" placeholder="请选择">
                            <el-option
                            v-for="item in chanpinList"
                            :key="item"
                            :label="item"
                            :value="item">
                            </el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="6">
                        <el-button :loading="getProductGraph" type="primary" @click="clickProduct" class="DailyInfoButton">获取产品图谱</el-button>
                    </el-col>
                </el-row>
                <!-- 分析信息 -->
                <el-row :gutter="30">
                    <el-card style="margin:30px;">
                        <p>本系统对于农产品2022年度的评价信息进行了整体分析。</p>
                        <p id="year_comment"></p>
                    </el-card>
                </el-row>
                <!-- 图谱 -->
                <el-row>
                    <kg-product ref="KgProduct"/>
                </el-row>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    import {getProductGraph} from '@/api/knowledgeGraph.js'
    import KgOntology from './ontology.vue'
    import KgProduct from './product.vue'
    export default {
        components: {
            KgOntology,
            KgProduct,
        },
        data() {
        return {
            chanpinValue:'大米',
            chanpinList:['大米', '番茄', '茶叶', '荸荠', '猕猴桃', '竹笋', '蜜柚', '茶油', '椪柑', '大蒜', '藕', '豆皮', '蜜茄'],
            // chanpinList:['大米', '番茄', '茶叶', '荸荠', '油茶', '猕猴桃', '竹笋', '红米', '蜜柚', '茶油', '贡米', '炒青', '椪柑', '大蒜', '白肉姜', '红心脚板薯', '藕', '酱姜', '豆皮', '橙皮', '蜜茄'],
            // chanpinList:['大米','番茄','茶叶'],
            getProductGraph:false,
        }
        },
        methods: {
            clickProduct(){
                this.getProductGraph = true
                let data = {}
                if (this.chanpinValue){
                    data['variety'] = this.chanpinValue
                    // this.$refs.KgProduct.initChart('产品图谱','', this.chanpinValue)
                    getProductGraph(data).then(res =>{
                        this.getAnalysisDetailLoading = false
                        this.$message({message:"获取成功", type:'success'})
                        this.ProductRes = res
                        console.log(this.ProductRes)
                        document.getElementById('year_comment').innerText = res['comment_data']
                        this.$refs.KgProduct.initChart(this.chanpinValue, '', res['graph_data'])
                        // this.$refs.KgProduct.initChart('产品图谱','', res['data']['graph_data'])
                    })
                    }
                else{
                    this.$message.warning('请选择产品');
                }
                this.getProductGraph = false
            },
        }
    }
</script>


<style lang="scss" scoped>
    .Background{
        margin: 20px;
        background: white;
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
    .fenquCol{
        border-radius: 4px;
        background: rgb(240, 242, 245);
    }
    .fenqubiaoti{
        font-family: 'Inter';
        font-style: normal;
        font-weight: 400;
        font-size: 24px;
        line-height: 29px;
        display: flex;
        justify-content: center;
        /* align-items: center; */
        /* text-align: center;  */
        /* margin:auto; */
    }
    .fenqubiaotiRow{
        margin-top: 30px;
        margin-bottom: 20px;
    }
    .fenquxuanzekuangRow{
        margin-top: 30px;
        margin-bottom: 20px;
    }
    .xuanzekuangshuoming{
        font-family: 'Inter';
        font-style: normal;
        font-weight: 400;
        font-size: 18px;
        line-height: 22px;
        display: flex;
        justify-content: center;
        padding-top: 8px;
    }
    .DailyInfoButton{
        display: flex;
        justify-content: center;
    }
    .cardStyle{
        width: 80%;
        background: #F9F9F9;
        border: 1px solid #C4C4C4;
        box-sizing: border-box;
        border-radius: 10px;display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-left: 10%;
        margin-right: 10%;
    }
</style>