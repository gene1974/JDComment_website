
<!-- <script src="../../../public/js/jquery-3.6.1.min.js"></script>
<script type="text/javascript" src="../../../public/static/neovis.js"></script> -->
<script type="text/javascript" src="/static/neovis.js"></script>
<template>
    <div>
        <el-row>
            <h2 style="margin: 40px; margin-bottom: 0px;">可视化</h2>
        </el-row>
        <el-row :gutter="20" style="margin:20px; margin-left: 40px;">
            <div id="viz"></div>
            <h4>Cypher query: </h4>
            <textarea rows="4" cols=50 id="cypher"></textarea><br>
            <!-- <input type="submit" value="Submit" id="reload" class="InfoButton" @click="submit">
            <input type="submit" value="Stabilize" id="stabilize" class="InfoButton" @click="stabilize"> -->
            <input type="text" v-model="cypher_lan"/>
        </el-row>
        <el-row :gutter="20" style="margin:20px; margin-left: 40px;">
            <el-button type="primary" value="Submit" @click="submit" id="reload" class="InfoButton">查询</el-button>
            <!-- <el-button :loading="getDailyInfoLoading" type="primary" @click="clickQuery" class="InfoButton">查询</el-button> -->
        </el-row>
    </div>
</template>
 

<script>
export default {
    name: '',
    components: {},
    props: {},
    data() {
        return {
            cypher_lan: '',
            viz: {} //定义一个viz对象
        }
    },
    mounted() { this.draw() }, //渲染
    methods: {
        submit() { 
            var cypher = $("#cypher").val();
            // var cypher = document.getElementById("cypher").value
            console.log(cypher)
            if (cypher.length > 3) {
                this.viz.renderWithCypher(cypher);
            } else {
                console.log("reload");
                this.viz.reload();
 
            }
        },
        stabilize() {
            this.viz.stabilize();
        },
        draw() {
            var config = {
                container_id: "viz",
                server_url: "http://47.100.99.53:7474/browser/",
                server_user: "neo4j",
                server_password: "neo4j",
                labels: {
                    //"Character": "name",
                    "Character": {
                        "caption": "name",
                        "size": "pagerank",
                        "community": "community"
                        //"sizeCypher": "MATCH (n) WHERE id(n) = {id} MATCH (n)-[r]-() RETURN sum(r.weight) AS c"
                    }
                },
                relationships: {
                    "INTERACTS": {
                        "thickness": "weight",
                        "caption": false
                    }
                },
                //查询节点的语句，写成你们的
                // match (n:Product {name:'洋芋') return n;
                initial_cypher: "match (n)-[r]->(m) return n,r,m;" 
 
            };
 
            this.viz = new NeoVis.default(config);
            this.viz.render();
            console.log(this.viz);
        }
    },
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
</style>

<!-- <style lang="less" scoped>
.myDiv {
    width: 800px;
    height: 800px;
}
textarea {
    border: 1px solid lightgray;
    margin: 5px;
    border-radius: 5px;
}
#viz {
    width: 100%;
    height: 80%;
    border: 1px solid #f1f3f4;
    font: 22pt arial;
}
input {
    border: 1px solid #ccc;
} -->