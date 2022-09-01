<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
  import echarts from 'echarts'
  import 'echarts-wordcloud'
  import resize from '@/utils/echarts_resize.js'

  export default {
    name: 'WordCloud',
    mixins: [resize],
    props: {
      className: {
        type: String,
        default: 'positionloopecharts'
      },
      width: {
        type: String,
        default: '500px'
      },
      height: {
        type: String,
        default: '600px'
      }
    },
    data() {
      return {
        chart: null,
      }
    },
    mounted() {
      this.initChart()
    },
    beforeDestroy() {
      if (!this.chart) {
        return
      }
      this.chart.dispose()
      this.chart = null
    },
    methods: {
      initChart(titleText, seriesData, sizeRange) {
        this.chart = echarts.init(this.$el)
        let option = {
            title: {
                text: titleText,
                // subtext: 'Fake Data',
                left: 'center'
            },
            tooltip: {
                // trigger: 'item'
                show: true,
                position: 'top',
                textStyle: {
                    fontSize: 30
                },
            },
            // legend: {
            //     orient: 'vertical',
            //     left: 'left'
            // },
            series: [
                {
                // name: '数据详情',
                type: 'wordCloud',
                gridSize: 35,
                shape: 'circle',
                sizeRange: sizeRange,
                rotationRange: [0,0],
                left: 'center',
                top: 'center',
                right: null,
                bottom: null,
                width: '90%',
                height: '90%',
                drawOutBound: false,
                textStyle:{
                    normal:{
                        color:function(){
                            return 'rgb(' + [Math.round(Math.random() * 200 + 55), Math.round(Math.random() * 200 + 55), Math.round(Math.random() * 200 + 55)].join(',') + ')'
                        },
                    },
                    emphasis:{
                        shadowBlur: 10,
                        shadowColor: '#2ac',
                    },
                },
                data:seriesData,
                }
            ]
        }
        this.chart.setOption(option)
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

  @media screen and (max-width: 992px) {
    .home-container {
      .chart-wrapper {
        padding: 8px;
      }
    }
  }
</style>
