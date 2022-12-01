<template>
  <div ref="mychart" class="graph" :style="{height:height,width:width}"></div>
</template>

<script>
  import echarts from 'echarts'
  import resize from '@/utils/echarts_resize.js'
//   import benti from '@/assets/graph_data/benti.js'

  export default {
    name: 'KGOntology',
    mixins: [resize],
    props: {
      width: {
        type: String,
        //default: '100%'
        default: '500px'
      },
      height: {
        type: String,
        default: '500px'
      },
    },
    data() {
      return {
        chart: null,
        // dict:benti,
        nodes: [],
        links: [],
          
        xiaofeidata:{"name": "产品", "children": [{"name": "价格", "children": [{"name": "价格", "children": [{"name": "正向", "children": [{"name": "实惠"}, {"name": "便宜"}, {"name": "优惠"}, {"name": "划算"}, {"name": "不贵"}, {"name": "不错"}, {"name": "公道"}, {"name": "美丽"}]}, {"name": "中性", "children": [{"name": "合适"}, {"name": "还可以"}, {"name": "可以"}, {"name": "还行"}, {"name": "适中"}, {"name": "一般"}]}, {"name": "负向", "children": [{"name": "贵"}, {"name": "高"}, {"name": "虚高"}, {"name": "不值"}, {"name": "不值得"}, {"name": "不便宜"}, {"name": "不一样"}]}]}, {"name": "价钱", "children": [{"name": "正向", "children": [{"name": "实惠"}, {"name": "公道"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "贵"}, {"name": "不值"}, {"name": "不便宜"}, {"name": "高"}]}]}, {"name": "价", "children": [{"name": "正向", "children": [{"name": "廉"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "高"}]}]}, {"name": "价位", "children": [{"name": "正向", "children": [{"name": "便宜"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "活动", "children": [{"name": "正向", "children": [{"name": "划算"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "性价比", "children": [{"name": "正向", "children": [{"name": "高"}, {"name": "不错"}]}, {"name": "中性", "children": [{"name": "一般"}]}, {"name": "负向", "children": [{"name": "不高"}]}]}]}, {"name": "品质", "children": [{"name": "品质", "children": [{"name": "正向", "children": [{"name": "好"}, {"name": "还好"}, {"name": "不错"}, {"name": "有保证"}, {"name": "保证"}]}, {"name": "中性", "children": [{"name": "一般"}, {"name": "一般般"}]}, {"name": "负向", "children": [{"name": "差"}, {"name": "不好"}, {"name": "差很多"}]}]}, {"name": "质量", "children": [{"name": "正向", "children": [{"name": "好"}, {"name": "还好"}, {"name": "不错"}, {"name": "还不错"}, {"name": "可以"}, {"name": "还可以"}, {"name": "还行"}, {"name": "优良"}, {"name": "挺好的"}, {"name": "杠杠的"}, {"name": "有保障"}, {"name": "有保证"}, {"name": "干净"}]}, {"name": "中性", "children": [{"name": "一般"}, {"name": "一般般"}]}, {"name": "负向", "children": [{"name": "差"}, {"name": "不好"}, {"name": "不行"}, {"name": "不稳定"}, {"name": "不太好"}, {"name": "不咋地"}, {"name": "不一样"}]}]}, {"name": "个头", "children": [{"name": "正向", "children": [{"name": "大"}, {"name": "均匀"}, {"name": "不错"}]}, {"name": "中性", "children": [{"name": "一般"}, {"name": "中等"}]}, {"name": "负向", "children": [{"name": "小"}, {"name": "不大"}, {"name": "有大有小"}, {"name": "参差不齐"}]}]}, {"name": "个", "children": [{"name": "正向", "children": [{"name": "大"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "小"}]}]}, {"name": "大小", "children": [{"name": "正向", "children": [{"name": "均匀"}, {"name": "合适"}, {"name": "适中"}, {"name": "可以"}]}, {"name": "中性", "children": [{"name": "一般"}]}, {"name": "负向", "children": [{"name": "不一"}, {"name": "不均匀"}, {"name": "不均"}, {"name": "差异太大"}, {"name": "不同"}]}]}, {"name": "颗粒", "children": [{"name": "正向", "children": [{"name": "饱满"}, {"name": "均匀"}, {"name": "大"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "小"}, {"name": "不饱满"}, {"name": "不均匀"}, {"name": "大小不一"}]}]}, {"name": "粒", "children": [{"name": "正向"}, {"name": "中性"}, {"name": "负向", "children": [{"name": "小"}]}]}, {"name": "日期", "children": [{"name": "正向", "children": [{"name": "新鲜"}, {"name": "新"}, {"name": "新的"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "不新鲜"}]}]}, {"name": "东西", "children": [{"name": "正向", "children": [{"name": "好"}, {"name": "新鲜"}, {"name": "不错"}, {"name": "还行"}, {"name": "可以"}, {"name": "还可以"}]}, {"name": "中性", "children": [{"name": "一般"}]}, {"name": "负向"}]}, {"name": "商品", "children": [{"name": "正向", "children": [{"name": "不错"}, {"name": "还可以"}, {"name": "好"}, {"name": "好评"}]}, {"name": "中性", "children": [{"name": "一般"}]}, {"name": "负向"}]}, {"name": "产品", "children": [{"name": "正向", "children": [{"name": "嫩"}, {"name": "新鲜"}, {"name": "不错"}]}, {"name": "中性", "children": [{"name": "一般"}]}, {"name": "负向", "children": [{"name": "垃圾"}]}]}, {"name": "物", "children": [{"name": "正向", "children": [{"name": "美"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "果子", "children": [{"name": "正向", "children": [{"name": "新鲜"}, {"name": "饱满"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "果", "children": [{"name": "正向"}, {"name": "中性"}, {"name": "负向", "children": [{"name": "小"}]}]}, {"name": "核", "children": [{"name": "正向"}, {"name": "中性"}, {"name": "负向", "children": [{"name": "大"}]}]}, {"name": "皮", "children": [{"name": "正向", "children": [{"name": "薄"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "厚"}]}]}, {"name": "汁", "children": [{"name": "正向", "children": [{"name": "多"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "水分", "children": [{"name": "正向", "children": [{"name": "足"}, {"name": "多"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "少"}, {"name": "不足"}, {"name": "不够"}, {"name": "没有"}]}]}, {"name": "营养", "children": [{"name": "正向", "children": [{"name": "丰富"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "食用", "children": [{"name": "正向", "children": [{"name": "方便"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "杂质", "children": [{"name": "正向"}, {"name": "中性"}, {"name": "负向", "children": [{"name": "多"}]}]}, {"name": "坏果", "children": [{"name": "正向"}, {"name": "中性"}, {"name": "负向", "children": [{"name": "多"}]}]}, {"name": "手感", "children": [{"name": "正向", "children": [{"name": "不错"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "做工", "children": [{"name": "正向", "children": [{"name": "精致"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "说明书", "children": [{"name": "正向"}, {"name": "中性"}, {"name": "负向", "children": [{"name": "没有"}]}]}]}, {"name": "色泽", "children": [{"name": "品相", "children": [{"name": "正向", "children": [{"name": "不错"}]}, {"name": "中性", "children": [{"name": "一般"}]}, {"name": "负向"}]}, {"name": "色泽", "children": [{"name": "正向", "children": [{"name": "正"}, {"name": "好"}, {"name": "金黄"}, {"name": "透亮"}, {"name": "清澈"}, {"name": "新鲜"}, {"name": "可以"}, {"name": "不错"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "暗淡"}, {"name": "不好"}]}]}, {"name": "颜色", "children": [{"name": "正向", "children": [{"name": "好看"}, {"name": "可以"}, {"name": "还行"}, {"name": "纯正"}, {"name": "正"}, {"name": "漂亮"}, {"name": "不错"}, {"name": "金黄"}, {"name": "正常"}]}, {"name": "中性", "children": [{"name": "一般"}]}, {"name": "负向", "children": [{"name": "没有"}, {"name": "发黑"}, {"name": "发黄"}, {"name": "偏黄"}, {"name": "黄的"}, {"name": "不对"}, {"name": "不好"}, {"name": "不正"}, {"name": "深"}, {"name": "淡"}, {"name": "浅"}, {"name": "不一样"}, {"name": "不鲜亮"}]}]}, {"name": "外表", "children": [{"name": "正向", "children": [{"name": "不错"}]}, {"name": "中性"}, {"name": "负向"}]}]}, {"name": "口感", "children": [{"name": "口感", "children": [{"name": "正向", "children": [{"name": "好"}, {"name": "不错"}, {"name": "可以"}, {"name": "还可以"}, {"name": "还不错"}, {"name": "还行"}, {"name": "醇厚"}, {"name": "纯正"}, {"name": "软糯"}]}, {"name": "中性", "children": [{"name": "一般"}, {"name": "一般般"}]}, {"name": "负向", "children": [{"name": "不好"}, {"name": "不太好"}, {"name": "不是很好"}, {"name": "不是特别好"}, {"name": "差"}, {"name": "不好吃"}, {"name": "不咋的"}, {"name": "一言难尽"}]}]}, {"name": "味道", "children": [{"name": "正向", "children": [{"name": "好"}, {"name": "好吃"}, {"name": "不错"}, {"name": "好极了"}, {"name": "可以"}, {"name": "还行"}, {"name": "还好"}, {"name": "尚可"}, {"name": "纯正"}, {"name": "正宗"}, {"name": "纯"}, {"name": "正"}, {"name": "甜"}, {"name": "香"}, {"name": "棒"}]}, {"name": "中性", "children": [{"name": "一般"}, {"name": "一般般"}]}, {"name": "负向", "children": [{"name": "不好"}, {"name": "不好吃"}, {"name": "不怎么好吃"}, {"name": "不太好"}, {"name": "不行"}, {"name": "不是很甜"}, {"name": "不是很好"}, {"name": "不怎么样"}, {"name": "不咋滴"}, {"name": "不咋地"}, {"name": "差了一点"}, {"name": "难吃"}, {"name": "一言难尽"}, {"name": "怪怪的"}, {"name": "奇怪"}, {"name": "怪味"}, {"name": "怪"}, {"name": "不一样"}, {"name": "难闻"}, {"name": "淡"}, {"name": "没有"}, {"name": "不甜"}, {"name": "不对"}, {"name": "变了"}, {"name": "重"}, {"name": "大"}, {"name": "差"}, {"name": "酸"}, {"name": "涩"}, {"name": "刺鼻"}, {"name": "不香"}]}]}, {"name": "香味", "children": [{"name": "正向", "children": [{"name": "浓"}]}, {"name": "中性", "children": [{"name": "一般"}]}, {"name": "负向", "children": [{"name": "没有"}, {"name": "淡"}, {"name": "没"}]}]}, {"name": "香气", "children": [{"name": "正向"}, {"name": "中性", "children": [{"name": "一般"}]}, {"name": "负向"}]}, {"name": "口味", "children": [{"name": "正向"}, {"name": "中性", "children": [{"name": "一般"}]}, {"name": "负向"}]}, {"name": "风味口感", "children": [{"name": "正向", "children": [{"name": "好"}]}, {"name": "中性", "children": [{"name": "一般"}]}, {"name": "负向"}]}, {"name": "甜度", "children": [{"name": "正向", "children": [{"name": "可以"}, {"name": "还行"}]}, {"name": "中性", "children": [{"name": "一般"}]}, {"name": "负向"}]}]}, {"name": "包装", "children": [{"name": "包装", "children": [{"name": "正向", "children": [{"name": "好"}, {"name": "完好"}, {"name": "不错"}, {"name": "精美"}, {"name": "严实"}, {"name": "完整"}, {"name": "精致"}, {"name": "完好无损"}, {"name": "可以"}, {"name": "方便"}, {"name": "完美"}, {"name": "还可以"}, {"name": "还行"}, {"name": "用心"}, {"name": "好看"}, {"name": "结实"}, {"name": "真空"}, {"name": "精细"}, {"name": "漂亮"}, {"name": "满意"}, {"name": "方便"}, {"name": "仔细"}, {"name": "独立"}, {"name": "没有破损"}, {"name": "整齐"}, {"name": "棒"}, {"name": "到位"}]}, {"name": "中性", "children": [{"name": "一般"}]}, {"name": "负向", "children": [{"name": "破损"}, {"name": "损坏"}, {"name": "简陋"}, {"name": "差"}, {"name": "不好"}, {"name": "没有"}, {"name": "破了"}, {"name": "烂了"}, {"name": "简单"}, {"name": "坏了"}, {"name": "不行"}, {"name": "不是真空"}, {"name": "漏气"}, {"name": "差劲"}, {"name": "差评"}, {"name": "随意"}, {"name": "脏"}, {"name": "破烂"}, {"name": "烂的"}, {"name": "有问题"}, {"name": "不敢恭维"}, {"name": "不一样"}]}]}, {"name": "袋子", "children": [{"name": "正向"}, {"name": "中性"}, {"name": "负向", "children": [{"name": "破了"}]}]}, {"name": "箱子", "children": [{"name": "正向"}, {"name": "中性"}, {"name": "负向", "children": [{"name": "破了"}]}]}]}, {"name": "分量", "children": [{"name": "分量", "children": [{"name": "正向", "children": [{"name": "足"}, {"name": "多"}, {"name": "可以"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "少"}, {"name": "不足"}, {"name": "不够"}]}]}, {"name": "份量", "children": [{"name": "正向", "children": [{"name": "足"}, {"name": "十足"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "不足"}, {"name": "不够"}, {"name": "少"}]}]}, {"name": "重量", "children": [{"name": "正向", "children": [{"name": "足够"}, {"name": "够"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "不够"}, {"name": "不足"}, {"name": "不对"}]}]}, {"name": "数量", "children": [{"name": "正向"}, {"name": "中性"}, {"name": "负向", "children": [{"name": "不对"}, {"name": "不够"}]}]}, {"name": "量", "children": [{"name": "正向", "children": [{"name": "足"}]}, {"name": "中性"}, {"name": "负向"}]}]}, {"name": "物流", "children": [{"name": "物流", "children": [{"name": "正向", "children": [{"name": "快"}, {"name": "迅速"}, {"name": "快速"}, {"name": "给力"}, {"name": "快捷"}, {"name": "可以"}, {"name": "还行"}, {"name": "不错"}, {"name": "满意"}]}, {"name": "中性", "children": [{"name": "一般"}]}, {"name": "负向", "children": [{"name": "慢"}, {"name": "差"}, {"name": "垃圾"}]}]}, {"name": "物流速度", "children": [{"name": "正向", "children": [{"name": "快"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "快递", "children": [{"name": "正向", "children": [{"name": "快"}, {"name": "给力"}, {"name": "还行"}, {"name": "好"}, {"name": "可以"}, {"name": "及时"}, {"name": "不错"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "慢"}, {"name": "垃圾"}, {"name": "破损"}, {"name": "差评"}, {"name": "差"}, {"name": "丢了"}, {"name": "不给力"}]}]}, {"name": "发货", "children": [{"name": "正向", "children": [{"name": "快"}, {"name": "及时"}, {"name": "迅速"}, {"name": "速度"}, {"name": "神速"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "慢"}]}]}, {"name": "发货速度", "children": [{"name": "正向", "children": [{"name": "快"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "慢"}]}]}, {"name": "发货时间", "children": [{"name": "正向"}, {"name": "中性"}, {"name": "负向", "children": [{"name": "长"}]}]}, {"name": "送货", "children": [{"name": "正向", "children": [{"name": "快"}, {"name": "及时"}, {"name": "方便"}, {"name": "快捷"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "送货速度", "children": [{"name": "正向", "children": [{"name": "快"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "慢"}]}]}, {"name": "派送", "children": [{"name": "正向"}, {"name": "中性"}, {"name": "负向", "children": [{"name": "不快"}]}]}, {"name": "配送", "children": [{"name": "正向", "children": [{"name": "快"}, {"name": "不错"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "配送速度", "children": [{"name": "正向", "children": [{"name": "快"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "速度", "children": [{"name": "正向", "children": [{"name": "还行"}, {"name": "快"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "服务", "children": [{"name": "正向", "children": [{"name": "好"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "差"}, {"name": "差评"}]}]}, {"name": "服务态度", "children": [{"name": "正向", "children": [{"name": "好"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "快递小哥", "children": [{"name": "正向", "children": [{"name": "给力"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "态度", "children": [{"name": "正向", "children": [{"name": "好"}]}, {"name": "中性"}, {"name": "负向"}]}]}, {"name": "售后", "children": [{"name": "服务", "children": [{"name": "正向", "children": [{"name": "好"}, {"name": "周到"}, {"name": "一流"}, {"name": "还行"}, {"name": "还好"}, {"name": "不错"}, {"name": "到位"}, {"name": "可以"}]}, {"name": "中性", "children": [{"name": "一般"}]}, {"name": "负向", "children": [{"name": "差"}]}]}, {"name": "服务态度", "children": [{"name": "正向", "children": [{"name": "好"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "差"}, {"name": "不好"}]}]}, {"name": "客服", "children": [{"name": "正向", "children": [{"name": "好"}, {"name": "不错"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "找不到"}, {"name": "没有"}, {"name": "没人理"}, {"name": "不理人"}, {"name": "没人回复"}, {"name": "敷衍"}, {"name": "差评"}, {"name": "差劲"}, {"name": "垃圾"}, {"name": "不理睬"}, {"name": "不理"}, {"name": "一问三不知"}]}]}, {"name": "客服态度", "children": [{"name": "正向", "children": [{"name": "好"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "卖家", "children": [{"name": "正向", "children": [{"name": "好"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "卖家服务", "children": [{"name": "正向", "children": [{"name": "好"}]}, {"name": "中性"}, {"name": "负向"}]}, {"name": "退货", "children": [{"name": "正向"}, {"name": "中性"}, {"name": "负向", "children": [{"name": "不给"}]}]}, {"name": "购物体验", "children": [{"name": "正向"}, {"name": "中性"}, {"name": "负向", "children": [{"name": "差"}, {"name": "糟糕"}]}]}, {"name": "售后", "children": [{"name": "正向", "children": [{"name": "好"}]}, {"name": "中性"}, {"name": "负向", "children": [{"name": "差"}, {"name": "无语"}]}]}]}]}
      }
    },
    mounted() {
      // this.$nextTick(() => {
      //   this.initChart()
      // })
      // console.log(benti)
      // console.log(this.dict)
      this.initChart({ renderer: "svg" })
    },
    beforeDestroy() {
      if (!this.chart) {
        return
      }
      this.chart.dispose()
      this.chart = null
    },
    methods: {

      initChart() {
        this.chart = echarts.init(this.$el)
        
        let option = {
            title: {
              text: '本体图谱',
              subtext: '层次化展示农产品评价类别\n\n点击节点展开/收起子类别',
              top: 'top',
              left: 'left'
            },
            color: ['#249EFF', '#165DFF', '#61C4C7', '#21CCFF', '#199ED8'],
            tooltip: {
                trigger: 'item',
                triggerOn: 'mousemove'
            },
            series:[
                {
                    type: 'tree',
                    data: [this.xiaofeidata],
                    color: '#249EFF',
                    top: '18%',
                    bottom: '14%',
                    layout: 'radial',
                    symbol: 'emptyCircle',
                    symbolSize: 7,
                    initialTreeDepth: 2,
                    animationDurationUpdate: 750,
                    emphasis:{
                        focus: 'descendant'
                    }
                }
            ]
        };
        this.chart.setOption(option)
      }
    }
  }
</script>

<style scoped>
  .graph {
    margin-top: 20px;
    /* background-color: red; */
  }
</style>
