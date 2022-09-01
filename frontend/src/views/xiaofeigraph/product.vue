<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>
<!-- <template>
  <div ref="mychart" class="graph" :style="{height:height,width:width}"></div>
</template> -->

 <!-- <script>
  import echarts from 'echarts'
  import resize from '@/utils/echarts_resize.js'

  export default {
    name: 'KgProduct',
    mixins: [resize],
    props: {
      width: {
        type: String,
        default: '600px'
      },
      height: {
        type: String,
        default: '600px'
      },
    },
    data() {
      return {
        chart: null,
        // dict:benti,
        nodes: [],
        links: [],
        ProductData: {'name': '大米', 'children': [{'name': '价格', 'children': [{'name': '价', 'children': ['平时比活动价还便宜']}, {'name': '价格', 'children': ['便宜']}, {'name': '保价', 'children': ['降价不退钱']}, {'name': '价格', 'children': ['不便宜']}, {'name': '价格', 'children': ['比超市便宜']}, {'name': '价格', 'children': ['值']}, {'name': '价格', 'children': ['便宜']}, {'name': '价格', 'children': ['还可以']}, {'name': '', 'children': ['物美价廉']}, {'name': '价格', 'children': ['便宜']}, {'name': '价位', 'children': ['便宜']}, {'name': '价格', 'children': ['有点小贵']}, {'name': '性价比', 'children': ['一般']}, {'name': '价格', 'children': ['变来变去的']}, {'name': '差价', 'children': ['不能退']}, {'name': '米', 'children': ['价廉物美']}, {'name': '价格', 'children': ['实惠']}, {'name': '价格', 'children': ['香']}, {'name': '', 'children': ['便宜']}, {'name': '价格', 'children': ['便宜']}, {'name': '', 'children': ['偏贵了']}, {'name': '价格', 'children': ['变动太频繁']}, {'name': '', 'children': ['才一个礼拜就减价促销']}, {'name': '', 'children': ['不贵']}, {'name': '价格', 'children': ['不值这个价格']}, {'name': '', 'children': ['不值这个价钱']}, {'name': '香米', 'children': ['非常划算']}, {'name': '价格', 'children': ['偏贵']}, {'name': '价格', 'children': ['实惠']}, {'name': '', 'children': ['不贵']}, {'name': '价格', 'children': ['对不起价格']}, {'name': '价', 'children': ['廉']}, {'name': '价格', 'children': ['小贵']}, {'name': '价格', 'children': ['也不贵']}, {'name': '价', 'children': ['廉']}, {'name': '', 'children': ['胜在便宜']}, {'name': '价格', 'children': ['实惠']}, {'name': '性价比', 'children': ['高']}, {'name': '价格', 'children': ['高']}, {'name': '价格', 'children': ['略贵']}, {'name': '', 'children': ['不划算']}, {'name': '价', 'children': ['不值']}, {'name': '价格', 'children': ['不值得']}, {'name': '', 'children': ['便宜']}, {'name': '价格', 'children': ['比较实惠']}, {'name': '价格', 'children': ['合理']}, {'name': '价格', 'children': ['实惠']}, {'name': '', 'children': ['涨价']}, {'name': '价钱', 'children': ['不值']}, {'name': '', 'children': ['不能价格保护']}, {'name': '大米', 'children': ['便宜']}, {'name': '价格', 'children': ['贵']}, {'name': '价格', 'children': ['不值']}, {'name': '', 'children': ['便宜多了']}, {'name': '价格', 'children': ['实惠']}, {'name': '优惠', 'children': ['比较多']}, {'name': '', 'children': ['不值这个价']}, {'name': '', 'children': ['与价格有点不符']}, {'name': '价钱', 'children': ['不值']}, {'name': '性价比', 'children': ['还不错']}, {'name': '价格', 'children': ['适中']}, {'name': '', 'children': ['比超市便宜几块']}, {'name': '价格', 'children': ['小贵']}, {'name': '价', 'children': ['不值']}, {'name': '价格', 'children': ['实惠']}, {'name': '价钱', 'children': ['也差不多']}, {'name': '', 'children': ['每袋降10元']}, {'name': '', 'children': ['一点都不保值']}]}, {'name': '品质', 'children': [{'name': '大米', 'children': ['很不错']}, {'name': '产品香气', 'children': ['一般']}, {'name': '货品', 'children': ['很好']}, {'name': '质量', 'children': ['很一般']}, {'name': '性价比', 'children': ['超级低']}, {'name': '米香', 'children': ['没有']}, {'name': '品质', 'children': ['不相符']}, {'name': '质量', 'children': ['不一样']}, {'name': '', 'children': ['不新鲜']}, {'name': '', 'children': ['还不错']}, {'name': '米', 'children': ['有黑的']}, {'name': '米', 'children': ['还好']}, {'name': '大米', 'children': ['不错']}, {'name': '米', 'children': ['不好']}, {'name': '', 'children': ['挺好的']}, {'name': '米', 'children': ['变质']}, {'name': '米', 'children': ['一般']}, {'name': '质量', 'children': ['很好']}, {'name': '米香', 'children': ['good']}, {'name': '日期', 'children': ['新鲜']}, {'name': '大米', 'children': ['一般']}, {'name': '品质', 'children': ['一般']}, {'name': '大米', 'children': ['很好']}, {'name': '品质', 'children': ['特别好']}, {'name': '商品质量', 'children': ['可以']}, {'name': '大米', 'children': ['非常好']}, {'name': '颗粒', 'children': ['饱满']}, {'name': '宝贝', 'children': ['非常喜欢']}, {'name': '', 'children': ['差']}, {'name': '颗粒', 'children': ['非常小']}, {'name': '东西', 'children': ['很好']}, {'name': '质量', 'children': ['可以']}, {'name': '', 'children': ['一点都不好']}, {'name': '杂物', 'children': ['多']}, {'name': '味道', 'children': ['不对']}, {'name': '米', 'children': ['非常不行']}, {'name': '品质', 'children': ['差很多']}, {'name': '质量', 'children': ['还行']}, {'name': '颗粒', 'children': ['饱满']}, {'name': '米粒', 'children': ['完整']}, {'name': '', 'children': ['一般般，不好不坏']}, {'name': '颗粒', 'children': ['饱满']}, {'name': '大米质量', 'children': ['好']}, {'name': '米', 'children': ['有一股放着时间比较久的味道']}, {'name': '粒粒', 'children': ['饱满']}, {'name': '大米', 'children': ['还算不错吧']}, {'name': '米', 'children': ['不错']}, {'name': '颗粒', 'children': ['饱满']}, {'name': '品质', 'children': ['有保证']}, {'name': '', 'children': ['不是很满意']}, {'name': '红豆', 'children': ['非常满意']}, {'name': '质量', 'children': ['一般']}, {'name': '质量', 'children': ['很好']}, {'name': '', 'children': ['感觉有点上当']}, {'name': '大米', 'children': ['颗粒大']}, {'name': '米', 'children': ['煮饭不香']}, {'name': '蒸出来的米', 'children': ['发黑']}, {'name': '', 'children': ['颗粒小']}, {'name': '米', 'children': ['不怎么样']}, {'name': '', 'children': ['颗粒小']}, {'name': '', 'children': ['煮饭颜色又黄又干不好吃']}, {'name': '米粒', 'children': ['饱满圆润光滑']}, {'name': '米粒', 'children': ['饱满']}, {'name': '泰国香米', 'children': ['米粒长']}, {'name': '', 'children': ['不怎么好']}, {'name': '质量', 'children': ['还行']}, {'name': '米粒', 'children': ['稍小']}, {'name': '', 'children': ['东西不错']}, {'name': '糯米', 'children': ['一般']}, {'name': '', 'children': ['看上去挺不错的']}, {'name': '', 'children': ['买到的可能是陈米']}, {'name': '', 'children': ['颗粒碎']}, {'name': '米', 'children': ['质量不好']}, {'name': '米', 'children': ['一点香味也没有']}, {'name': '米', 'children': ['放很久了']}, {'name': '', 'children': ['味较淡']}, {'name': '', 'children': ['感觉是老米']}, {'name': '', 'children': ['新鲜']}, {'name': '香气', 'children': ['不佳']}, {'name': '', 'children': ['只能算一般']}, {'name': '米', 'children': ['很干净']}, {'name': '米', 'children': ['不香']}, {'name': '', 'children': ['一般般']}, {'name': '质量', 'children': ['很好']}, {'name': '大米', 'children': ['太垃圾了']}, {'name': '米', 'children': ['感觉若有若无的霉味']}, {'name': '质量', 'children': ['肯定没问题']}, {'name': '米', 'children': ['像陈米']}, {'name': '米', 'children': ['一般']}, {'name': '米', 'children': ['没比我买的2块6的米好']}, {'name': '大米', 'children': ['看起来不错']}, {'name': '', 'children': ['不太像新米']}, {'name': '个头', 'children': ['太小']}, {'name': '', 'children': ['有小黑颗粒']}, {'name': '日期', 'children': ['新鲜']}, {'name': '豆子', 'children': ['颗粒饱满']}, {'name': '', 'children': ['感觉湿湿的']}, {'name': '', 'children': ['吃起来还可以?']}, {'name': '颗粒', 'children': ['饱满']}, {'name': '米', 'children': ['非常好']}, {'name': '大米', 'children': ['不错的']}, {'name': '珍珠米', 'children': ['千万不买']}, {'name': '', 'children': ['再也不买了']}, {'name': '物', 'children': ['美']}, {'name': '品质', 'children': ['一般']}, {'name': '颗粒', 'children': ['饱']}, {'name': '', 'children': ['非常干净']}, {'name': '品质', 'children': ['正品']}, {'name': '做出来的饭', 'children': ['一点米的香味都没']}, {'name': '米饭', 'children': ['松散']}, {'name': '质量', 'children': ['非常一般']}, {'name': '质量', 'children': ['一般']}, {'name': '碎米', 'children': ['颗粒小']}, {'name': '大米', 'children': ['很新鲜']}, {'name': '大米', 'children': ['很高档的']}, {'name': '米', 'children': ['也不算太发']}, {'name': '', 'children': ['并没有几种杂粮']}, {'name': '', 'children': ['里面掺杂碎米']}, {'name': '颗粒', 'children': ['饱满']}, {'name': '', 'children': ['没有一点香味']}, {'name': '', 'children': ['说的是长粒米打开确是短粒米']}, {'name': '', 'children': ['陈米']}, {'name': '大米', 'children': ['不错']}, {'name': '米', 'children': ['挺不错']}, {'name': '东西', 'children': ['很不错']}, {'name': '质量', 'children': ['好']}, {'name': '整体', 'children': ['还行吧']}, {'name': '', 'children': ['真香']}, {'name': '质量', 'children': ['没食体店大米质量好']}, {'name': '大米', 'children': ['长虫子']}, {'name': '质量', 'children': ['很好']}, {'name': '颗粒', 'children': ['饱满']}, {'name': '质量', 'children': ['不错']}, {'name': '', 'children': ['有股怪味']}, {'name': '大米', 'children': ['都是陈米']}, {'name': '煮出来的饭', 'children': ['一般般']}, {'name': '质量', 'children': ['很好']}, {'name': '米粒', 'children': ['细细小小的']}, {'name': '', 'children': ['有股异味']}, {'name': '质量', 'children': ['一般']}, {'name': '香气', 'children': ['没什么香味']}, {'name': '', 'children': ['一股陈米味']}, {'name': '', 'children': ['不是很香']}, {'name': '质量', 'children': ['很好']}, {'name': '', 'children': ['还可以啊']}, {'name': '货', 'children': ['烂']}, {'name': '质量', 'children': ['挺好']}, {'name': '质量', 'children': ['好']}, {'name': '', 'children': ['物美价廉']}, {'name': '品质', 'children': ['非常好']}, {'name': '香气', 'children': ['就那样']}, {'name': '日期', 'children': ['不够新鲜']}, {'name': '米', 'children': ['生虫了']}, {'name': '', 'children': ['不新鲜']}, {'name': '', 'children': ['看着不错']}, {'name': '香米', 'children': ['还行吧']}, {'name': '香米', 'children': ['没有想象中的好']}, {'name': '米', 'children': ['有虫子']}, {'name': '产品质量', 'children': ['一般']}, {'name': '大米', 'children': ['大小均匀']}, {'name': '性价比', 'children': ['很差']}, {'name': '', 'children': ['长虫']}, {'name': '丝苗米', 'children': ['假的']}, {'name': '米粒', 'children': ['比较饱满']}, {'name': '颗粒', 'children': ['很小']}, {'name': '米饭', 'children': ['没有香味']}, {'name': '颗粒', 'children': ['饱满']}, {'name': '金龙鱼', 'children': ['很不错']}, {'name': '东西', 'children': ['还不错']}, {'name': '产品香气', 'children': ['好']}, {'name': '产地', 'children': ['正']}, {'name': '', 'children': ['物有所值']}, {'name': '', 'children': ['不错的']}, {'name': '质量', 'children': ['可以']}, {'name': '米', 'children': ['还好']}, {'name': '', 'children': ['洗很多遍煮出来的饭还是不好']}, {'name': '大米', 'children': ['一般般']}, {'name': '大米', 'children': ['没有啥特色']}, {'name': '大米', 'children': ['值得购买']}, {'name': '大米', 'children': ['特别满意']}, {'name': '大米', 'children': ['感觉非常好']}, {'name': '颗粒', 'children': ['饱满']}, {'name': '绿豆', 'children': ['不好']}, {'name': '绿豆', 'children': ['煮不烂的死豆']}, {'name': '', 'children': ['开花的有磕牙的']}, {'name': '米饭', 'children': ['喜欢']}, {'name': '日期', 'children': ['1月份的']}, {'name': '日期', 'children': ['不是那么的新鲜']}, {'name': '大米', 'children': ['不错']}, {'name': '质量', 'children': ['很好']}, {'name': '米', 'children': ['普通']}, {'name': '米', 'children': ['没什么特色']}, {'name': '米', 'children': ['很差']}, {'name': '米', 'children': ['不干净']}, {'name': '糙米', 'children': ['有点细长']}, {'name': '小站稻', 'children': ['正宗']}, {'name': '颗粒', 'children': ['均匀、透亮']}, {'name': '质量', 'children': ['一般']}, {'name': '大米', 'children': ['都生虫了']}, {'name': '大米', 'children': ['不新鲜']}, {'name': '八宝粥米', 'children': ['有发霉的']}, {'name': '', 'children': ['不是长粒米']}, {'name': '米香', 'children': ['没有其他几款香']}, {'name': '效果', 'children': ['超级好']}, {'name': '质量', 'children': ['不如散称米']}, {'name': '', 'children': ['虫子了']}, {'name': '', 'children': ['有米渣']}, {'name': '', 'children': ['很像是有米虫的样子']}, {'name': '', 'children': ['一般一般']}, {'name': '', 'children': ['还算新鲜']}, {'name': '', 'children': ['还可以']}, {'name': '质量', 'children': ['一般']}, {'name': '颗粒', 'children': ['饱满']}, {'name': '质量', 'children': ['一如既往地靠谱']}, {'name': '', 'children': ['非常值得推荐']}, {'name': '颗粒', 'children': ['分明']}, {'name': '', 'children': ['毫无粘性']}, {'name': '', 'children': ['假货']}, {'name': '', 'children': ['没有香味']}, {'name': '米粒', 'children': ['饱满']}, {'name': '米粒', 'children': ['干净新鲜']}, {'name': '', 'children': ['一般']}, {'name': '', 'children': ['好像也不怎么香']}, {'name': '颗粒', 'children': ['饱满']}, {'name': '大米', 'children': ['不会很碎']}, {'name': '颗粒', 'children': ['还可以']}, {'name': '', 'children': ['不象是新米']}, {'name': '大米', 'children': ['真的很不错']}, {'name': '', 'children': ['没有让我失望哦']}, {'name': '', 'children': ['一般般']}, {'name': '', 'children': ['跟吃过的香米不一样']}, {'name': '米', 'children': ['不对劲']}, {'name': '米', 'children': ['没有之前那么颗粒分明']}, {'name': '', 'children': ['谈不上新米']}, {'name': '', 'children': ['挺好的']}]}, {'name': '色泽', 'children': [{'name': '颜色', 'children': ['暗黄']}, {'name': '米色', 'children': ['光亮']}, {'name': '颜色', 'children': ['发黄']}, {'name': '米的颜色', 'children': ['较暗']}, {'name': '颜色', 'children': ['正']}, {'name': '米', 'children': ['发黄']}, {'name': '颜色', 'children': ['偏黑']}, {'name': '大米', 'children': ['颜色比较清亮']}, {'name': '颜色', 'children': ['发黑']}, {'name': '色泽', 'children': ['不佳']}, {'name': '颜色', 'children': ['比较暗沉']}, {'name': '米', 'children': ['发黑']}, {'name': '米', 'children': ['有点发黑']}, {'name': '色泽', 'children': ['不像是新米']}, {'name': '蒸出米饭', 'children': ['发黑']}, {'name': '', 'children': ['难看']}, {'name': '颜色', 'children': ['有两种']}, {'name': '色泽', 'children': ['不好']}, {'name': '颜色', 'children': ['暗淡发黄']}, {'name': '米粒', 'children': ['光亮']}, {'name': '颜色', 'children': ['偏黄']}, {'name': '大米', 'children': ['发黑']}, {'name': '', 'children': ['有点发黑']}, {'name': '大米', 'children': ['发黄']}, {'name': '米粒', 'children': ['发黄']}, {'name': '色泽', 'children': ['偏黄']}, {'name': '颜色', 'children': ['很差']}, {'name': '米', 'children': ['很黑']}, {'name': '颜色', 'children': ['发暗']}, {'name': '米', 'children': ['发黄']}, {'name': '颜色', 'children': ['一般']}, {'name': '颜色', 'children': ['不是特别的金黄色']}, {'name': '颜色', 'children': ['也有点暗']}, {'name': '色泽', 'children': ['一般']}]}, {'name': '口感', 'children': [{'name': '风味口感', 'children': ['一般']}, {'name': '口味', 'children': ['还好']}, {'name': '口感', 'children': ['好']}, {'name': '饭', 'children': ['没什么香味']}, {'name': '米', 'children': ['差']}, {'name': '口感', 'children': ['硬绷绷']}, {'name': '香味', 'children': ['没']}, {'name': '香气', 'children': ['没']}, {'name': '口感', 'children': ['很一般']}, {'name': '', 'children': ['不好吃']}, {'name': '米香', 'children': ['没']}, {'name': '大米', 'children': ['比较香']}, {'name': '口味', 'children': ['没有那么纯香']}, {'name': '米', 'children': ['很柔软']}, {'name': '风味口感', 'children': ['垃圾，好难吃']}, {'name': '口感', 'children': ['还行']}, {'name': '口感', 'children': ['喜欢']}, {'name': '甜味', 'children': ['没有']}, {'name': '味道', 'children': ['不错']}, {'name': '口感', 'children': ['好']}, {'name': '口感', 'children': ['弹牙']}, {'name': '产品香气', 'children': ['吃不出半点米香']}, {'name': '口感', 'children': ['不太好']}, {'name': '风味口感', 'children': ['非常好吃']}, {'name': '大米', 'children': ['好吃']}, {'name': '口感', 'children': ['没有前几年的口感好了']}, {'name': '产品香气', 'children': ['一般']}, {'name': '风味口感', 'children': ['太差了']}, {'name': '珍珠米', 'children': ['很香，很好吃']}, {'name': '米', 'children': ['很香']}, {'name': '口感', 'children': ['非常差']}, {'name': '香味', 'children': ['没']}, {'name': '口感', 'children': ['非常好吃']}, {'name': '风味口感', 'children': ['不好吃']}, {'name': '产品香气', 'children': ['没香味']}, {'name': '口感', 'children': ['不好']}, {'name': '米', 'children': ['没有最早时期那么好吃了']}, {'name': '米', 'children': ['很难吃']}, {'name': '米的口感', 'children': ['很好']}, {'name': '米香味', 'children': ['很重']}, {'name': '口感', 'children': ['很重']}, {'name': '米', 'children': ['很香']}, {'name': '饭', 'children': ['特别好吃']}, {'name': '口感', 'children': ['不像宣传的那么香软']}, {'name': '味道', 'children': ['清香']}, {'name': '味道', 'children': ['']}, {'name': '米香味', 'children': ['没']}, {'name': '口感', 'children': ['会有差别']}, {'name': '红豆', 'children': ['香甜']}, {'name': '口感', 'children': ['很一般']}, {'name': '味道', 'children': ['一般']}, {'name': '', 'children': ['煮出来的米饭很好吃']}, {'name': '', 'children': ['软硬适中']}, {'name': '口感', 'children': ['一般']}, {'name': '', 'children': ['好吃']}, {'name': '', 'children': ['真的不好吃']}, {'name': '口感', 'children': ['一般']}, {'name': '', 'children': ['不好吃']}, {'name': '味道', 'children': ['没有以前的那么好']}, {'name': '', 'children': ['好吃']}, {'name': '口感', 'children': ['差']}, {'name': '口感', 'children': ['不错']}, {'name': '大米', 'children': ['真难吃']}, {'name': '米', 'children': ['不好吃']}, {'name': '', 'children': ['不好吃']}, {'name': '', 'children': ['太好吃了']}, {'name': '油脂', 'children': ['比较少']}, {'name': '口感', 'children': ['一般']}, {'name': '珍珠米', 'children': ['不好吃']}, {'name': '口感', 'children': ['好']}, {'name': '口感', 'children': ['和之前买的大袋包装的口感天差地别']}, {'name': '', 'children': ['非常难吃']}, {'name': '口感', 'children': ['不像是新米']}, {'name': '', 'children': ['不好吃']}, {'name': '煮饭', 'children': ['好吃']}, {'name': '煲粥', 'children': ['美味']}, {'name': '口感', 'children': ['很好']}, {'name': '口感', 'children': ['还可以']}, {'name': '', 'children': ['老公说不太好吃']}, {'name': '风味口感', 'children': ['没有想象的好']}, {'name': '', 'children': ['香甜可口']}, {'name': '', 'children': ['难吃']}, {'name': '口感', 'children': ['不错']}, {'name': '', 'children': ['有霉味']}, {'name': '小粒米', 'children': ['好吃']}, {'name': '味道', 'children': ['不新鲜']}, {'name': '米', 'children': ['实在难吃']}, {'name': '', 'children': ['吃着没啥感觉']}, {'name': '口感', 'children': ['一般']}, {'name': '饭', 'children': ['香甜可囗']}, {'name': '', 'children': ['吃起来没问题']}, {'name': '口感', 'children': ['好吃']}, {'name': '口感', 'children': ['一般']}, {'name': '', 'children': ['没有米香']}, {'name': '味道', 'children': ['一般']}, {'name': '', 'children': ['不好吃']}, {'name': '', 'children': ['香甜可口']}, {'name': '', 'children': ['不太好吃']}, {'name': '味道', 'children': ['一般般']}, {'name': '口感', 'children': ['一般']}, {'name': '口感', 'children': ['一般']}, {'name': '口感', 'children': ['一般']}, {'name': '风味口感', 'children': ['好']}, {'name': '口感', 'children': ['一点不好']}, {'name': '', 'children': ['吃着挺筋道']}, {'name': '味道', 'children': ['很差']}, {'name': '味道', 'children': ['正宗']}, {'name': '', 'children': ['没比其他品牌的好吃']}, {'name': '口感', 'children': ['软糯']}, {'name': '', 'children': ['实在难吃']}, {'name': '口感', 'children': ['不错']}, {'name': '口感', 'children': ['好']}, {'name': '', 'children': ['吃起来一般']}, {'name': '口感', 'children': ['还行']}, {'name': '米饭', 'children': ['很难吃']}, {'name': '大米', 'children': ['一般般']}, {'name': '米', 'children': ['很干']}, {'name': '米', 'children': ['特别硬']}, {'name': '风味口感', 'children': ['完美']}, {'name': '口感', 'children': ['不香']}, {'name': '大米', 'children': ['应该好吃']}, {'name': '', 'children': ['不新鲜']}, {'name': '米', 'children': ['不好吃']}, {'name': '口感', 'children': ['绵软']}, {'name': '', 'children': ['不好吃']}, {'name': '米', 'children': ['很难吃']}, {'name': '米', 'children': ['没有香味']}, {'name': '米香味', 'children': ['浓浓的']}, {'name': '米', 'children': ['不咋样']}, {'name': '味道', 'children': ['还可以']}, {'name': '口感', 'children': ['很差']}, {'name': '风味口感', 'children': ['好']}, {'name': '', 'children': ['很好吃']}, {'name': '大米', 'children': ['香的']}, {'name': '', 'children': ['不好吃']}, {'name': '口感', 'children': ['平常']}, {'name': '大米', 'children': ['不好吃']}, {'name': '大米', 'children': ['粗糙']}, {'name': '大米', 'children': ['蒸熟没有一点香味']}, {'name': '口感', 'children': ['很好']}, {'name': '口感', 'children': ['很香']}, {'name': '大米', 'children': ['好吃']}, {'name': '米饭', 'children': ['软糯可口']}, {'name': '味道', 'children': ['不错']}, {'name': '口感', 'children': ['一般']}, {'name': '口感', 'children': ['没有惊喜']}, {'name': '', 'children': ['煮饭很香滑']}, {'name': '口感', 'children': ['一般']}, {'name': '', 'children': ['不好吃']}, {'name': '', 'children': ['硬硬的']}, {'name': '味道', 'children': ['和普通米没有区别']}, {'name': '口感', 'children': ['一般']}, {'name': '口感', 'children': ['略差']}, {'name': '味道', 'children': ['不错']}, {'name': '味道', 'children': ['特别的香']}, {'name': '味道', 'children': ['非常好吃']}, {'name': '', 'children': ['既不香也不糯']}, {'name': '香米', 'children': ['还不如在超市买的好吃']}, {'name': '口感', 'children': ['不好']}, {'name': '米', 'children': ['很香']}, {'name': '米', 'children': ['很好吃']}, {'name': '', 'children': ['香甜可口']}, {'name': '', 'children': ['没有米香']}, {'name': '大米', 'children': ['非常好吃']}, {'name': '口感', 'children': ['很好']}, {'name': '大米', 'children': ['很好吃']}, {'name': '大米', 'children': ['吃起来很香']}, {'name': '', 'children': ['吃着一点都不香']}, {'name': '口感', 'children': ['绵软']}, {'name': '', 'children': ['有浓浓的米饭的味道']}, {'name': '', 'children': ['感觉到什么香味']}, {'name': '口感', 'children': ['很差']}, {'name': '大米', 'children': ['一点不糯']}, {'name': '', 'children': ['有一股清香味']}]}, {'name': '包装', 'children': [{'name': '包装', 'children': ['很好']}, {'name': '产品包装', 'children': ['好']}, {'name': '包装', 'children': ['完美']}, {'name': '袋', 'children': ['漏气']}, {'name': '包装', 'children': ['有破损']}, {'name': '', 'children': ['有点漏了']}, {'name': '包装', 'children': ['有破损']}, {'name': '产品包装', 'children': ['简陋']}, {'name': '外包装', 'children': ['漏了']}, {'name': '包装', 'children': ['破损']}, {'name': '包装', 'children': ['仔细']}, {'name': '包装', 'children': ['质量不好']}, {'name': '包装', 'children': ['破损']}, {'name': '包装', 'children': ['不错']}, {'name': '包装', 'children': ['漏气']}, {'name': '包装', 'children': ['很好']}, {'name': '产品包装', 'children': ['非常好']}, {'name': '真空', 'children': ['没有']}, {'name': '包装', 'children': ['破损']}, {'name': '重量', 'children': ['无']}, {'name': '包装', 'children': ['很好']}, {'name': '包装', 'children': ['气都漏了']}, {'name': '包装', 'children': ['破损']}, {'name': '包装', 'children': ['真空']}, {'name': '产品包装', 'children': ['就那样']}, {'name': '包装', 'children': ['是真空']}, {'name': '包装', 'children': ['不是真空']}, {'name': '包装', 'children': ['精美，完好无损']}, {'name': '包装', 'children': ['完好']}, {'name': '包装', 'children': ['非常严实']}, {'name': '包装', 'children': ['特别精美']}, {'name': '包装', 'children': ['好']}, {'name': '包装', 'children': ['真空']}, {'name': '包装', 'children': ['太差劲了']}, {'name': '包装', 'children': ['污损']}, {'name': '', 'children': ['一袋跑气了']}, {'name': '米', 'children': ['有一袋破了']}, {'name': '包装', 'children': ['太陋']}, {'name': '包装', 'children': ['严实']}, {'name': '包装', 'children': ['不是很满意']}, {'name': '', 'children': ['两袋不是真空']}, {'name': '', 'children': ['**玩意，无包装']}, {'name': '', 'children': ['漏气']}, {'name': '包装', 'children': ['精细']}, {'name': '包装', 'children': ['很好']}, {'name': '包装', 'children': ['真空']}, {'name': '包装', 'children': ['精细']}, {'name': '包装', 'children': ['漏了']}, {'name': '包装', 'children': ['很好']}, {'name': '包装', 'children': ['非常好']}, {'name': '包装', 'children': ['不是真空']}, {'name': '包装', 'children': ['不是一真空']}, {'name': '包装', 'children': ['完整']}, {'name': '', 'children': ['漏气了']}, {'name': '包装', 'children': ['好']}, {'name': '包装', 'children': ['完好']}, {'name': '', 'children': ['有一包漏气的']}, {'name': '', 'children': ['每次都是破损的']}, {'name': '包装', 'children': ['真空']}, {'name': '', 'children': ['没我以前那款好吃']}, {'name': '包装', 'children': ['只有一包真空']}, {'name': '包装', 'children': ['差了点']}, {'name': '', 'children': ['漏气']}, {'name': '包装', 'children': ['是完整的']}, {'name': '包装', 'children': ['把手居然都没了']}, {'name': '包装', 'children': ['两个漏气的']}, {'name': '包装', 'children': ['简陋']}, {'name': '包装', 'children': ['真空']}, {'name': '包装', 'children': ['破损了']}, {'name': '包装', 'children': ['还可以']}, {'name': '', 'children': ['有一袋漏气了']}, {'name': '产品包装', 'children': ['好']}, {'name': '包装', 'children': ['很完整']}, {'name': '包装', 'children': ['坏']}, {'name': '袋', 'children': ['破了']}, {'name': '包装', 'children': ['完好无损']}, {'name': '包装', 'children': ['一袋真空']}, {'name': '包装', 'children': ['一袋就是破损的']}, {'name': '包装', 'children': ['保鲜膜缠绕']}, {'name': '包装', 'children': ['漏气']}, {'name': '包装', 'children': ['非真空']}, {'name': '包装', 'children': ['太差']}, {'name': '', 'children': ['一袋抽真空一袋没有真空']}, {'name': '产品包装', 'children': ['漂亮']}, {'name': '', 'children': ['漏气了']}, {'name': '包装', 'children': ['']}, {'name': '袋子', 'children': ['漏的']}, {'name': '包装', 'children': ['整齐']}, {'name': '产品包装', 'children': ['和图片不符']}, {'name': '袋子', 'children': ['一大半都是破的']}, {'name': '产品包装', 'children': ['好']}, {'name': '包装', 'children': ['真空']}, {'name': '', 'children': ['漏气']}, {'name': '包装', 'children': ['完好']}, {'name': '包装', 'children': ['已经破了']}, {'name': '真空', 'children': ['保持的不错']}, {'name': '真空', 'children': ['没有发生漏气']}, {'name': '包装', 'children': ['严实']}, {'name': '包装', 'children': ['很失望']}, {'name': '包装', 'children': ['都是漏气的']}, {'name': '包装', 'children': ['好']}, {'name': '', 'children': ['漏气了']}, {'name': '包装', 'children': ['破损']}, {'name': '大米', 'children': ['已外漏']}, {'name': '包装', 'children': ['简易']}, {'name': '包装', 'children': ['破碎']}, {'name': '包装', 'children': ['漏气']}, {'name': '口子', 'children': ['还不小']}, {'name': '包装', 'children': ['坏了']}, {'name': '包装', 'children': ['外包装都没有一个']}, {'name': '包装', 'children': ['太差了']}, {'name': '包装', 'children': ['方便']}]}, {'name': '分量', 'children': [{'name': '分量', 'children': ['少']}, {'name': '重量', 'children': ['不够']}, {'name': '油', 'children': ['满减都是坑']}, {'name': '重量', 'children': ['应该是足的']}, {'name': '份量', 'children': ['也太少了']}, {'name': '重量', 'children': ['不够']}, {'name': '重量', 'children': ['亏损']}]}, {'name': '物流', 'children': [{'name': '物流速度', 'children': ['快']}, {'name': '速度', 'children': ['快']}, {'name': '物流', 'children': ['慢']}, {'name': '送货速度', 'children': ['不错']}, {'name': '送货员', 'children': ['很不错']}, {'name': '物流', 'children': ['快']}, {'name': '配送员', 'children': ['态度好']}, {'name': '发货', 'children': ['很快']}, {'name': '发货', 'children': ['及时']}, {'name': '物流速度', 'children': ['快']}, {'name': '送货', 'children': ['快捷']}, {'name': '服务', 'children': ['好']}, {'name': '发货速度', 'children': ['很好']}, {'name': '物流速度', 'children': ['很快']}, {'name': '送货速度', 'children': ['快']}, {'name': '物流速度', 'children': ['很快']}, {'name': '物流', 'children': ['非常快']}, {'name': '快递', 'children': ['很快']}, {'name': '物流', 'children': ['快速']}, {'name': '送货', 'children': ['挺好的']}, {'name': '服务', 'children': ['真好']}, {'name': '送货', 'children': ['真好']}, {'name': '物流', 'children': ['很快']}, {'name': '送货', 'children': ['快']}, {'name': '物流速度', 'children': ['快']}, {'name': '送货速度', 'children': ['快']}, {'name': '运输', 'children': ['快捷']}, {'name': '物流', 'children': ['真快']}, {'name': '送货速度', 'children': ['快']}, {'name': '物流', 'children': ['度快']}, {'name': '物流', 'children': ['太差']}, {'name': '快递', 'children': ['很快']}, {'name': '快递员', 'children': ['送到挺快']}, {'name': '快递', 'children': ['很快']}, {'name': '快递', 'children': ['一车东西乱七八糟的']}, {'name': '快递', 'children': ['挺速度']}, {'name': '', 'children': ['19.1.15日下单，2.25日送货']}, {'name': '速度', 'children': ['还可以']}, {'name': '快递员工', 'children': ['服务态度非常好']}, {'name': '快递小哥', 'children': ['服务很差']}, {'name': '物流', 'children': ['快']}, {'name': '物流', 'children': ['特别快']}, {'name': '送货', 'children': ['很快']}, {'name': '配送货', 'children': ['及时']}, {'name': '送货', 'children': ['及时']}, {'name': '发货', 'children': ['快']}, {'name': '发货', 'children': ['快']}, {'name': '物流', 'children': ['很快']}, {'name': '快递', 'children': ['送货快']}, {'name': '快递', 'children': ['真心好']}, {'name': '物流', 'children': ['超快']}, {'name': '快递', 'children': ['不作为']}, {'name': '物流', 'children': ['快']}, {'name': '', 'children': ['不送货上门']}, {'name': '物流', 'children': ['全国第一']}, {'name': '配送员', 'children': ['服务周到']}, {'name': '物流', 'children': ['速度也快']}, {'name': '发货', 'children': ['快']}, {'name': '送货', 'children': ['方便']}, {'name': '送货', 'children': ['很快']}, {'name': '送货', 'children': ['及时']}, {'name': '快递', 'children': ['服务很好']}, {'name': '物流', 'children': ['连地址都找不到']}, {'name': '物流速度', 'children': ['好好']}, {'name': '快递', 'children': ['一星给']}, {'name': '物流', 'children': ['很神速']}, {'name': '速度', 'children': ['也快']}, {'name': '物流', 'children': ['很快']}, {'name': '发货速度', 'children': ['快']}, {'name': '发货速度', 'children': ['快']}, {'name': '', 'children': ['送货到家']}, {'name': '物流', 'children': ['配送很快']}, {'name': '物流速度', 'children': ['很快']}, {'name': '快递', 'children': ['很给力']}, {'name': '物流速度', 'children': ['快']}, {'name': '物流', 'children': ['很快']}, {'name': '快递小哥', 'children': ['很给力']}, {'name': '物流', 'children': ['一塌糊涂']}, {'name': '物流速度', 'children': ['快']}, {'name': '物流', 'children': ['挺快的']}, {'name': '送货', 'children': ['快']}, {'name': '快递员态度', 'children': ['特别差']}, {'name': '物流', 'children': ['很快']}, {'name': '物流', 'children': ['快捷']}, {'name': '快递', 'children': ['速度']}, {'name': '态度', 'children': ['也好']}, {'name': '物流速度', 'children': ['多次催发货']}, {'name': '快递员', 'children': ['非常好']}, {'name': '快递', 'children': ['送货上门的']}, {'name': '速度', 'children': ['早上下单，下午送达']}, {'name': '速度', 'children': ['满意']}]}, {'name': '售后', 'children': [{'name': '客服', 'children': ['没人管']}, {'name': '退货', 'children': ['不给上门取件']}, {'name': '投诉', 'children': ['不会回复']}, {'name': '售后服务', 'children': ['好']}, {'name': '客服', 'children': ['一袋米宝一样']}, {'name': '客服', 'children': ['店铺客服不在京东']}, {'name': '', 'children': ['反馈了，也没回复']}, {'name': '卖家', 'children': ['不退不换']}, {'name': '服务', 'children': ['好']}, {'name': '服务', 'children': ['很周到']}, {'name': '售后', 'children': ['省心']}, {'name': '客服', 'children': ['无客服服务']}, {'name': '送货', 'children': ['很快']}, {'name': '服务', 'children': ['很好']}, {'name': '客服', 'children': ['不作为']}, {'name': '客服', 'children': ['很差劲']}, {'name': '', 'children': ['卖家说可以免费更换']}, {'name': '服务态度', 'children': ['好']}, {'name': '客服', 'children': ['态度超好']}, {'name': '服务', 'children': ['很热情']}, {'name': '卖家', 'children': ['没人理']}, {'name': '客服', 'children': ['无法转人工']}, {'name': '客服', 'children': ['没有人管']}, {'name': '售后', 'children': ['说好送赠品']}, {'name': '客服', 'children': ['联系不上']}, {'name': '货', 'children': ['要自己付快递费']}, {'name': '', 'children': ['赔1.92元']}, {'name': '', 'children': ['还不如直接给我退货呢']}, {'name': '服务', 'children': ['差']}, {'name': '态度', 'children': ['差']}, {'name': '平台', 'children': ['不靠谱']}, {'name': '客服', 'children': ['敷衍']}]}, {'name': '其它', 'children': [{'name': '', 'children': ['非常失望']}, {'name': '', 'children': ['不错']}, {'name': '卖家服务态度', 'children': ['可以']}, {'name': '饼干', 'children': ['碎了']}, {'name': '', 'children': ['非常满意']}, {'name': '产品香气', 'children': ['好好']}, {'name': '京东', 'children': ['值得信赖！']}]}]}, 

        
      }
    },
    mounted() {
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

      initChart(Data) {
        this.chart = echarts.init(this.$el)
        // let seriesData = []
        // for (var index in Data){
        //     seriesData.push({value:1, name:'Data[index]'})
        //     // seriesData.push({
        //     //   name: Data[index]['name'], children: Data[index]['children']
        //     // })
        // }
        
        let option = {
            title: {
              text: '本体图谱',
              subtext: '层次化展示农产品评价类别\n\n点击节点展开/收起子类别',
              top: 'top',
              left: 'left'
            },
            tooltip: {
                trigger: 'item',
                triggerOn: 'mousemove'
            },
            series:[
                {
                    type: 'tree',
                    data: [this.ProductData],
                    top: '18%',
                    bottom: '14%',
                    // layout: 'radial',
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
</script> -->

<style scoped>
  .graph {
    margin-top: 20px;
    /* background-color: red; */
  }
</style>

<script>
  import echarts from 'echarts'
  import resize from '@/utils/echarts_resize.js'

  export default {
    name: 'KgProduct',
    mixins: [resize],
    props: {
      className: {
        type: String,
        default: 'chart'
      },
      width: {
        type: String,
        default: '500px'
      },
      height: {
        type: String,
        default: '500px'
        // default: '100%'
      }
    },
    data() {
      return {
        chart: null,
      }
    },
    mounted() {
      this.initChart('等待获取', '', {'name': '产品'})
    },
    beforeDestroy() {
      if (!this.chart) {
        return
      }
      this.chart.dispose()
      this.chart = null
    },
    methods: {
      initChart(titleText, subTitleText, Data) {
        console.log(Data)
        let seriesData = Data
        
        this.chart = echarts.init(this.$el)
        let option = {
            color: ['#63b2ee', '#76da91', '#f8cb7f', '#f89588', '#7cd6cf'],
            title: {
                text: '产品图谱 - ' + titleText,
                subtext: '点击类别查看具体评价',
                left: 'center'
            },
            tooltip: {
                trigger: 'item',
                triggerOn: 'mousemove',
                // formatter: '{a} <br/>{b} : {c} ({d}%)'
            },
            series: [
              {
                type: 'tree',
                name: '产品图谱-大米',
                data: [seriesData],
                // top: '20%',
                left: '20%',
                // bottom: '22%',
                right: '18%',
                // symbolSize: 7,
                initialTreeDepth: 1,
                label: {
                  position: 'left',
                  verticalAlign: 'middle',
                  align: 'right'
                },
                leaves: {
                  label: {
                    position: 'right',
                    verticalAlign: 'middle',
                    align: 'left'
                  }
                },
                expandAndCollapse: true,
                emphasis: {
                  focus: 'descendant'
                },
                animationDuration: 550,
                animationDurationUpdate: 750
              }
            ]
        }
        this.chart.setOption(option)
        
      }
    }
  }
</script>

<!-- <style lang="scss" scoped>
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
</style> -->
