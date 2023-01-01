<template>
    <div style="background:#F2F3F5 ;min-width:fit-content;">
        <div>
            <!-- <el-row :gutter="20" class="Background">
                <h2 style="margin-left:40px">图谱查询</h2>
                <el-row :gutter="20" style="margin:10px">
                    <el-col :span="4"><div class="xuanzekuangshuoming">查询类型</div></el-col>
                    <el-col :span="8">
                        <el-select v-model="searchValue" placeholder="请选择" @change="searchValueChange">
                            <el-option v-for="item in searchList" :key="item" :label="item" :value="item"></el-option>
                        </el-select>
                    </el-col>
                </el-row>
            </el-row> -->
            <el-row id="SearchNode" class="Background" :gutter="10" style="margin-left: 10px; padding-bottom: 20px;">
                <h4 style="margin-left:20px">实体查询</h4>
                <el-col :span="18">
                    <el-row :gutter="20">
                        <el-col :span="3"><div class="xuanzekuangshuoming">类型</div></el-col>
                        <el-col :span="7">
                            <el-select v-model="entityType" placeholder="请选择">
                                <el-option v-for="item in typeList" :key="item" :label="item" :value="item"></el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="3"><div class="xuanzekuangshuoming">文本</div></el-col>
                        <el-col :span="9">
                            <el-input type="text" v-model="entity" placeholder="花生" @input="input_text"></el-input>
                            <p id="entity_alert" hidden style="color:red;margin-left: 5px;">请输入查询内容！</p>
                        </el-col>
                    </el-row>
                </el-col>
                <el-col :span="4">
                    <el-button type="primary" value="Submit" @click="search_node" class="InfoButton">查询</el-button>
                </el-col>
            </el-row>
            <!-- <el-row id="SearchTriplet" class="Background" :gutter="20" style="margin-left: 10px" hidden>
                <h4 style="margin-left:40px">三元组查询</h4>
                <el-col :span="18">
                    <el-row :gutter="20">
                        <el-col :span="4"><div class="xuanzekuangshuoming">三元组</div></el-col>
                        <el-col :span="10">
                            <el-select v-model="nodeValue" placeholder="请选择">
                                <el-option v-for="item in nodeList" :key="item" :label="item" :value="item"></el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="10">
                            <el-input type="text" v-model="entity" placeholder="实体" @input="input_text"></el-input>
                            <p id="triplet_alert" hidden style="color:red;">请输入查询内容！</p>
                        </el-col>
                    </el-row>
                    <div style="margin-top:20px"><b>查询实体：{{entity}}</b></div>
                </el-col>
                <el-col :span="4">
                    <el-button type="primary" value="Submit" @click="search_triplet" class="InfoButton">查询</el-button>
                </el-col>
            </el-row> -->
            <el-row :gutter="20">
                <el-col :span="20" class="Background" style="margin-left: 20px">
                    <h4 style="margin:20px">查询结果</h4>
                    <div style="margin:20px">查询实体：{{entity}}</div>
                    <el-row>
                        <div id="result"></div>
                        <div>
                            <iframe id="visual" :src="visualUrl" frameborder="0" style="width:600px;height:700px;"></iframe>
                        </div>
                    </el-row>
                </el-col>
            </el-row>
        </div> 
    </div>
</template>

<script>
  export default {
    data() {
        return {
            entity: '',
            searchValue: '节点查询',
            searchList: ['节点查询', '三元组查询'],
            entityType: '评价对象',
            typeList: ['产品', '评价对象', '评价词', '评价类别', '情感极性', '全部'],
            typeDict:{
                '产品': 'Product',
                '评价对象': 'Entity',
                '评价词': 'Opinion',
                '评价类别': 'Category',
                '情感极性': 'Polarity',
                '全部': 'All',
            },
            visualUrl: '/visual.html',
            visualData: 'Hello world',
        }
    },
    methods:{
        input_text(){
            this.$forceUpdate();
        },
        searchValueChange(){
            if(this.searchValue == '节点查询'){
                document.getElementById('SearchNode').hidden = false
                document.getElementById('SearchTriplet').hidden = true
            }
            else{
                document.getElementById('SearchNode').hidden = true
                document.getElementById('SearchTriplet').hidden = false
            }
        },
        click_search(){
            if(this.searchValue == '节点查询') this.search_node()
            else this.search_triplet()
        },
        search_node(){
            if(this.entity == ''){ // 没有输入信息
                // document.getElementById('entity_alert').hidden = false
                // return
                this.entity = '花生'
            }
            var param = {
                mod: 'entity',
                type: this.typeDict[this.entityType],
                name: this.entity,
            }
            var param_list = []
            for (var key in param){
                param_list.push(key + '=' + param[key])
            }
            var param_url = '?' + param_list.join('&')
            document.getElementById('visual').src = this.visualUrl + param_url
        },
        search_triplet(){

        },
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
