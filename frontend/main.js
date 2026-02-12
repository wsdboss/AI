import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'

// 配置axios
axios.defaults.baseURL = ''
Vue.prototype.$axios = axios

// 使用ElementUI
Vue.use(ElementUI)

Vue.config.productionTip = false

// 创建Vue实例
console.log('创建Vue实例...')
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')