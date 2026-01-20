import Vue from 'vue'
import VueRouter from 'vue-router'

// 导入视图组件
import FileUploadView from '../views/FileUploadView.vue'
import InterfaceListView from '../views/InterfaceListView.vue'
import InterfaceDetailView from '../views/InterfaceDetailView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    components: {
      left: FileUploadView,
      main: InterfaceListView,
      right: InterfaceDetailView
    }
  },
  {
    path: '/interface/:id',
    name: 'interface-detail',
    components: {
      left: FileUploadView,
      main: InterfaceListView,
      right: InterfaceDetailView
    },
    props: {
      right: true
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: '/',
  routes
})

export default router