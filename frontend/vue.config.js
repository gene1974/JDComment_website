
const path = require('path')
function resolve(dir) {
  return path.join(__dirname, dir)
}

const name = '农产品情感分析系统'

module.exports = {
  devServer: {
      port: 9070,     // 端口号
  },
  configureWebpack: {
    name: name,
  },
  chainWebpack: config => {
    config.module
      .rule('svg')
      .exclude.add(resolve('src/icons'))
      .end()
    config.module
      .rule('icons')
      .test(/\.svg$/)
      .include.add(resolve('src/icons'))
      .end()
      .use('svg-sprite-loader')
      .loader('svg-sprite-loader')
      .options({
        symbolId: 'icon-[name]'
      })
      .end() 
  }
}
