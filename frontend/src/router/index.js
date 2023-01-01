import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style

import Layout from '@/layout/index.vue'

export const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/home',
    children: [{
      path: 'home',
      component: () => import('@/views/home/Home.vue'),
      name: '主页',
      meta: {title: 'Home', icon: 'el-icon-s-home', affix: true, noCache: true}
    }]
  },
  {
    path: 'dataPresent',
    component: Layout,
    name: 'shujuku',
    meta: {title: '民意数据', icon: 'el-icon-edit-outline'},
    children: [{
      path: 'dataPresent',
      component: () => import('@/views/dataPresent/index.vue'),
      name: 'dataPresent',
      meta: {title: '数据展示', noCache: true, icon: 'el-icon-edit-analysis'}
    },
    {
      path: 'annotator',
      component: () => import('@/views/annotator/index.vue'),
      name: 'Annotator',
      meta: {title: '数据标注', noCache: true, icon: 'el-icon-edit-outline'}
      //     meta: {title: '数据标注', icon: 'el-icon-document-copy', noCache: true}
    // },
    // {
    //   path: 'annotatorChange',
    //   component: () => import('@/views/annotatorChange/index.vue'),
    //   name: 'annotatorChange',
    //   meta: {title: '标注修改', noCache: true, icon: 'el-icon-edit-outline'}
    }]
  },
  {
    path: '/dataAnalysis',
    component: Layout,
    name: 'shujufenxi',
    meta: {title: '情感分析', icon: 'el-icon-data-analysis'},
    children: [{
      path: 'dataAnalysis',
      component: () => import('@/views/dataAnalysis/index.vue'),
      name: 'dataAnalysis',
      meta: {title: '数据分析', icon: 'el-icon-data-analysis'}
    },
    {
      path: 'analysis',
      component: () => import('@/views/analysis/index.vue'),
      name: 'analysis',
      meta: {title: '文本分析', icon: 'el-icon-data-analysis'}
    },
    {
      path: 'whitepaper',
      component: () => import('@/views/whitepaper/index.vue'),
      name: 'whitepaper',
      meta: {title: '白皮书', icon: 'el-icon-download'},
    },
  ]
},
  {
    path: '/xiaofeigraph',
    component: Layout,
    children: [{
      path: 'index',
      component: () => import('@/views/xiaofeigraph/index.vue'),
      name: 'xiaofeigraph',
      meta: {title: '知识图谱', icon: 'el-icon-document-copy'}
    }]
  },
  {
    path: '/knowledgegraph',
    component: Layout,
    // meta: {title: '可视化', icon: 'el-icon-s-help'},
    children: [{
      path: 'index',
      component: () => import('@/views/knowledgegraph/index.vue'),
      name: 'knowledgegraph',
      meta: {title: '图谱查询', icon: 'el-icon-search'}
    // },{
    //   path: 'neovisgraph',
    //   component: () => import('@/views/kg/neovisgraph.vue'),
    //   name: 'neovisgraph',
      // meta: {title: '图谱前端', icon: 'el-icon-document-copy'}
    },
  ]
  },
  {
    path: '/whitepaper',
    component: Layout,
    meta: {title: '白皮书', icon: 'el-icon-reading'},
    children: [{
      path: 'index',
      component: () => import('@/views/whitepaper/index.vue'),
      name: 'whitepaper',
      meta: {title: '总览', icon: 'el-icon-document'}
    },
    {
      path: 'fengcheng',
      component: () => import('@/views/whitepaper/fengcheng.vue'),
      name: 'fengcheng',
      meta: {title: '江西丰城大米', icon: 'el-icon-download'}
    },{
      path: 'chaohu',
      component: () => import('@/views/whitepaper/chaohu.vue'),
      name: 'chaohu',
      meta: {title: '安徽巢湖番茄', icon: 'el-icon-download'}
    },{
      path: 'xiantao',
      component: () => import('@/views/whitepaper/xiantao.vue'),
      name: 'xiantao',
      meta: {title: '湖北仙桃莲藕', icon: 'el-icon-download'}
    },{
      path: 'fengxin',
      component: () => import('@/views/whitepaper/fengxin.vue'),
      name: 'fengxin',
      meta: {title: '江西奉新猕猴桃', icon: 'el-icon-download'}
    },{
      path: 'jinggangshan',
      component: () => import('@/views/whitepaper/jinggangshan.vue'),
      name: 'jinggangshan',
      meta: {title: '江西井冈山蜜柚', icon: 'el-icon-download'}
    },{
      path: 'shanggao',
      component: () => import('@/views/whitepaper/shanggao.vue'),
      name: 'shanggao',
      meta: {title: '江西上高大蒜', icon: 'el-icon-download'}
    },{
      path: 'yongxin',
      component: () => import('@/views/whitepaper/yongxin.vue'),
      name: 'yongxin',
      meta: {title: '江西永新橙皮', icon: 'el-icon-download'}
    },{
      path: 'wannian',
      component: () => import('@/views/whitepaper/wannian.vue'),
      name: 'wannian',
      meta: {title: '江西万年茶油', icon: 'el-icon-download'}
    },{
      path: 'yibin',
      component: () => import('@/views/whitepaper/yibin.vue'),
      name: 'yibin',
      meta: {title: '四川宜宾屏山桠橙', icon: 'el-icon-download'}
    }
  ]
  },
  // {
  //   path: '/',
  //   component: Layout,
  //   redirect: '/whitepaper',
  //   children: [{
  //     path: 'index',
  //     component: () => import('@/views/whitepaper/index.vue'),
  //     name: 'index',
  //     meta: {title: '白皮书', icon: 'el-icon-s-home', affix: true, noCache: true}
  //   }]
  // },
  // {
  //   path: '/analysis',
  //   component: Layout,
  //   children: [{
  //     path: 'temp',
  //     component: () => import('@/views/analysis/temp.vue'),
  //     name: 'temp',
  //     meta: {title: 'temp', icon: 'el-icon-data-analysis'}
  //   }]
  // }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})


// 个性化配置进度条外观
NProgress.configure({
    easing: 'ease',  // 动画方式    
    speed: 500,  // 递增进度条的速度    
    showSpinner: false, // 是否显示加载ico    
    trickleSpeed: 200, // 自动递增间隔    
    minimum: 0.3 // 初始化时的最小百分比
})

router.beforeEach((to, from, next) => {
    NProgress.start()
    next()
})
router.afterEach(() => {
    NProgress.done()
})

export default router
