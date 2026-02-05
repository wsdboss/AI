import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
import socketService from './utils/socketService'

// 配置axios
axios.defaults.baseURL = ''
Vue.prototype.$axios = axios

// 使用ElementUI
Vue.use(ElementUI)

Vue.config.productionTip = false

// 初始化WebSocket服务，添加到Vue原型
Vue.prototype.$socket = socketService

// 创建Vue实例前初始化WebSocket连接
// 由于init()现在是异步的，我们需要等待它完成后再创建Vue实例
socketService.init().then(() => {
  console.log('WebSocket初始化完成，创建Vue实例...')
  new Vue({
    router,
    store,
    render: h => h(App)
  }).$mount('#app')
}).catch(error => {
  console.error('WebSocket初始化出错，但仍将创建Vue实例:', error)
  // 即使WebSocket初始化失败，也要创建Vue实例，确保应用能正常运行
  new Vue({
    router,
    store,
    render: h => h(App)
  }).$mount('#app')
})