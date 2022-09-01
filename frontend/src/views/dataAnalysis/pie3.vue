<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
  import echarts from 'echarts'
  import resize from '@/utils/echarts_resize.js'

  export default {
    name: 'DataStatisticsPie0',
    mixins: [resize],
    props: {
      className: {
        type: String,
        default: 'chart'
      },
      width: {
        type: String,
        default: '400px'
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
        let seriesData = []
        for (var index in Data){
            seriesData.push({value:Data[index]['number'],name:Data[index]['target']})
        }
        let option = {
            color: ['#63b2ee', '#76da91', '#f8cb7f', '#f89588', '#7cd6cf'],
            title: {
                text: titleText,
                subtext: subTittleText,
                left: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b} : {c} ({d}%)'
            },
            legend: {
                orient: 'vertical',
                left: 'left',
                height: 120,
                type: 'scroll',
                selectedMode: false,
            },
            series: [
                {
                name: '评价对象',
                type: 'pie',
                radius: '50%',
                center: ['50%', '60%'],
                data:seriesData,
                emphasis: {
                    itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
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
