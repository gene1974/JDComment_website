<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
  import echarts from 'echarts'
  import resize from '@/utils/echarts_resize.js'

  export default {
    name: 'Bar0',
    mixins: [resize],
    props: {
      className: {
        type: String,
        default: 'chart'
      },
      width: {
        type: String,
        default: '300px'
      },
      height: {
        type: String,
        default: '300px'
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
      initChart(titleText, subTittleText, Data) {
        this.chart = echarts.init(this.$el)
        // let barNameList = []
        let yData = []
        let xData = []
        for (var index in Data){
            xData.push(Data[index]['date'])
            yData.push(Data[index]['comment_number'])
        }
        let option = {
            title: {
                text: '评价热度',
                subtext: '按日统计消费者的评价数量',
                left: 'center'
            },
            xAxis: {
                type: 'category',
                data: xData,
                name: '日期',
            },
            yAxis: {
                type: 'value',
                name: '评价数量',
                // data: yData,
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            series: {
              data: yData,
              type: 'bar',
              showBackground: true,
              backgroundStyle: {
                color: 'rgba(180, 180, 180, 0.2)'
              },
              color: 'rgb(50, 150, 250)',
            },
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                type: 'cross'
              }
            }
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
    // position: relative;
    position: fixed;

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
