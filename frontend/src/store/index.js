import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

// 加载 ./modules 中的所有文件内容，用对象的形式保存
const modulesFiles = require.context('./modules', true, /\.js$/)
const modules = modulesFiles.keys().reduce((modules, modulePath) => {
  // './app.js' => 'app'
  const key = modulePath.replace(/^\.\/(.*)\.\w+$/, '$1')
  const value = modulesFiles(modulePath).default
  modules[key] = value
  return modules
}, {})

// 综合为getter，类似于计算属性
const getters = {
  sidebar: state => state.app.sidebar,
  size: state => state.app.size,
  device: state => state.app.device,
  
  visitedViews: state => state.tagsView.visitedViews,
  cachedViews: state => state.tagsView.cachedViews,
}

const store = new Vuex.Store({
  modules,
  getters
})

export default store

