<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
  import * as echarts from 'echarts'
  import resize from '@/utils/echarts_resize.js'

  export default {
    name: 'DataStatisticsBar0',
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
      initChart(titleText, subTittleText, Data) {
        this.chart = echarts.init(this.$el)
        // let barNameList = []
        let seriesData = []
        let POSData = []
        let NEUData = []
        let NEGData = []
        let yData = []
        for (var key in Data){
            yData.push(key)
            POSData.push(Data[key]['POS'])
            NEUData.push(Data[key]['NEU'])
            NEGData.push(Data[key]['NEG'])
            // seriesData.push({name:key,type:'bar',stack:'total',label:{show:true},emphasis: {focus: 'series'},data:[Data[key]['POS'],Data[key]['NEU'],Data[key]['NEG']]})
        }
        seriesData.push({name:'POS',type:'bar',radius: '40%',stack:'total',label:{show:true},emphasis: {focus: 'series'},data:POSData})
        seriesData.push({name:'NEU',type:'bar',radius: '40%',stack:'total',label:{show:true},emphasis: {focus: 'series'},data:NEUData})
        seriesData.push({name:'NEG',type:'bar',radius: '40%',stack:'total',label:{show:true},emphasis: {focus: 'series'},data:NEGData})
        let option = {
            title: {
                text: titleText,
                subtext: subTittleText,
                left: 'center'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    // Use axis to trigger tooltip
                    type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
                }
            },
            legend: {
                left: 'right',
                top: 30,
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'value'
            },
            yAxis: {
                type: 'category',
                data: yData,
            },
            series: seriesData,
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
