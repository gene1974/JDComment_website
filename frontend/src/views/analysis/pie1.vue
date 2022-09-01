<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
  import echarts from 'echarts'
  import resize from '@/utils/echarts_resize.js'

  export default {
    name: 'DataStatisticsPie1',
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
        default: '400px'
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
      initChart(titleText, subTittleText, seriesData) {
        this.chart = echarts.init(this.$el)
        let option = {
            title: {
                text: titleText,
                subtext: subTittleText,
                // subtext: 'Fake Data',
                left: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b} : {c} ({d}%)'
            },
            legend: {
            //     // type: 'scroll',
            //     orient: 'vertical',
            //     left: 'left',
            //     height: 300,
                top: 30,
            //     bottom: 50,
            //     // data: legendData,
            //     // data: ['1','2'],
            //     // formatter: function (name) {
            //     //     for(let i = 0, l = seriesData.length; i < l; i++){
            //     //         if (seriesData[i].name == name) {
            //     //             return  seriesData[i].name + ' ' + '平均评分' + seriesData[i].user_stars;
            //     //         }
            //     //     }
            //     //     return 'Legend ' + name;
            //     // },
            },
            series: [
                {
                name: '情感极性',
                type: 'pie',
                radius: '45%',
                center: ['45%', '45%'],
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
